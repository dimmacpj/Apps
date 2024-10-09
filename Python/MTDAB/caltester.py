import sympy as sp
import numpy as np


def main():
    opVdc = 43.2         # Output DC Voltage
    opIdc = 100           # Output DC Current
    opPower = opVdc*opIdc       # Output Power
    turnsRatio = 10      # Turns ratio
    #Powerfactor = 1      # Set PF to 1
    inductanceL = 35*1e-6     # Pirmary inductance, unit is H
    switchFreq = 14.285*1e4     # Switching Frequency, unit is Hz
    switchPeriod = 1/switchFreq     # Switching Period, unit is s
    phaseShiftPriSec = 2       # Phase Shift between Pri and Sec, out of 0.5, half switching cycle                                                                                                                                                                                                                                                       
    psPeriod = phaseShiftPriSec/0.5*(1/switchFreq/2)    # Phase Shift durition, unit is s
    ipVphph = 480        # Input Phase to Phase AC RMS Votlage
    ipIphph = opPower/1/ipVphph       # Input Phase to Phase AC RMS Current
    ipVphn = ipVphph/np.sqrt(3)       # Input Phase to Nuetral AC RMS Current
    ipIphn = ipIphph/np.sqrt(3)       # Input Phase to Nuetral AC RMS Current
    ipVamplitude = ipVphn*np.sqrt(2)      # Input Phase to Nuetral AC Voltage Amplitude
    ipIamplitude = ipIphn*np.sqrt(2)      # Input Phase to Nuetral AC Current Amplitude
    #ipACFreq = 50        # Input AC frequency
    acAngle = 10         # Input AC Phase Angle, unit is degree
    ipVaInst = ipVamplitude*np.cos(acAngle/180*np.pi)       # Instantaneous Phase A voltage at 10 degree phase angle
    ipVbInst = ipVamplitude*np.cos(acAngle/180*np.pi + 2/3*np.pi)         # Instantaneous Phase B voltage at 10 degree phase angle
    ipVcInst = ipVamplitude*np.cos(acAngle/180*np.pi - 2/3*np.pi)         # Instantaneous Phase C voltage at 10 degree phase angle
    ipIatarget = ipIamplitude*np.cos(acAngle/180*np.pi)       # Instantaneous Phase A current at 10 degree phase angle
    ipIbtarget = ipIamplitude*np.cos(acAngle/180*np.pi + 2/3*np.pi)         # Instantaneous Phase B current at 10 degree phase angle
    ipIctarget = ipIamplitude*np.cos(acAngle/180*np.pi - 2/3*np.pi)         # Instantaneous Phase C current at 10 degree phase angle
    mcVMajor = np.sort(abs(np.array([ipVaInst, ipVbInst, ipVcInst])))[2] + np.sort(abs(np.array([ipVaInst, ipVbInst, ipVcInst])))[1]    # Major voltage of Matrix converter's output  
    mcVMinor = np.sort(abs(np.array([ipVaInst, ipVbInst, ipVcInst])))[2] + np.sort(abs(np.array([ipVaInst, ipVbInst, ipVcInst])))[0]    # Minor voltage of Matrix converter's output
    mcIMajorTarget = - np.sort(abs(np.array([ipIatarget, ipIbtarget, ipIctarget])))[1]      # Targeted major current
    mcIMinorTarget = - np.sort(abs(np.array([ipIatarget, ipIbtarget, ipIctarget])))[0]      # Targeted minor current
    #ipPower = ipVaInst*ipIatarget + ipVbInst*ipIbtarget + ipVcInst*ipIctarget       # Input Power
    secVrep = opVdc*turnsRatio      # The reflect voltage at primary to replace output voltage and turns ratio
    targetIRatio = mcIMinorTarget/mcIMajorTarget        # Ratio of the target Minor current and Major current, which is equal to the ratio of the minor on time and major on time

    Vmj, Vmn, Vs, Ll, Tx, Ty, Tmj, Tmn, Ts, i1, i2, i3 = sp.symbols('Vmj, Vmn, Vs, Ll, Tx, Ty, Tmj, Tmn, Ts, i1, i2, i3', positive = True)

