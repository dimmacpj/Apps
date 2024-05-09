import Megmeet
import time
import HiokiPW
import sys

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

        #Create UUT instance
        megRect = Megmeet.Megmeet()

        #Start test
        while True:
            beforetime = time.time()
            while float(hioki.query(':MEAS? Urms4')) >= 63.0:
                if megRect.alarmStatus() != 0:
                    sdTime = time.time()
                    sys.exit(f'UUT entered into lockout mode, OVSD delay time is {(sdTime-beforetime)*1000}ms')
                    
    except Exception as e:
        print('\n Exception:', e.__class__, e.args)

if __name__ == '__main__':
    main()
