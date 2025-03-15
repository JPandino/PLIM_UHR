import pandas as pd
import pyomo.environ as pyo
from pyomo.environ import*

def milp_optimization(uhr, As, Ai, P, VIs, VIi, VFs, VFi):

    steps = 24   # time steps (24 hours = 1 day)

    model = pyo.ConcreteModel()

    model.set_time = pyo.Set(initialize=range(steps))
    model.set_unit = pyo.Set(initialize=uhr["unit"])

    model.p = pyo.Var(model.set_unit, model.set_time, bounds=(0, None))
    p = model.p
    model.pw = pyo.Var(model.set_unit, model.set_time, bounds=(0, None))
    pw = model.pw
    model.qs = pyo.Var(model.set_time, bounds=(0, uhr["qsmax"]))
    qs = model.qs
    model.qi = pyo.Var(model.set_time, bounds=(0, uhr["qimax"]))
    qi = model.qi

    model.vs = pyo.Var(model.set_time, bounds=(uhr["vsmin"], uhr["vsmax"]))
    vs = model.vs
    model.vi = pyo.Var(model.set_time, bounds=(uhr["vimin"], uhr["vimax"]))
    vi = model.vi
    model.profit = pyo.Var(model.set_time, bounds=(None, None))
    profit = model.profit

    model.i_p = pyo.Var(model.set_unit, model.set_time, within=pyo.Binary)
    i_p = model.i_p
    model.i_pw = pyo.Var(model.set_unit, model.set_time, within=pyo.Binary)
    i_pw = model.i_pw
    model.i_p_pw = pyo.Var(model.set_unit, model.set_time, within=pyo.Binary)
    i_p_pw = model.i_p_pw
    model.i_pw_p = pyo.Var(model.set_unit, model.set_time, within=pyo.Binary)
    i_pw_p = model.i_pw_p
    model.i_f = pyo.Var(model.set_unit, model.set_time, within=pyo.Binary)
    i_f = model.i_f
    model.i_os = pyo.Var(model.set_unit, model.set_time, within=pyo.Binary)
    i_os = model.i_os
    model.i_off = pyo.Var(model.set_unit, model.set_time, within=pyo.Binary)
    i_off = model.i_off
    model.i_st = pyo.Var(model.set_unit, model.set_time, within=pyo.Binary)
    i_st = model.i_st

    def min_flow_p(model, u, t):  # Restrição de vazão mínima para unidade geradora no modo turbina
        return p[u,t] >= uhr["pmin"][u] * i_p[u,t]
    model.c1 = pyo.Constraint(model.set_unit, model.set_time, rule=min_flow_p)

    def min_flow_pw(model, u, t):  # Restrição de vazão mínima para unidade geradora no modo bomba
        return pw[u,t] >= uhr["pwmin"][u] * i_pw[u,t]
    model.c2 = pyo.Constraint(model.set_unit, model.set_time, rule=min_flow_pw)

    def upper_reservoir_rule(model, t): # Restrição de balanço hídrico do reservatório superior
        if t == 0:
            return vs[t] == VIs + 0.0036*(As[t] + sum([pw[u,t] for u in model.set_unit]) - sum([p[u,t] for u in model.set_unit]) - qs[t])  # Restrição para t=0
        else:
            return vs[t] == vs[t-1] + 0.0036*(As[t] + sum([pw[u,t] for u in model.set_unit]) - sum([p[u,t] for u in model.set_unit]) - qs[t])
    model.c3 = pyo.Constraint(model.set_time, rule=upper_reservoir_rule)

    def lower_reservoir_rule(model, t): # Restrição de balanço hídrico do reservatório inferior
        if t == 0:
            return vi[t] == VIi + 0.0036*(Ai[t] + sum([p[u,t] for u in model.set_unit]) + qs[t] - sum([pw[u,t] for u in model.set_unit]) - qi[t])  # Restrição para t=0
        else:
            return vi[t] == vi[t-1] + 0.0036*(Ai[t] + sum([p[u,t] for u in model.set_unit]) + qs[t] - sum([pw[u,t] for u in model.set_unit]) - qi[t])
    model.c4 = pyo.Constraint(model.set_time, rule=lower_reservoir_rule)

    model.c5 = pyo.Constraint(expr=vs[steps-1] == VFs)
    model.c6 = pyo.Constraint(expr=vi[steps-1] == VFi)

    model.c = pyo.ConstraintList()

    for t in model.set_time:
        # Profit
        model.c.add(expr=profit[t] == P[t]*(sum([p[u,t]*uhr["e_p"][u] for u in model.set_unit]) - uhr["M_acl"]) -
            P[t]*(sum([pw[u,t]*uhr["e_pw"][u] for u in model.set_unit])) -
            uhr["k1"]*(sum([p[u,t]*uhr["e_p"][u] for u in model.set_unit]) + sum([pw[u,t]*uhr["e_pw"][u] for u in model.set_unit])) -
            uhr["k2"]*sum([i_st[u,t] for u in model.set_unit]) - uhr["k3"]*sum([i_off[u,t] for u in model.set_unit]))

        for u in model.set_unit:
            model.c.add(expr=-uhr["pwmax"][u] + uhr["pwmin"][u] <= pw[u,t] - i_pw[u,t]*uhr["pwmax"][u])
            model.c.add(expr=pw[u,t] - i_pw[u,t]*uhr["pwmax"][u] <= 0)
            model.c.add(expr=-uhr["pmax"][u] + uhr["pmin"][u] <= p[u,t] - i_p[u,t]*uhr["pmax"][u])
            model.c.add(expr=p[u,t] - i_p[u,t]*uhr["pmax"][u] <= 0)

            model.c.add(expr=i_p[u,t] + i_pw[u,t] <= 1)
            model.c.add(expr=i_p[u,t] + i_pw[u,t] == i_f[u,t])
            model.c.add(expr=i_p_pw[u,t] + i_pw_p[u,t] + i_os[u,t] == i_st[u,t])

            if t == 0:
                model.c.add(expr=p[u,t] - p[u,t+1] <= uhr["rp"]*uhr["pmax"][u])
                model.c.add(expr=p[u,t+1] - p[u,t] <= uhr["rp"]*uhr["pmax"][u])
                model.c.add(expr=pw[u,t] - pw[u,t+1] <= uhr["rp"]*uhr["pwmax"][u])
                model.c.add(expr=pw[u,t+1] - pw[u,t] <= uhr["rp"]*uhr["pwmax"][u])

                model.c.add(expr=i_f[u,t+1] - i_f[u,t] == i_os[u,t+1] - i_off[u,t+1])
                model.c.add(expr=i_pw[u,t] + i_p[u,t+1] - i_pw_p[u,t+1] <= 1)
                model.c.add(expr=i_p[u,t] + i_pw[u,t+1] - i_p_pw[u,t+1] <= 1)

            else:
                model.c.add(expr=p[u,t-1] - p[u,t] <= uhr["rp"]*uhr["pmax"][u])
                model.c.add(expr=p[u,t] - p[u,t-1] <= uhr["rp"]*uhr["pmax"][u])
                model.c.add(expr=pw[u,t-1] - pw[u,t] <= uhr["rp"]*uhr["pwmax"][u])
                model.c.add(expr=pw[u,t] - pw[u,t-1] <= uhr["rp"]*uhr["pwmax"][u])

                model.c.add(expr=i_f[u,t] - i_f[u,t-1] == i_os[u,t] - i_off[u,t])
                model.c.add(expr=i_pw[u,t-1] + i_p[u,t] - i_pw_p[u,t] <= 1)
                model.c.add(expr=i_p[u,t-1] + i_pw[u,t] - i_p_pw[u,t] <= 1)

    model.obj = pyo.Objective(expr=sum([profit[t] for t in range(steps)]), sense=maximize)

    opt = pyo.SolverFactory("cplex")
    results = opt.solve(model)

    # Inicializa o Dataframe
    df_resultado = pd.DataFrame()

    if results.solver.termination_condition == pyo.TerminationCondition.optimal:  # Tem água para ir de VI a VF

        # Resultado das variáveis de decisão do modelo
        p_value = [[pyo.value(model.p[u,t]) for u in model.set_unit] for t in model.set_time]
        pw_value = [[pyo.value(model.pw[u,t]) for u in model.set_unit] for t in model.set_time]
        vs_value = [round(model.vs[i].value, 2) for i in model.vs]
        qs_value = [round(model.qs[i].value, 2) for i in model.qs]
        vi_value = [round(model.vi[i].value, 2) for i in model.vi]
        qi_value = [round(model.qi[i].value, 2) for i in model.qi]

        i_f_value = [sum([pyo.value(model.i_f[u,t]) for u in model.set_unit]) for t in model.set_time]
        i_p_pw_value = [[pyo.value(model.i_p_pw[u,t]) for u in model.set_unit] for t in model.set_time]
        i_pw_p_value = [[pyo.value(model.i_pw_p[u,t]) for u in model.set_unit] for t in model.set_time]
        i_os_value = [[pyo.value(model.i_os[u,t]) for u in model.set_unit] for t in model.set_time]
        i_off_value = [[pyo.value(model.i_off[u,t]) for u in model.set_unit] for t in model.set_time]

        # i_p_value = [round(model.i_p[i].value, 2) for i in model.i_p]
        # i_p_pw_value = [round(model.i_p_pw[i].value, 2) for i in model.i_p_pw]
        # i_pw_value = [round(model.i_pw[i].value, 2) for i in model.i_pw]
        # i_pw_p_value = [round(model.i_pw_p[i].value, 2) for i in model.i_pw_p]
        # i_f_value = [round(model.i_f[i].value, 2) for i in model.i_f]
        # i_os_value = [round(model.i_os[i].value, 2) for i in model.i_os]
        # i_st_value = [round(model.i_st[i].value, 2) for i in model.i_st]
        # i_off_value = [round(model.i_off[i].value, 2) for i in model.i_off]

        # Creat a Results DataFrame
        df_resultado = pd.DataFrame(data=[p_value, pw_value, vs_value, qs_value, vi_value, qi_value, i_f_value, i_p_pw_value, i_pw_p_value, i_os_value, i_off_value]).T
        df_resultado.columns = ["p", "pw", "vs", "qs", "vi", "qi", "i_f", "i_p_pw", "i_pw_p", "i_os", "i_off"]

    return df_resultado
