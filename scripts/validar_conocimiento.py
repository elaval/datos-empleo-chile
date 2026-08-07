"""Valida la Base de Conocimiento (`conocimiento/`) en tres vías independientes.

Correr DESPUÉS de `generar_conocimiento.py`, en cada release:

    python -m scripts.validar_conocimiento

Bloques de validación:
  A. Coherencia interna  — las sumas y las identidades de la propia base cuadran.
  B. vs microdatos       — recómputo independiente desde los microdatos (fact_cal).
  C. vs boletines INE    — contraste contra las cifras publicadas por el INE,
                           transcritas a mano en `conocimiento/referencia-ine.json`.

(B) detecta errores del generador; (C) detecta que la base entera se haya desviado
de la fuente oficial. Son complementarios: (B) puede pasar y (C) fallar.

⚠ (C) solo aplica a releases recientes. Los boletines anteriores a la recalibración
con proyecciones post-Censo 2017 NO coinciden con esta base (es esperado, no un error):
ver el caveat `recalibracion-censo-2017` en `conocimiento/metodologia.md`.

Sale con código 1 si alguna verificación falla (usable en CI).
"""
from __future__ import annotations

import json
import pathlib
import sys

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONO = ROOT / "conocimiento"
EVID = CONO / "evidencia"
MICRO_DIR = ROOT / "data" / "processed" / "microdatos"

MESES = {1: "def", 2: "efm", 3: "fma", 4: "mam", 5: "amj", 6: "mjj",
         7: "jja", 8: "jas", 9: "aso", 10: "son", 11: "ond", 12: "nde"}
REGION = {1: "Tarapacá", 2: "Antofagasta", 3: "Atacama", 4: "Coquimbo", 5: "Valparaíso",
          6: "O'Higgins", 7: "Maule", 8: "Biobío", 9: "La Araucanía", 10: "Los Lagos",
          11: "Aysén", 12: "Magallanes", 13: "Metropolitana", 14: "Los Ríos",
          15: "Arica y Parinacota", 16: "Ñuble"}
GRUPOS_EDAD = [(15, 24, "15-24"), (25, 34, "25-34"), (35, 44, "35-44"),
               (45, 54, "45-54"), (55, 64, "55-64"), (65, 200, "65 y más")]
CATEGORIA = {1: "empleador", 2: "cuenta_propia", 3: "asalariado_sector_privado",
             4: "asalariado_sector_publico", 5: "servicio_domestico",
             6: "servicio_domestico", 7: "familiar_no_remunerado"}

TOL_PERSONAS = 1.0   # tolerancia por redondeo de la evidencia
TOL_TASA = 0.06      # el boletín publica 1 decimal; la base, 2

fallos: list[str] = []
checks = 0


def check(ok: bool, etiqueta: str, detalle: str = "") -> None:
    global checks
    checks += 1
    print(f"  {'✓' if ok else '✗'} {etiqueta}{('  — ' + detalle) if detalle else ''}")
    if not ok:
        fallos.append(etiqueta)


