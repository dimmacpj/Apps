import numpy as np
import sympy as sp

def equationcal():
    Vmj, Vmn, Vs, Ll, Dps, Dmj, Dmn, Ts, Dzero, i1, i2, i3, turns = sp.symbols('Vmj, Vmn, Vs, Ll, Dps, Dmj, Dmn, Ts, Dzero, i1, i2, i3, turns')    #Dps = 2Tps/Ts
    #Tps > 0
    eq1 = Dmj + Dmn + Dzero - 1
    eq2 = -2*i1 + (Vmj+Vs)/Ll*(Dps*(Ts/2))      #inductor current at the end of Tps
    eq3 = i1 - i2 + (Vmj-Vs)/Ll*(Dmj*(Ts/2)-Dps*(Ts/2))      #inductor current at the end of Tmj
    eq4 = i2 - i3 + (Vmn-Vs)/Ll*(Dmn*(Ts/2))      #inductor current at the end of Tmn
    eq5 = i3 - i1 + (-Vs)/Ll*(Dzero*(Ts/2))      #inductor current at the end of Tzero

    #currents = sp.solve([eq1, eq2, eq3, eq4, eq5], [i1, i2, i3], dict = True)
    i1s = sp.solve(eq2, i1)[0]
    print(sp.collect(i1s, Dps))
    i2s = sp.solve(eq3.subs(i1, i1s), i2)[0]
    print(sp.simplify(i2s).collect([Dmj, Dps]))
    i3s = sp.solve(eq4.subs(i2, i2s), i3)[0]
    print(sp.simplify(i3s).collect([Dmj, Dps, Dmn]))
    print(sp.simplify(eq5.subs([(i1, i1s), (i3, i3s), (Dzero, 1-Dmj-Dmn)])).collect([Dmj, Dps, Dmn]))
    Tzero = sp.simplify((i1s - i3s) * Ll / (-Vs))
    DZero = 2 * Tzero / Ts
    print(DZero)
    eq1 = eq1.subs(Dzero, DZero)

    iMJ = (i1s + i2s)*((Dmj - Dps)*(Ts/2))/Ts
    iMN = (i2s + i3s)*(Dmn*(Ts/2))/Ts
    print(sp.simplify(iMJ))
    print(sp.simplify(iMN))
    iPRIavg = iMJ + iMN + (i3s + i1s)*(1 - Dmj - Dmn)*(Ts/2)/Ts
    iOUTavg = iPRIavg/turns
    print(sp.simplify(iOUTavg))
    eq6 = iOUTavg - 100
    periods = sp.solve([eq1, eq6], [Dmj, Dmn])
    print(periods)

def main():
    equationcal()

if __name__ == '__main__':
    main()