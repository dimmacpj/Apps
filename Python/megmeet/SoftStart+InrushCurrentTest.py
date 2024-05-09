import numpy as np
import pandas as pd
import datetime
import HiokiPW

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
        
        #Data arrays
        timeArr = np.array([])
        #uutOVMeasArr = np.array([])
        hioOVMeasArr = np.array([])
        #uutIVMeasArr = np.array([])
        hioIVMeasArr = np.array([])
        hioIIMeasArr = np.array([])

        #Start test
        #No AC supplied
        while float(hioki.query(':MEAS? Urms1')) < 0.5:
            print('UUT power off')
            #Record time
            timeArr = np.append(timeArr, datetime.datetime.now().time())
            
            #Record measurements into data arrays
            hioOVMeasArr = np.append(hioOVMeasArr, float(hioki.query(':MEAS? Urms4')))
            hioIVMeasArr = np.append(hioIVMeasArr, float(hioki.query(':MEAS? Urms1')))
            hioIIMeasArr = np.append(hioIIMeasArr, float(hioki.query(':MEAS? Irms1')))

        #Create UUT instance
        #megRect = Megmeet.Megmeet()

        #Start supplying AC
        while float(hioki.query(':MEAS? Urms1')) > 0.5:
            
            #Record time
            timeArr = np.append(timeArr, datetime.datetime.now().time())
            #print(datetime.datetime.now().time())
            #Record measurements into data arrays
            #uutOVMeasArr = np.append(uutOVMeasArr, megRect.opVMeas())
            #print(megRect.opVMeas())
            hioOVMeasArr = np.append(hioOVMeasArr, float(hioki.query(':MEAS? Urms4')))
            #print(float(hioki.query(':MEAS? Urms4')))
            #uutIVMeasArr = np.append(uutIVMeasArr, megRect.ipVMeas())
            #print(megRect.ipVMeas())
            hioIVMeasArr = np.append(hioIVMeasArr, float(hioki.query(':MEAS? Urms1')))
            #print(float(hioki.query(':MEAS? Urms1')))
            hioIIMeasArr = np.append(hioIIMeasArr, float(hioki.query(':MEAS? Irms1')))

            if float(hioki.query(':MEAS? Urms1')) < 210.0:
                print('Test finished')
                break
            
            print('UUT start')
        #testData = pd.DataFrame(data={'OV from UUT':uutOVMeasArr, 'OV from HIOKI':hioOVMeasArr, 'IV from UUT':uutIVMeasArr, 'IV from HIOKI':hioIVMeasArr, 'Time':timeArr})
        testData = pd.DataFrame(data={'OV from HIOKI':hioOVMeasArr,'IV from HIOKI':hioIVMeasArr,'II from HIOKI':hioIIMeasArr, 'Time':timeArr})
        testData.to_excel('SoftStart+InrushCurrent Test Result.xlsx')        

        #Close HIOKI connection
        hioki.closeHio()

    except Exception as e:
        print('\n Exception: ', e.__class__, e.args)

if __name__ == '__main__':
    main()
