import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from matplotlib.widgets import TextBox, Button, Slider



def getInfo():
    opVdc = 43.2         # Output DC Voltage
    opIdc = 100           # Output DC Current
    opPower = opVdc*opIdc       # Output Power
    turnsRatio = 10      # Turns ratio
    #Powerfactor = 1      # Set PF to 1
    inductanceL = 35*1e-6     # Pirmary inductance, unit is H
    switchFreq = 14.285*1e4     # Switching Frequency, unit is Hz
    switchPeriod = 1/switchFreq     # Switching Period, unit is s
    phaseShiftPriSec = 0.0377       # Phase Shift between Pri and Sec, out of 0.5, half switching cycle                                                                                                                                                                                                                                                       
    psPeriod = phaseShiftPriSec/0.5*(1/switchFreq/2)    # Phase Shift durition, unit is s
    ipVphph = 480        # Input Phase to Phase AC RMS Votlage
    ipIphph = opPower/1/ipVphph       # Input Phase to Phase AC RMS Current
    ipVphn = ipVphph/np.sqrt(3)       # Input Phase to Nuetral AC RMS Current
    ipIphn = ipIphph/np.sqrt(3)       # Input Phase to Nuetral AC RMS Current
    ipVamplitude = ipVphn*np.sqrt(2)      # Input Phase to Nuetral AC Voltage Amplitude
    ipIamplitude = ipIphn*np.sqrt(2)      # Input Phase to Nuetral AC Current Amplitude
    #ipACFreq = 50        # Input AC frequency
    acAngle = 15.01         # Input AC Phase Angle, unit is degree
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

    return inductanceL, switchPeriod, psPeriod, mcVMajor, mcVMinor, secVrep, targetIRatio, ipVamplitude, opVdc, ipVaInst, ipVbInst, ipVcInst, opPower

