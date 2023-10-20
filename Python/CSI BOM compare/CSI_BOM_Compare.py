import numpy as np
import pandas as pd

print('First, please put the BOM excel files that you have pulled out from CSI into the same folder as this script.')
print('Second, rename the excel files to the CSI product name.')
input("Once you finished above two steps, please press Enter to continue...")
print('The CSI product name of first BOM:')
FirstBom = input()
#print('Excel name of first BOM, include extension:')
#FirstBomFileName = input()
print('The CSI product name of second BOM:')
SecondBom = input()
#print('Excel name of second BOM, include extension:')
#SecondBomFileName = input()

path = 'C:\\Users\\neal.peng\\Documents\\Programming\\Python\\CSI BOM compare\\'

BOMOne = pd.read_excel(path + FirstBom + '.xlsx', usecols=['Item', 'Description', 'Ref Designator'])
BOMTwo = pd.read_excel(path + SecondBom + '.xlsx', usecols=['Item', 'Description', 'Ref Designator'])

LengthOne = len(BOMOne)
LengthTwo = len(BOMTwo)

BOMOne.index = [FirstBom]*LengthOne
print(BOMOne.index)
BOMTwo.index = [SecondBom]*LengthTwo

#BOMOne = BOMOne.sort_values(['Item', 'Ref Designator'], ignore_index=True)
#BOMTwo = BOMTwo.sort_values(['Item', 'Ref Designator'], ignore_index=True)

#BOMTwo.set_index(['Item', 'Ref Designator']).count(level='Item').to_excel(path + 'twocount.xlsx')
#BOMOne.set_index(['Item', 'Ref Designator']).count(level='Item').to_excel(path + 'onecount.xlsx')
#BOMTwo.to_excel(path + 'RM2048.xlsx')
#BOMOne.to_excel(path + 'RM1860.xlsx')
'''
if LengthOne > LengthTwo:
    Delta = LengthOne - LengthTwo
elif LengthTwo > LengthOne:
    Delta = LengthTwo - LengthOne

DFDelta = pd.DataFrame(columns= BOMOne.columns, index=range(Delta))
#print(Delta)
if LengthOne > LengthTwo:
    BOMTwo = BOMTwo.append(DFDelta, ignore_index=True)
elif LengthTwo > LengthOne:
    BOMOne = BOMOne.append(DFDelta, ignore_index=True)
'''

#BOMTwo.to_excel('C:\\Users\\NUC\\Documents\\Pandas\\CSI BOM compare\\Two.xlsx')
#BOMOne.to_excel('C:\\Users\\NUC\\Documents\\Pandas\\CSI BOM compare\\One.xlsx')
#print(len(BOMOne) - len(BOMTwo))
#Result = BOMOne.head(60).compare(BOMTwo.head(60))
Result = pd.concat([BOMOne,BOMTwo]).drop_duplicates(keep=False).sort_values('Ref Designator')
Result.to_excel(path + 'Result.xlsx')
print('Now there will be an Excel file named Result.xlsx in the same folder as this script,')
print('open it and you will find the difference between the two BOMs. Thanks.')

