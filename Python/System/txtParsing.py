import sys
import pandas as pd

def main():
   filePath = 'C:\\Users\\neal.peng\\Documents\\Works\\System\\Projects\\Narada Batt Comms Test\\ModbusPoll\\'
   fileName = 'ModbusPoll+16Batt'
   pdData = []
   header = ['Type', 'Time', 'Data']
   timeData = []

   with open(filePath + fileName + '.txt','r') as rtTxt:
      for line in rtTxt:
         #for Modbus Poll data
         val = line.split('-')
         #for qModbus data
         #val = line.replace('[RTU]>','').replace('>','-').split('-')
         pdData.append(dict(zip(header, val)))
   df = pd.DataFrame(pdData)

   for time in df['Time']:
      time = ''.join(time.split(':'))
      timeData.append(time[len(time) - 6:])
   df['Time'] = df['Time'].replace(df['Time'].tolist(), timeData)
   df.to_excel(filePath + fileName + '.xlsx')

if __name__ == '__main__':
    main()