def WFsPlot(inductanceL, switchPeriod, psPeriod, mcVMajor, mcVMinor, secVrep, targetIRatio, ipVamplitude, opVdc, ipVaInst, ipVbInst, ipVcInst, opPower):
    ''' Calculations, to get Tmajor, Tminor, Imajor<avg>, Iminor<avg> '''
    tMajor, tMinor, iMJAVG, iMNAVG = MTDABcal(inductanceL, switchPeriod, psPeriod, mcVMajor, mcVMinor, secVrep, targetIRatio, ipVaInst, ipVbInst, ipVcInst, opPower)
    print('Major current is ' + str(iMJAVG) + ', Minor current is ' + str(iMNAVG))                                  

    ''' Plot waveforms '''
    fig, (axs1, axs2) = plt.subplots(2)  # Create two plots vertically in one figure 
    fig.set_size_inches(22,12)

    # Create plot 1
    x1 = np.linspace(-30, 30, 60)
    phA = ipVamplitude*np.cos(x1/180*np.pi)       # Instantaneous Phase A current at 10 degree phase angle
    phB = ipVamplitude*np.cos(x1/180*np.pi + 2/3*np.pi)         # Instantaneous Phase B current at 10 degree phase angle
    phC = ipVamplitude*np.cos(x1/180*np.pi - 2/3*np.pi) 
    axs1.plot(x1, phA)
    axs1.plot(x1, phB)
    axs1.plot(x1, phC)
    axs1.set_xlabel('Phase Angle (\xb0)')
    axs1.set_ylabel('Voltage (V)')
    axs1.set_title('AC Waveforms')

    # Create plot 2 
    # Calculate data
    i1 = ((mcVMajor+secVrep)*psPeriod/(2*inductanceL))
    i2 = i1 + (mcVMajor - secVrep) * (tMajor-psPeriod) / inductanceL
    i3 = i2 + (mcVMinor - secVrep) * tMinor / inductanceL
    priVWF = [(0, mcVMajor), (tMajor*1e6, mcVMajor), (tMajor*1e6, mcVMinor), ((tMajor+tMinor)*1e6, mcVMinor), ((tMajor+tMinor)*1e6, 0), (switchPeriod/2*1e6, 0), (switchPeriod/2*1e6, -mcVMajor), 
              ((switchPeriod/2+tMajor)*1e6, -mcVMajor), ((switchPeriod/2+tMajor)*1e6, -mcVMinor), ((switchPeriod/2+tMajor+tMinor)*1e6, -mcVMinor), ((switchPeriod/2+tMajor+tMinor)*1e6, 0), 
              (switchPeriod*1e6, 0), (switchPeriod*1e6, mcVMajor)]
    secVWF = [(0, -opVdc), (psPeriod*1e6, -opVdc), (psPeriod*1e6, opVdc), ((switchPeriod/2+psPeriod)*1e6, opVdc), ((switchPeriod/2+psPeriod)*1e6, -opVdc), (switchPeriod*1e6, -opVdc)]
    priIWF = [(0, -i1), (psPeriod*1e6, i1), (tMajor*1e6, i2), ((tMajor+tMinor)*1e6, i3), (switchPeriod/2*1e6, i1), 
              ((switchPeriod/2+psPeriod)*1e6, -i1), ((switchPeriod/2+tMajor)*1e6, -i2), ((switchPeriod/2+tMajor+tMinor)*1e6, -i3), (switchPeriod*1e6, -i1)]
    line1, = axs2.plot(*zip(*secVWF), color = 'tab:blue')
    line2, = axs2.plot(*zip(*priVWF), color = 'tab:orange')
    axs2.set_xlabel('Time (s)')
    axs2.set_ylabel('Voltage (V)', color = 'tab:blue')
    axs2.tick_params(axis = 'y', labelcolor = 'tab:blue')
    axs2.set_title('Vin > Vout Positive phase')
    
    axs3 = axs2.twinx()         #   Create a new Axes with an invisible x-axis and an independent y-axis positioned opposite to the original one
    line3, = axs3.plot(*zip(*priIWF), color = 'tab:green')
    axs3.set_ylabel('Current (A)', color = 'tab:green')
    axs3.tick_params(axis = 'y', labelcolor = 'tab:green')

    #fig.tight_layout()      # Otherwise the area between the two subplots would be overlapped
    '''
    # Adjust figure to make room for the sliders
    fig.subplots_adjust(bottom = 0.3)
    # Create a horizontal slider for phase shift
    axPhaseShift = fig.add_axes([0.15, 0.15, 0.15, 0.01])
    ps_Slider = Slider(ax=axPhaseShift, label='Phase Shift (out of 0.5)', valmin= 0, valmax= 0.5, valinit=psPeriod/(switchPeriod/2)*0.5)
    
    def update(val):
        psPeriod = ps_Slider.val/0.5*(switchPeriod/2)
        tMajor, tMinor, iMJAVG, iMNAVG = MTDABcal(inductanceL, switchPeriod, psPeriod, mcVMajor, mcVMinor, secVrep, targetIRatio)
        i1 = ((mcVMajor+secVrep)*psPeriod/(2*inductanceL))
        i2 = i1 + (mcVMajor - secVrep) * (tMajor-psPeriod) / inductanceL
        i3 = i2 + (mcVMinor - secVrep) * tMinor / inductanceL
        priVWF = [(0, mcVMajor), (tMajor*1e6, mcVMajor), (tMajor*1e6, mcVMinor), ((tMajor+tMinor)*1e6, mcVMinor), ((tMajor+tMinor)*1e6, 0), (switchPeriod/2*1e6, 0), (switchPeriod/2*1e6, -mcVMajor), 
                ((switchPeriod/2+tMajor)*1e6, -mcVMajor), ((switchPeriod/2+tMajor)*1e6, -mcVMinor), ((switchPeriod/2+tMajor+tMinor)*1e6, -mcVMinor), ((switchPeriod/2+tMajor+tMinor)*1e6, 0), 
                (switchPeriod*1e6, 0), (switchPeriod*1e6, mcVMajor)]
        secVWF = [(0, -opVdc), (psPeriod*1e6, -opVdc), (psPeriod*1e6, opVdc), ((switchPeriod/2+psPeriod)*1e6, opVdc), ((switchPeriod/2+psPeriod)*1e6, -opVdc), (switchPeriod*1e6, -opVdc)]
        priIWF = [(0, -i1), (psPeriod*1e6, i1), (tMajor*1e6, i2), ((tMajor+tMinor)*1e6, i3), (switchPeriod/2*1e6, i1), 
                ((switchPeriod/2+psPeriod)*1e6, -i1), ((switchPeriod/2+tMajor)*1e6, -i2), ((switchPeriod/2+tMajor+tMinor)*1e6, -i3), (switchPeriod*1e6, -i1)]
        line1.set_data(*zip(*secVWF))
        line2.set_data(*zip(*priVWF))
        line3.set_data(*zip(*priIWF))
    ps_Slider.on_changed(update)
    '''
    plt.grid(True,linestyle="-",color="gray",linewidth="0.5",axis='both')
    plt.show()

