import megmeet.labview as lv
import time

class Megmeet:

    #Constructor
    def __init__(self) -> None:
        lv.open_connection(interface='pcan', channel='PCAN_USBBUS1')

    #Get module info
    def getInfo(self):
        print(f'Megmeet rectifier {bin(lv.read_int32(1, 0x001))} has been connected\n'
              f'Software and Hardware version is {lv.read_int16(1, 0x005)}\n')

    #Decipher alarm - from int to binary - then match with alarm name
    def onAlarm(self):
        alarmBi = f'{self.alarmStatus():032b}'
        alarmList = ['Cabinet address conflict alarm', 'Seriour unbalanced bus voltage alarm',
                     'Module input power failure alrm', 'Reserved', 'Module output fuse break alarm',
                     'Drop line alarm', 'Module unbalanced current alarm', 'Module PFC fault alarm', 
                     'Module input overvoltage alarm', 'Reserved', 'Serious uneven current alarm caused by the module not being able to carry the load',
                     'Module AC phase loss alarm', 'Module AC imbalance alarm', 'Module input undervoltage alarm',
                     'Module sequence start function enable', 'Reserved', 'Output overvoltage protection alarm',
                     'Reserved', 'Internal overtemperature alarm', 'Module WALK-IN function enable',
                     'Reserved', 'Module shutdown status', 'Low temperature shutdown alarm',
                     'Reserved', 'Reserved', 'Reserved', 'Fan failure alarm', 'Module protection alarm',
                     'Module failure alarm', 'Ambient temperature over temperature alarm', 'Output overvoltage lockout alarm']
        alarmDic = dict(zip(alarmList, alarmBi))
        onAlarms = []
        for key, value in alarmDic.items():
            if value == '1':
                print(f'{key} : On')
                onAlarms.append(key)
        if onAlarms == []:
            onAlarms.append('No alarms')
        return onAlarms

    #Read alarm status
    def alarmStatus(self):
        print(f'Module alarm status:\n'
              f'{lv.read_int48(1,0x183)}')
        return lv.read_int48(1, 0x183)

    #Read/Write o/p voltage
    def rwVolt(self, voltSP: float):
        lv.write_fixed32(1, 0x100, voltSP)
        time.sleep(2.0)
        
        return lv.read_fixed32(1, 0x175)
        
    #Read/Write OVSD
    def rwOVSD(self, ovsdSP: float):
        lv.write_fixed32(1, 0x102, ovsdSP)

        return {'DC output voltage overvoltage protection point': lv.read_fixed32(1, 0x102),
                'DC output voltage setting value': lv.read_fixed32(1, 0x100),
                'DC output voltage measurement': lv.read_fixed32(1, 0x175),
                'DC output external voltage': lv.read_fixed32(1, 0x184)}

    #OVSD lockout reset control
    def ovsdReset(self):
        lv.write_int8(1, 0x133, 1)

    #Read/Write o/p current limit
    def rwCurrLimit(self, iLimitSP: float):
        lv.write_fixed32(1, 0x103, iLimitSP)
        time.sleep(2.0)
        
        return {'Current limit setting value':lv.read_fixed32(1,0x103),  
                'Actual current limit point':lv.read_fixed32(1, 0x176)}

    #Read o/p current
    def opIMeas(self):
        return lv.read_fixed32(1, 0x182)
    
    #Output voltage measurement
    def opVMeas(self):
        return lv.read_fixed32(1, 0x175)
        
    #Input voltage 
    def ipVMeas(self):
        return lv.read_fixed32(1, 0x178)
    
    #Input current
    def ipIMeas(self):
        return lv.read_fixed32(1, 0x172)
    
    #Turn off module
    def turnOff(self):
        lv.write_int8(1, 0x132, 1)
        return True

    #Turn on module
    def turnOn(self):
        lv.write_int8(1, 0x132, 0)
        return True

    #Fan duty cycle feedbad
    def fanD(self):
        return lv.read_fixed32(1, 0x22B)


    #Close connection
    def close(self):
        lv.close_connection()