# Phase shift = 0
    if phaseShiftPriSec == 0 :
        eq1 = (- i1 -i3 + (Vmj - Vs)*Tmj/Ll).subs([(Vmn, mcVMinor), (Vs, secVrep), (Ll, inductanceL), (Vmj, mcVMajor), (Ts, switchPeriod)])          # Equation for instantaneous primary inductor current at the end of Tps
        eq2 = (- i2 + i1 + (Vmn - Vs)*(Tmn)/Ll).subs([(Vmn, mcVMinor), (Vs, secVrep), (Ll, inductanceL), (Vmj, mcVMajor), (Ts, switchPeriod)])         # Equation for instantaneous primary inductor current at the end of Tjm
        eq3 = (- i3 + i2 + (- Vs)*(switchPeriod/2 - Tmj - Tmn)/Ll).subs([(Vmn, mcVMinor), (Vs, secVrep), (Ll, inductanceL), (Vmj, mcVMajor), (Ts, switchPeriod)])         # Equation for instantaneous primary inductor current at the end of Tmn
    
# Phase shift = Tmj
    else :
        eq1 = (- i1 - i3 + (Vmj + Vs)*Tmj/Ll).subs([(Vmn, mcVMinor), (Vs, secVrep), (Ll, inductanceL), (Vmj, mcVMajor), (Ts, switchPeriod)])
        eq2 = (- i2 + i1 + (Vmn - Vs)*(Tmn)/Ll).subs([(Vmn, mcVMinor), (Vs, secVrep), (Ll, inductanceL), (Vmj, mcVMajor), (Ts, switchPeriod)])
        eq3 = (- i3 + i2 + (- Vs)*(switchPeriod/2 - Tmj - Tmn)/Ll).subs([(Vmn, mcVMinor), (Vs, secVrep), (Ll, inductanceL), (Vmj, mcVMajor), (Ts, switchPeriod)])
    
# Common eqs
    currents = sp.solve([eq1, eq2, eq3], [i1, i2, i3])
    #print(currents[i1])
    i1 = currents[i1]
    i2 = currents[i2]
    i3 = currents[i3]
    #print(i1, i2, i3)
    
    iMJ = sp.simplify(((i1*Ty - i3*Tx)/Ts).subs([(Ts, switchPeriod)]))        # Average current during major period
    iMN = sp.simplify(((i1 + i2)*Tmn/Ts).subs([(Ts, switchPeriod)]))              # Average current during minor period

    #print(iMJ)
    #print(iMN/iMJ)

    eq4 = Tmj - Tx - Ty
    Tzero = (i2 - i3) * inductanceL / (secVrep) 
    #print(Tzero)
    eq5 = Tmj + Tmn + Tzero - switchPeriod/2
    eq6 = (iMJ + iMN) * ipVaInst - iMJ * ipVbInst - iMN * ipVcInst - opPower
    actualIRatio = iMN/iMJ   
    print(ipVaInst, ipVbInst, ipVcInst)

    periods = sp.solve([eq4, actualIRatio - targetIRatio, eq5, eq6], [Tmj, Tmn, Tx, Ty])
    print(periods)

    actualImj = sp.simplify(iMJ.subs([(Vmn, mcVMinor), (Vmj, mcVMajor), (Vs, secVrep), (Ll, inductanceL), (Ts, switchPeriod), (Tmj, periods[0][0]), (Tmn, periods[0][1]), (Tx, periods[0][2]), (Ty, periods[0][3])]))
    actualImn = sp.simplify(iMN.subs([(Vmn, mcVMinor), (Vmj, mcVMajor), (Vs, secVrep), (Ll, inductanceL), (Ts, switchPeriod), (Tmj, periods[0][0]), (Tmn, periods[0][1]), (Tx, periods[0][2]), (Ty, periods[0][3])]))
        
    print(actualImj)
    print(actualImn)
    

if __name__ == '__main__':
    main()