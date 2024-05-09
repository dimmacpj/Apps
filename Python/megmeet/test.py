import pandas as pd
import numpy as np
import time
import datetime


'''
arr1 = np.array([])
arr2 = np.array([])
arr3 = np.array([])

for x in range(5):
    arr1 = np.append(arr1, x)
    arr2 = np.append(arr2, x+1)
    arr3 = np.append(arr3, x+2)

pd1 = pd.DataFrame(data={'arra1':arr1,'arr2':arr2,'arr3':arr3})
print(pd1)
'''
#gmt = time.gmtime(time.time())
#print(datetime.datetime.now().time())
#print(bin(525).zfill(32))
#print(format(525,'032b'))
'''
alarmBi = f'{525:032b}'
alarmList = ['Cabinet address conflict alarm', 'Seriour unbalanced bus voltage alarm',
            'Module input power failure alrm', 'Reserved', 'Module output fuse break alarm', 'Module internal communication abnormal alarm',
            'Drop line alarm', 'Module unbalanced current alarm', 'Module PFC fault alarm', 
            'Module input overvoltage alarm', 'Reserved', 'Serious uneven current alarm caused by the module not being able to carry the load',
            'Module AC phase loss alarm', 'Module AC imbalance alarm', 'Module input undervoltage alarm',
            'Module sequence start function enable', 'Reserved', 'Output overvoltage protection alarm',
            'Reserved', 'Internal overtemperature alarm', 'Module WALK-IN function enable',
            'Reserved', 'Module shutdown status', 'Low temperature shutdown alarm',
            'Reserved', 'Reserved', 'Reserved', 'Fan failure alarm', 'Module protection alarm',
            'Module failure alarm', 'Ambient temperature over temperature alarm', 'Output overvoltage lockout alarm']
alarmDict = dict(zip(alarmList, alarmBi))
alarmArry = []
print(alarmDict.items())
for key, value in alarmDict.items():
    if value == '1':
        print(f'{key} : On')
        alarmArry.append(key)

print(alarmArry)
'''
listOne = []
if listOne == []:
    print('None')
else:
    print('Full')

