import Megmeet
import HiokiPW
import datetime
import numpy as np
import pandas as pd
import time

def main():
    
    try:
        #Create HIOKI PW3390 instance
        hioki = HiokiPW.HiokiPW()
        print(f'Start connecting...\nPlease select HIOKI PW3390 from below resource list')
        #Display resource list
        print(hioki.getResource())
        hiokiResource = 'ASRL4::INSTR'
        #Open HIOKI connection
        hioki.open(hiokiResource)
        #Display HIOKI ID
        hiokiID = hioki.query('*idn?')
        print(f'{hiokiID} is connected.\n')

        #Create a Megmeet module instance
        megRect = Megmeet.Megmeet()

        #Data arrays
        timeArr = np.array([])
        uutOVMeasArr = np.array([])
        hioOVMeasArr = np.array([])
        hioOIMeasArr = np.array([])
        uutIVMeasArr = np.array([])
        hioIVMeasArr = np.array([])
        #uutAlarms = np.array([])

        print(f'Wating for UUT to startup...It will take about 1min...')
        while megRect.opVMeas() < 50:
            time.sleep(30.0)

        #Set OV to 54.5 as per Enatel 48V XHE module PRS
        print(f'Setting voltage to 54.5Vdc, please wait...')
        while megRect.rwVolt(54.5) < 54.4:
            time.sleep(3.0)

        #Apply load
        loadINPUT = input('Please apply 40A DC load.\n Once load is applied, please press ENTER to continue...')
        while loadINPUT != '':
            loadINPUT = input('Please apply 40A DC load.\n Once load is applied, please press ENTER to continue...')
        
        #Start test
        while True:
            #Record time
            timeArr = np.append(timeArr, datetime.datetime.now().time())
            #print(datetime.datetime.now().time())
            #Record measurements into data arrays
            uutOVMeasArr = np.append(uutOVMeasArr, megRect.opVMeas())
            #print(megRect.opVMeas())
            hioOVMeasArr = np.append(hioOVMeasArr, float(hioki.query(':MEAS? Urms4')))
            #print(float(hioki.query(':MEAS? Urms4')))
            hioOIMeasArr = np.append(hioOIMeasArr, float(hioki.query(':MEAS? Irms4')))
            uutIVMeasArr = np.append(uutIVMeasArr, megRect.ipVMeas())
            #print(megRect.ipVMeas())
            hioIVMeasArr = np.append(hioIVMeasArr, float(hioki.query(':MEAS? Urms1')))
            #print(float(hioki.query(':MEAS? Urms1')))
            #uutAlarms = np.append(uutAlarms, megRect.onAlarm())

            if float(hioki.query(':MEAS? Urms4')) < 3.0:
                print('Test finished, please turn off DC load.')
                break
            
            #print(len(uutAlarms),len(uutIVMeasArr),len(uutOVMeasArr),len(hioIVMeasArr),len(hioOIMeasArr),len(timeArr),len(hioOVMeasArr))
        
        testData = pd.DataFrame(data={'OV from UUT':uutOVMeasArr, 'OV from HIOKI':hioOVMeasArr, 'OI from HIOKI':hioOIMeasArr, 'IV from UUT':uutIVMeasArr, 'IV from HIOKI':hioIVMeasArr, 'Time':timeArr})
        #testData = pd.DataFrame(data={'OV from HIOKI':hioOVMeasArr,'IV from HIOKI':hioIVMeasArr, 'Time':timeArr})
        testData.to_excel('HoldupTestResult.xlsx')  

        #Close Megmeet communication
        megRect.close()
        #Close HIOKI connection
        hioki.closeHio()

    except Exception as e:
        print('\n Exception:', e.__class__, e.args)

if __name__ == '__main__':
    main()