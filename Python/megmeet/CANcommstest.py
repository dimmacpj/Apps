import numpy as np 
import time
import HiokiPW
import pandas as pd
import Megmeet


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
        
        #Preset voltage to 42.0
        print(f'Setting voltage to 42.0Vdc, please wait...')
        while megRect.rwVolt(42.0) > 42.5:
            time.sleep(3.0)

        #Read and write output voltage test and meter reading
        vTMeg = np.array([])
        vRMeg = np.array([])
        vRHio = np.array([])
        print(f'Read and write output voltage test, range is 42 - 58Vdc...\n')
        for voltSP in np.arange(42.5, 59.0, 0.5):
            #lv.write_fixed32(1, 0x100, voltSP)
            print(f'Set o/p volt to {voltSP}\n')
            vTMeg = np.append(vTMeg, voltSP)
            megVolt = megRect.rwVolt(voltSP)
            vRMeg = np.append(vRMeg, megVolt)
            print(f'Reading from the module is {megVolt}\n')
            hiokiVMea = hioki.query(':MEAS? Urms4')
            vRHio = np.append(vRHio, hiokiVMea)
            print(f'Volt reading from the PW3390 is: {hiokiVMea}\n')
            time.sleep(1.0)    
        voltTestData = pd.DataFrame(data={'Send to Megmeet':vTMeg,'Read from Megmeet':vRMeg,'Read from HIOKI PW3390':vRHio})

        print(f'Setting voltage to 54.0Vdc, please wait...')
        while megRect.rwVolt(54.0) < 53.5:
            time.sleep(3.0)
        #Current limit test
        iLTMeg = np.array([])
        iLRMeg = np.array([])
        for iLSP in np.arange(0, 1.22, 0.122):
            print(f'Set iL to {iLSP}\n')
            iLTMeg = np.append(iLTMeg, iLSP)
            megIL = megRect.rwCurrLimit(iLSP)
            iLRMeg = np.append(iLRMeg, megIL)
            print(f'Reading from the module is {megIL}\n')
            time.sleep(1.0)
        iLTestData = pd.DataFrame(data={'Send to Megmeet':iLTMeg, 'Read from Megmeet':iLRMeg})


        #Save DFs to Excel
        with pd.ExcelWriter('CAMCOMSTEST.xlsx') as writer:
            voltTestData.to_excel(writer, sheet_name='Write and Read Volt')
            iLTestData.to_excel(writer, sheet_name='Write and Read Current Limit')

        #Close Megmeet communication
        megRect.close()
        #Close HIOKI connection
        hioki.closeHio()
    except Exception as e:
        print("\n  Exception:", e.__class__.__name__, e.args)
        
if __name__ == "__main__":
    main()