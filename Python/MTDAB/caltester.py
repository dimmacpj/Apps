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
    phaseShiftPriSec = 0       # Phase Shift between Pri and Sec, out of 0.5, half switching cycle                                                                                                                                                                                                                                                       
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

    #Vmj, Vmn, Vs, Ll, Tx, Ty, Tmj, Tmn, Ts, i1, i2, i3 = sp.symbols('Vmj, Vmn, Vs, Ll, Tx, Ty, Tmj, Tmn, Ts, i1, i2, i3', positive = True)

    
    Vmj, Vmn, Vs, Ll, Tps, Tmj, Tmn, Ts , Tzero = sp.symbols('Vmj, Vmn, Vs, Ll, Tps, Tmj, Tmn, Ts, Tzero', positive = True)
    i1 = Vs*Tzero/(2*Ll)          # Equation for instantaneous primary inductor current at the end of Tps
    i2 = i1 + (Vmj - Vs)*(Tmj)/Ll         # Equation for instantaneous primary inductor current at the end of Tjm
    i1 = i2 + (Vmn - Vs)*Tmn/Ll         # Equation for instantaneous primary inductor current at the end of Tmn
    Tzero = (i1 + i1) * inductanceL / (secVrep) 
    

    iMJ = (i1 + i2)*(Tmj)/Ts        # Average current during major period
    iMN = (i2 + i1)*Tmn/Ts              # Average current during minor period
    
    i1 = sp.simplify(i1.expand().subs([(Vmj, mcVMajor), (Vs, secVrep), (Tps, psPeriod), (Ll, inductanceL), (Vmn, mcVMinor)]))     
    i2 = sp.simplify(i2.expand().subs([(Vmn, mcVMinor), (Vs, secVrep), (Ll, inductanceL), (Vmj, mcVMajor), (Tps, psPeriod)]))        
    print(i1)
    print(i2)
    periodEquation = Tmj + Tmn + Tzero - switchPeriod/2
    actualIRatio = sp.simplify((iMN/iMJ).expand().subs([(Vmn, mcVMinor), (Vmj, mcVMajor), (Vs, secVrep), (Tps, psPeriod), (Ll, inductanceL)]))    

    periods = sp.solve([actualIRatio - targetIRatio, periodEquation], [Tmj, Tmn])
    print(periods[Tmj])
    actualImj = - iMJ.subs([(Vmn, mcVMinor), (Vmj, mcVMajor), (Vs, secVrep), (Tps, psPeriod), (Ll, inductanceL), (Ts, switchPeriod), (Tmj, periods[Tmj]), (Tmn, periods[Tmn])])
    actualImn = - iMN.subs([(Vmn, mcVMinor), (Vmj, mcVMajor), (Vs, secVrep), (Tps, psPeriod), (Ll, inductanceL), (Ts, switchPeriod), (Tmj, periods[Tmj]), (Tmn, periods[Tmn])])

    print(actualImj, actualImn)   
    tMajor = periods[Tmj]
    tMinor = periods[Tmn]
    #print(tMajor, tMinor)
    
    '''
# Phase shift = 0
    Tzero = 2 * inductanceL / (secVrep)
    eq1 = (i1 - i2 + (Vmj - Vs)*Tmj/Ll).subs([(Vmn, mcVMinor), (Vs, secVrep), (Ll, inductanceL), (Vmj, mcVMajor), (Ts, switchPeriod)])          # Equation for instantaneous primary inductor current at the end of Tps
    eq2 = (i2 - i1 + (Vmn - Vs)*Tmn/Ll).subs([(Vmn, mcVMinor), (Vs, secVrep), (Ll, inductanceL), (Vmj, mcVMajor), (Ts, switchPeriod)])         # Equation for instantaneous primary inductor current at the end of Tjm
    #eq3 = (- i3 + i2 + (- Vs)*(switchPeriod/2 - Tmj - Tmn)/Ll).subs([(Vmn, mcVMinor), (Vs, secVrep), (Ll, inductanceL), (Vmj, mcVMajor), (Ts, switchPeriod)])         # Equation for instantaneous primary inductor current at the end of Tmn
    eq3 = Tzero - 2 * inductanceL / (secVrep)
    eq5 = Tmj + Tmn + Tzero - switchPeriod/2
# Common eqs
    currents = sp.solve([eq1, eq2, eq3,eq5], [i1, i2])
    print(currents)
    i1 = currents[0]
    i2 = currents[1]
    #i3 = currents[i3]
    print(i1, i2)
    
    iMJ = sp.simplify(((i1*Ty - i3*Tx)/Ts).subs([(Ts, switchPeriod)]))        # Average current during major period
    iMN = sp.simplify(((i1 + i2)*Tmn/Ts).subs([(Ts, switchPeriod)]))              # Average current during minor period

    #print(iMJ)
    #print(iMN/iMJ)
    Tzero = 2 * inductanceL / (secVrep) 
    #print(Tzero)
    eq5 = Tmj + Tmn + Tzero - switchPeriod/2
    eq6 = (iMJ + iMN) * ipVaInst - iMJ * ipVbInst - iMN * ipVcInst - opPower
    actualIRatio = iMN/iMJ   
    print(ipVaInst, ipVbInst, ipVcInst)

    periods = sp.solve([actualIRatio - targetIRatio, eq5, eq6], [Tmj, Tmn])
    print(periods)

    actualImj = sp.simplify(iMJ.subs([(Vmn, mcVMinor), (Vmj, mcVMajor), (Vs, secVrep), (Ll, inductanceL), (Ts, switchPeriod), (Tmj, periods[0][0]), (Tmn, periods[0][1]), (Tx, periods[0][2]), (Ty, periods[0][3])]))
    actualImn = sp.simplify(iMN.subs([(Vmn, mcVMinor), (Vmj, mcVMajor), (Vs, secVrep), (Ll, inductanceL), (Ts, switchPeriod), (Tmj, periods[0][0]), (Tmn, periods[0][1]), (Tx, periods[0][2]), (Ty, periods[0][3])]))
        
    print(actualImj)
    print(actualImn)
    '''

if __name__ == '__main__':
    main()