import Megmeet
import numpy as np
import pandas as pd
import HiokiPW
import time

def main():
    try:
        #Create HIOKI PW3390 instance
        hioki = HiokiPW.HiokiPW()
        print(f'Start connecting...\nPlease select HIOKI PW3390 from below resource list')
        #Display resource list
        print(hioki.getResource())
        hiokiResource = input()
        #Open HIOKI connection
        hioki.open(hiokiResource)
        #Display HIOKI ID
        hiokiID = hioki.query('*idn?')
        print(f'{hiokiID} is connected.\n')

        #Create a Megmeet module instance
        megRect = Megmeet.Megmeet()
        megRect.getInfo()
        megRect.alarmStatus()

        print('Setting OVSP to 59.7V.\n')
        print(f'Voltage info read from UUT\n {megRect.rwOVSD(59.7)}')
        time.sleep(2.0)

        #Internal overvoltage protection set point range test
        vTMeg = np.array([])
        vRMeg = np.array([])
        vRHio = np.array([])
        for ovspSP in np.arange(57.0, 60.5, 0.5):
            print(f'Set OVSP to {ovspSP}\n')
            vTMeg = np.append(vTMeg, ovspSP)
            megOVSDInfo = megRect.rwOVSD(ovspSP)        
            vRMeg = np.append(vRMeg, megOVSDInfo)
            print(f'Reading OVSP info from UUT:\n {megOVSDInfo}')
            hiokiVMea = hioki.query(':MEAS? Urms4')
            vRHio = np.append(vRHio, float(hiokiVMea))
            print(f'Volt reading from PW3390: {hiokiVMea}')
            time.sleep(2.0)
    
        ovspTestData = pd.DataFrame(data={'Send to UUT':vTMeg, 'Read from UUT':vRMeg, 'Read from PW3390':vRHio})
        
        #Overvoltage protection test
        ovsdRMeg = np.array([])
        alarmRMeg = np.array([])
        ovsdRHio = np.array([])
        print(f'Starting overvoltage protection test:'
              f'Set OVSP to 58.5V'
              f'Voltage info read from UUT: {megRect.rwOVSD(58.5)}'
              f'Alarm status: {megRect.alarmStatus()}')
        hiokiVMea = hioki.query(':MEAS? Urms4')
        print(f'Voltage on PW3390: {hiokiVMea}')
        ovsdRMeg = np.append(ovsdRMeg, megRect.rwOVSD(58.5))
        alarmRMeg = np.append(alarmRMeg, megRect.alarmStatus())
        ovsdRHio = np.append(ovsdRHio, float(hioki.query(':MEAS? Urms4')))
        print(f'Turn on bench power supply and start backfeeding DC to UUT\n')
        time.sleep(5.0)
        while float(hioki.query(':MEAS? Urms4')) < 58.5:
            print('Backfeeding voltage not reaches internal OVSP 58.5V, keep increasing...')
            print(f'Voltage info read from UUT: {megRect.rwOVSD(58.5)}'
              f'Alarm status: {megRect.alarmStatus()}')
            hiokiVMea = hioki.query(':MEAS? Urms4')
            print(f'Voltage on PW3390: {hiokiVMea}\n')
            ovsdRMeg = np.append(ovsdRMeg, megRect.rwOVSD(58.5))
            alarmRMeg = np.append(alarmRMeg, megRect.alarmStatus())
            ovsdRHio = np.append(ovsdRHio, float(hioki.query(':MEAS? Urms4')))
            time.sleep(2.0)
        while 63.0 > float(hioki.query(':MEAS? Urms4')) > 58.5:
            print(f'Backfeeding voltage reaches Internal OVSP 58.5V but not external OVSP 63V'
                f'Voltage info read from UUT: {megRect.rwOVSD(58.5)}'
                f'Alarm status: {megRect.alarmStatus()}')
            hiokiVMea = hioki.query(':MEAS? Urms4')
            print(f'Voltage on PW3390: {hiokiVMea}'
                f'Keep increasing backfeeding voltage until reach 63V.\n')
            ovsdRMeg = np.append(ovsdRMeg, megRect.rwOVSD(58.5))
            alarmRMeg = np.append(alarmRMeg, megRect.alarmStatus())
            ovsdRHio = np.append(ovsdRHio, float(hioki.query(':MEAS? Urms4')))
            time.sleep(2.0)
        while 63.0 < float(hioki.query(':MEAS? Urms4')):
            print(f'Backfeeding voltage reaches external OVSP 63V'
                f'Voltage info read from UUT: {megRect.rwOVSD(58.5)}'
                f'Alarm status: {megRect.alarmStatus()}')
            hiokiVMea = hioki.query(':MEAS? Urms4')
            print(f'Voltage on PW3390: {hiokiVMea}')
            ovsdRMeg = np.append(ovsdRMeg, megRect.rwOVSD(58.5))
            alarmRMeg = np.append(alarmRMeg, megRect.alarmStatus())
            ovsdRHio = np.append(ovsdRHio, float(hioki.query(':MEAS? Urms4')))
            print(f'Once UUT has been locked out, backfeeding voltage can be removed\n'
                  f'If removed type \'Y\' and Enter...')
            bfStatus = input()
            if bfStatus == 'Y':
                break
            else:
                time.sleep(1.0)
        print(f'Saving data.')
        protectTestData = pd.DataFrame(data={'Volt info from UUT':ovsdRMeg, 'Alarm info':alarmRMeg, 'Reading on PW3390':ovsdRHio})
        while 57.0 < float(hioki.query(':MEAS? Urms4')):
            print(f'Awaiting external voltage to drop below 57V, then restart the UUT.\n')
            time.sleep(2.0)
        print(f'Restarting UUT and exiting the programe...')
        megRect.ovsdReset()
        #Save DFs to Excel
        with pd.ExcelWriter('OVSDTestResult.xlsx') as writer:
            ovspTestData.to_excel(writer, sheet_name='OVSP range test')
            protectTestData.to_excel(writer, sheet_name='Protect test')

        #Close Megmeet communication
        megRect.close()
        #Close HIOKI connection
        hioki.closeHio()
    except Exception as e:
        print('\n Exception:', e.__class__.__name__, e.args)

if __name__ == '__main__':
    main()
