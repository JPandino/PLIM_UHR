from HIBRID import milp_hibrid

Sun_pred = [0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.006049,0.119073,0.325893,0.541241,0.729511,0.871414,0.954641,0.972483,0.925327,0.814170,0.645882,0.442199,0.225854,0.050824,0.000000]
As = [194, 200, 210, 212, 220, 300, 350, 350, 325, 300, 275, 250, 233, 230, 238, 225, 212, 208, 190, 180, 168, 150, 165, 176]
Ai = [120, 125, 130, 145, 150, 150, 160, 128, 110, 115, 120, 123, 125, 98, 99, 100, 105, 110, 112, 125, 150, 143, 136, 160]
P = [53.5,51.74,51.25,51.29,51.22,51.14,51.18,51.84,52.9,53.58,53.44,53.12,52.76,52.84,53.4,53.81,54.05,52.91,52.83,53.52,53.61,53.55,52.78,51.77]
uhr = {"Nome": "UHR_ACL",
        "unit": ["A", "B", "C", "D"],
        "vsmax": 5779,
        "vsmin": 1974,
        "vimax": 2950,
        "vimin": 2562,
        "qsmax": 10030,
        "qsmin": 0,
        "qimax": 16200,
        "qimin": 0,
        "pmax": {"A": 372, "B": 372, "C": 372, "D": 372},
        "pwmax": {"A": 372, "B": 372, "C": 372, "D": 372},
        "pmin": {"A": 50, "B": 50, "C": 50, "D": 50},
        "pwmin": {"A": 50, "B": 50, "C": 50, "D": 50},
        "e_p": {"A": 1.15*0.95, "B": 1.15*0.98, "C": 1.15*0.95, "D": 1.15*0.98},
        "e_pw": {"A": 1.15/0.90, "B": 1.15/0.92, "C": 1.15/0.90, "D": 1.15/0.92},
        "rp": 0.8,
        "VIs": 3876.5,
        "VIi": 2756,
        "VFs": 3876.5,
        "VFi": 2756,
        "C": 0.0036,
        "k1": 8.00,
        "k2": 1000.,
        "M_acl": 150.0,
        "P_acl": 141.58}
pps = {"efficiency": 0.85, # ? efficiency (decimal)
        "area": 9.03E+6, # area (m2)
        "M_solar": 40, # Quantidade de energia contratada por dia (MWh/dia)
        #"maxgrid": 150 # Solar grid max power (kw)
}

fob, unit, df_resultado = milp_hibrid(pps, uhr, Sun_pred, As, Ai, P)
vt = unit["vt"]
vb = unit["vb"]

print(f"Resultado da Função Objetivo: R${round(fob,2)}")
print(f"Volumes turbinado: {round(vt,2)}m³/s e bombeado: {round(vb,2)}m³/s")
print(f"Resultado das Variáveis de Decisão:\n {df_resultado}")

df_resultado.to_excel("df_resultado_HIBRID.xlsx")