def main() -> int:
    snap = json.load(open(EVID / "snapshot.json", encoding="utf-8"))
    release = snap["release"]
    ano, mes = snap["periodo"]["ano"], snap["periodo"]["mes_central"]
    nac = snap["nacional"]
    print(f"Validando Base de Conocimiento — release {release}\n")

    # ---------------------------------------------------------------- A
    print("A. Coherencia interna de la base")
    check(abs(nac["ft"] - (nac["o"] + nac["do"])) <= TOL_PERSONAS,
          "identidad FT = O + DO", f"{nac['ft'] - nac['o'] - nac['do']:+.0f}")
    check(abs(100 * nac["do"] / nac["ft"] - nac["td"]) < 0.01, "TD = 100·DO/FT")
    check(abs(100 * nac["ft"] / nac["pet"] - nac["tp"]) < 0.01, "TP = 100·FT/PET")

    comp = {k: v for k, v in snap["composicion_ocupados"].items() if k != "_agregados"}
    suma_comp = sum(v["o"] for v in comp.values())
    check(abs(suma_comp - nac["o"]) <= TOL_PERSONAS,
          "composición por categoría suma ocupados", f"{suma_comp - nac['o']:+.0f}")

    f = snap["formalidad"]
    suma_f = f["o_formal"]["o"] + f["o_informal"]["o"]
    check(abs(suma_f - nac["o"]) <= TOL_PERSONAS,
          "formal + informal = ocupados", f"{suma_f - nac['o']:+.0f}")

    for dim, obj in snap["cortes"].items():
        s = sum(g["o"] for g in obj["grupos"])
        check(abs(s - nac["o"]) <= TOL_PERSONAS, f"corte '{dim}' suma ocupados",
              f"{s - nac['o']:+.0f}")

    edu = snap.get("educacion")
    if edu:
        cob = edu["_cobertura"]
        check(abs(cob["suma_niveles"] + cob["sin_dato_de_nivel"] - nac["o"]) <= TOL_PERSONAS,
              "niveles educacionales + sin dato = ocupados",
              f"sin dato: {cob['sin_dato_de_nivel']:,.0f}")
        sup_tipos = sum(v["o"] for v in edu["superior_por_tipo"].values())
        check(abs(sup_tipos - edu["por_nivel"]["superior_completa"]["o"]) <= TOL_PERSONAS,
              "CFT + IP + universitaria = superior completa",
              f"{sup_tipos - edu['por_nivel']['superior_completa']['o']:+.0f}")
        d = edu["desajuste"]
        suma_d = (d["sup_en_puesto_alta_calificacion"]["o"]
                  + d["sup_en_puesto_no_alta_calificacion"]["o"])
        check(abs(suma_d - edu["por_nivel"]["superior_completa"]["o"]) <= TOL_PERSONAS,
              "desajuste (alta + no alta) = superior completa",
              f"{suma_d - edu['por_nivel']['superior_completa']['o']:+.0f}")
        t = 100 * d["sup_en_puesto_no_alta_calificacion"]["o"] / suma_d
        check(abs(t - edu["tasa_desajuste"]["valor"]) < 0.01, "tasa de desajuste bien calculada")

    sub = snap.get("subutilizacion")
    if sub:
        c = {k: v["o"] for k, v in sub["componentes"].items()}
        do_, idp = c["desocupados"], c.get("iniciadores_disponibles", 0)
        tpi_, ftp_ = c.get("parcial_involuntario", 0), c.get("fuerza_trabajo_potencial", 0)
        obe_, ft_, fta_ = c.get("ocupados_que_buscaron_empleo", 0), c["fuerza_trabajo"], c.get("fuerza_trabajo_ampliada")
        # Se recomputan desde los componentes: un renombre silencioso en la fuente puede
        # dejar una tasa publicada plausible pero fabricada (ver ADR-0002).
        esperado = {
            "su1": 100 * (do_ + idp) / (ft_ + idp),
            "su2": 100 * (do_ + idp + tpi_) / (ft_ + idp),
            "su3": 100 * (do_ + idp + ftp_) / fta_ if fta_ else None,
            "su4": 100 * (do_ + idp + tpi_ + ftp_) / fta_ if fta_ else None,
            "tpl": 100 * (do_ + idp + obe_) / (ft_ + idp),
        }
        for k, exp in esperado.items():
            got = sub["tasas"].get(k, {}).get("valor")
            if exp is None or got is None:
                continue
            check(abs(exp - got) < 0.02, f"{k} reproducible desde sus componentes",
                  f"calculado={exp:.3f} publicado={got}")
        if fta_:
            check(abs((ft_ + idp + ftp_) - fta_) <= TOL_PERSONAS,
                  "FTA = FT + ID + FTP", f"{ft_ + idp + ftp_ - fta_:+.0f}")
        t = {k: v["valor"] for k, v in sub["tasas"].items()}
        check(t["su1"] <= t["su2"] <= t["su4"] and t["su1"] <= t["su3"] <= t["su4"],
              "orden SU1 ≤ SU2/SU3 ≤ SU4")
        check(t["su1"] >= nac["td"], "SU1 ≥ TD (incorpora iniciadores disponibles)",
              f"su1={t['su1']} td={nac['td']}")
        check(idp > 0, "iniciadores disponibles > 0 (detecta el bug id/idisp de ADR-0002)",
              f"ID = {idp:,.0f}")

    ocu = snap.get("ocupacion_ciuo08")
    if ocu:
        s_g = sum(v["o"] for v in ocu["grupos"].values())
        check(abs(s_g - nac["o"]) <= TOL_PERSONAS, "grupos CIUO-08 suman ocupados",
              f"{s_g - nac['o']:+.0f}")
        alta = ocu["_agregados"]["alta_calificacion_g1_g3"]["o"]
        g13 = sum(ocu["grupos"][k]["o"] for k in
                  ("g1_directivos_gerentes", "g2_profesionales_cientificos",
                   "g3_tecnicos_nivel_medio"))
        check(abs(alta - g13) <= TOL_PERSONAS, "agregado alta calificación = G1+G2+G3")
        # El agregado CIUO-08 debe reproducir la columna que usa el desajuste educativo.
        if snap.get("educacion"):
            pat = snap["educacion"]["desajuste"]["puestos_alta_calificacion_total"]["o"]
            check(abs(alta - pat) <= TOL_PERSONAS,
                  "G1+G2+G3 coincide con `grupo_ciuo_alta` del desajuste educativo",
                  f"{alta - pat:+.0f}")

    jor = snap.get("jornada")
    if jor:
        cob = jor["_cobertura"]
        suma_tr = sum(v["o"] for v in jor["tramos"].values())
        check(abs(suma_tr - cob["o_declaran_horas"]) <= TOL_PERSONAS,
              "tramos de jornada suman los que declaran horas",
              f"{suma_tr - cob['o_declaran_horas']:+.0f}")
        check(abs(cob["o_declaran_horas"] + cob["no_declaran_horas"] - nac["o"]) <= TOL_PERSONAS,
              "declaran + no declaran horas = ocupados",
              f"no declaran: {cob['no_declaran_horas']:,.0f}")

    # --- Las VARIACIONES de cada partición deben sumar la variación nacional -------------
    # Verificar solo los niveles no basta: un error puede aparecer en los deltas (o en un
    # gráfico que los muestre) sin romper las sumas de stock.
    d_nac = nac["delta_yoy"]["delta_o"]

    def suma_deltas(dic, campo="delta_o"):
        return sum(v[campo] for v in dic.values() if v.get(campo) is not None)

    check(abs(suma_deltas(comp) - d_nac) <= TOL_PERSONAS,
          "Δ composición por categoría suma la Δ nacional",
          f"{suma_deltas(comp) - d_nac:+.0f}")
    check(abs((f["o_formal"]["delta_o"] + f["o_informal"]["delta_o"]) - d_nac) <= TOL_PERSONAS,
          "Δ formal + Δ informal = Δ nacional",
          f"{f['o_formal']['delta_o'] + f['o_informal']['delta_o'] - d_nac:+.0f}")
    for dim, obj in snap["cortes"].items():
        s = sum(g["delta_yoy"]["delta_o"] for g in obj["grupos"]
                if g.get("delta_yoy", {}).get("delta_o") is not None)
        check(abs(s - d_nac) <= TOL_PERSONAS, f"Δ corte '{dim}' suma la Δ nacional",
              f"{s - d_nac:+.0f}")
    if snap.get("ocupacion_ciuo08"):
        s = suma_deltas(snap["ocupacion_ciuo08"]["grupos"])
        check(abs(s - d_nac) <= TOL_PERSONAS, "Δ grupos CIUO-08 suma la Δ nacional",
              f"{s - d_nac:+.0f}")
    # Particiones con residuo: la suma cuadra al sumar la variación del residuo.
    if snap.get("educacion"):
        cob = snap["educacion"]["_cobertura"]
        if cob.get("delta_sin_dato_de_nivel") is not None:
            s = suma_deltas(snap["educacion"]["por_nivel"]) + cob["delta_sin_dato_de_nivel"]
            check(abs(s - d_nac) <= TOL_PERSONAS,
                  "Δ niveles educacionales + Δ sin dato = Δ nacional",
                  f"residuo {cob['delta_sin_dato_de_nivel']:+,.0f}")
    if snap.get("jornada"):
        cobj = snap["jornada"]["_cobertura"]
        if cobj.get("delta_no_declaran_horas") is not None:
            s = suma_deltas(snap["jornada"]["tramos"]) + cobj["delta_no_declaran_horas"]
            check(abs(s - d_nac) <= TOL_PERSONAS,
                  "Δ tramos de jornada + Δ no declaran = Δ nacional",
                  f"residuo {cobj['delta_no_declaran_horas']:+,.0f}")

    # Hallazgos: refs y caveats resolubles
    hal = json.load(open(CONO / "hallazgos" / "hallazgos.json", encoding="utf-8"))
    glosario = hal["esquema"]["caveats"]["glosario"]
    slugs = {c for h in hal["hallazgos"] for c in h["caveats"] if " " not in c}
    check(slugs <= set(glosario), "todos los slugs de caveats están glosados",
          f"sin glosa: {sorted(slugs - set(glosario)) or 'ninguno'}")
    check(all(h.get("vigencia") and h.get("confianza") for h in hal["hallazgos"]),
          "todos los hallazgos declaran vigencia y confianza")

    # ---------------------------------------------------------------- B
    print("\nB. Base vs microdatos (recómputo independiente, ponderado por fact_cal)")
    micro_path = MICRO_DIR / f"ene-{mes:02d}-{MESES[mes]}.parquet"
    m = pd.read_parquet(micro_path)
    s = m[(m.ano_trimestre == ano) & (m.edad >= 15)]
    w = s.fact_cal
    r = {"pet": w.sum(), "o": w[s.activ == 1].sum(), "do": w[s.activ == 2].sum()}
    r["ft"] = r["o"] + r["do"]
    for k in ("pet", "ft", "o", "do"):
        check(abs(r[k] - nac[k]) <= TOL_PERSONAS, f"nacional · {k}",
              f"micro={r[k]:,.0f} pack={nac[k]:,.0f}")

    oc = s[s.activ == 1]
    rec_cat = oc.assign(_c=oc.categoria_ocupacion.map(CATEGORIA)).groupby("_c").fact_cal.sum()
    peor = max(abs(rec_cat.get(k, 0) - v["o"]) for k, v in comp.items())
    check(peor <= TOL_PERSONAS, "composición por categoría", f"peor desvío {peor:.1f}")

    inf = w[(s.activ == 1) & (s.ocup_form == 2)].sum()
    check(abs(inf - f["o_informal"]["o"]) <= TOL_PERSONAS, "ocupados informales",
          f"micro={inf:,.0f} pack={f['o_informal']['o']:,.0f}")

    def bin_edad(df):
        out = pd.Series(index=df.index, dtype=object)
        for lo, hi, lab in GRUPOS_EDAD:
            out[(df.edad >= lo) & (df.edad <= hi)] = lab
        return out

    claves = {
        "sexo": s.sexo.map({1: "Hombre", 2: "Mujer"}),
        "edad": bin_edad(s),
        "region": s.region.map(REGION),
        "nacionalidad": s.nacionalidad.apply(
            lambda x: "Chileno/a" if x == 152 else ("Extranjero/a" if pd.notna(x) else None)),
    }
    for dim, clave in claves.items():
        tmp = s.assign(_g=clave)
        peor = 0.0
        for g in snap["cortes"][dim]["grupos"]:
            sub = tmp[tmp._g == g["clave"]]
            ww = sub.fact_cal
            peor = max(peor, abs(ww[sub.activ == 1].sum() - g["o"]),
                       abs(ww[sub.activ == 2].sum() - g["do"]),
                       abs(len(sub) - g["n"]))
        check(peor <= TOL_PERSONAS, f"corte '{dim}' (O, DO y n)", f"peor desvío {peor:.1f}")

    # ---------------------------------------------------------------- C
    print("\nC. Base vs boletines publicados por el INE")
    ref_path = CONO / "referencia-ine.json"
    if not ref_path.exists():
        print("  (sin referencia-ine.json: se omite)")
    else:
        ref = json.load(open(ref_path, encoding="utf-8"))["releases"]
        if release not in ref:
            print(f"  ⚠ el release {release} no está en referencia-ine.json — "
                  "agregar las cifras del boletín para validarlo")
        else:
            r0 = ref[release]
            print(f"  (boletín n°{r0['boletin']}, {r0['trimestre']})")
            for k, v in r0["niveles"].items():
                pack_v = nac.get(k) if k in nac else (
                    f["o_informal"]["o"] if k == "o_informal" else None)
                if pack_v is None:
                    continue
                check(abs(pack_v - v) <= TOL_PERSONAS, f"nivel · {k}",
                      f"INE={v:,} pack={pack_v:,.0f}")
            tasas = {"td": nac["td"], "tp": nac["tp"], "to": nac["to"],
                     "toi": f["tasa_ocupacion_informal"]["toi"]}
            sexo = {g["clave"]: g for g in snap["cortes"]["sexo"]["grupos"]}
            tasas["td_mujeres"] = sexo["Mujer"]["td"]
            tasas["td_hombres"] = sexo["Hombre"]["td"]
            for k, v in r0["tasas"].items():
                if k in tasas:
                    check(abs(tasas[k] - v) < TOL_TASA, f"tasa · {k}",
                          f"INE={v} pack={tasas[k]}")

    # ---------------------------------------------------------------- fin
    print(f"\n{'—' * 56}")
    if fallos:
        print(f"✗ {len(fallos)} de {checks} verificaciones FALLARON:")
        for x in fallos:
            print(f"    · {x}")
        return 1
    print(f"✓ {checks}/{checks} verificaciones OK — la base es consistente "
          "internamente, con los microdatos y con los boletines del INE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