def MTDABcal(inductanceL, switchPeriod, psPeriod, mcVMajor, mcVMinor, secVrep, targetIRatio, ipVaInst, ipVbInst, ipVcInst, opPower):
    """ Function to calculate the Major current and the Minor current based on knowing the ratio of the two."""
    '''
    Vmj, Vmn, Vs, Ll, Tps, Tmj, Tmn, Ts = sp.symbols('Vmj, Vmn, Vs, Ll, Tps, Tmj, Tmn, Ts', positive = True)
    i1 = (Vmj + Vs)*Tps/(2*Ll)          # Equation for instantaneous primary inductor current at the end of Tps
    i2 = i1 + (Vmj - Vs)*(Tmj - Tps)/Ll         # Equation for instantaneous primary inductor current at the end of Tjm
    i3 = i2 + (Vmn - Vs)*Tmn/Ll         # Equation for instantaneous primary inductor current at the end of Tmn

    iMJ = (i1 + i2)*(Tmj-Tps)/Ts        # Average current during major period
    iMN = (i2 + i3)*Tmn/Ts              # Average current during minor period
    
    i1 = sp.simplify(i1.expand().subs([(Vmj, mcVMajor), (Vs, secVrep), (Tps, psPeriod), (Ll, inductanceL)]))     
    i3 = sp.simplify(i3.expand().subs([(Vmn, mcVMinor), (Vs, secVrep), (Ll, inductanceL), (Vmj, mcVMajor), (Tps, psPeriod)]))        
    
    Tzero = (i1 - i3) * inductanceL / (-secVrep) 
    periodEquation = Tmj + Tmn + Tzero - switchPeriod/2
    actualIRatio = sp.simplify((iMN/iMJ).expand().subs([(Vmn, mcVMinor), (Vmj, mcVMajor), (Vs, secVrep), (Tps, psPeriod), (Ll, inductanceL)]))    

    periods = sp.solve([actualIRatio - targetIRatio, periodEquation], [Tmj, Tmn])

    actualImj = - iMJ.subs([(Vmn, mcVMinor), (Vmj, mcVMajor), (Vs, secVrep), (Tps, psPeriod), (Ll, inductanceL), (Ts, switchPeriod), (Tmj, periods[0][0]), (Tmn, periods[0][1])])
    actualImn = - iMN.subs([(Vmn, mcVMinor), (Vmj, mcVMajor), (Vs, secVrep), (Tps, psPeriod), (Ll, inductanceL), (Ts, switchPeriod), (Tmj, periods[0][0]), (Tmn, periods[0][1])])
        
    tMajor = periods[0][0]
    tMinor = periods[0][1]
    '''
    """ Function to calculate the Major current and the Minor current based on knowing the ratio of the two."""
    Vmj, Vmn, Vs, Ll, Tps, Tmj, Tmn, Ts = sp.symbols('Vmj, Vmn, Vs, Ll, Tps, Tmj, Tmn, Ts', positive = True)
    i1, i2, i3 = sp.symbols('i1, i2, i3')
    eq1 = ((Vmj + Vs)*Tps/(2*Ll) - i1).subs([(Vmn, mcVMinor), (Vmj, mcVMajor), (Vs, secVrep), (Tps, psPeriod), (Ll, inductanceL), (Ts, switchPeriod)])          # Equation for instantaneous primary inductor current at the end of Tps
    eq2 = (i1 + (Vmj - Vs)*(Tmj - Tps)/Ll - i2).subs([(Vmn, mcVMinor), (Vmj, mcVMajor), (Vs, secVrep), (Tps, psPeriod), (Ll, inductanceL), (Ts, switchPeriod)])         # Equation for instantaneous primary inductor current at the end of Tjm
    eq3 = (i2 + (Vmn - Vs)*Tmn/Ll - i3).subs([(Vmn, mcVMinor), (Vmj, mcVMajor), (Vs, secVrep), (Tps, psPeriod), (Ll, inductanceL), (Ts, switchPeriod)])         # Equation for instantaneous primary inductor current at the end of Tmn

    acCurrents = sp.solve([eq1, eq2, eq3], [i1, i2, i3])

    i1, i2, i3 = acCurrents.values()

    iMJ = sp.simplify(((i1 + i2)*(Tmj-Tps)/Ts).subs([(Tps, psPeriod), (Ts, switchPeriod)]))        # Average current during major period
    iMN = sp.simplify(((i2 + i3)*Tmn/Ts).subs([(Tps, psPeriod), (Ts, switchPeriod)]))              # Average current during minor period      
    
    Tzero = (i1 - i3) * inductanceL / (-secVrep) 
    eq4 = Tmj + Tmn + Tzero - switchPeriod/2
    eq5 = iMN/iMJ - targetIRatio   

    periods = sp.solve([eq4, eq5], [Tmj, Tmn])

    actualImj = - iMJ.subs([(Tmj, periods[0][0]), (Tmn, periods[0][1])])
    actualImn = - iMN.subs([(Tmj, periods[0][0]), (Tmn, periods[0][1])])
        
    tMajor = periods[0][0]
    tMinor = periods[0][1]

    return tMajor, tMinor, actualImj, actualImn

def main():
    calculationInfo = getInfo()
    WFsPlot(*calculationInfo)

if __name__ == '__main__':
    main()