import xml.etree.cElementTree as ET
import random
#from lxml import etree


def createTree():
    tree = ET.parse('C:\\Users\\neal.peng\\Documents\\Works\\Motive\\MP BoM+Config creation\\G3 1P configs\\SOC-MPG31VAU-A0\\SOC-MPG31VAU-A0.xml')
    root = tree.getroot()
    print(root.tag, root.attrib)
    print(root.find('entry').find('value').text)
    root.findall('.//*[@key="charger.ACCable"]/value')[0].text = random.randrange(8)
    print(root.findall('.//*[@key="charger.ACCable"]/value')[0].text)

'''print(root.tag, root.attrib)
for child in root:
    #print(child.tag, child.attrib)
    if 'charger.ACCable' in str(child.attrib) and 'BOOLEAN' in str(child.attrib):
        print(child.find('value').text)
for sub in root.iter('entry'):
    #print(sub.attrib)
    if 'charger.ACCable' in str(sub.attrib) and 'STRING' in str(sub.attrib):
        sub.find('value').text = 'IEC C20'
        #tree.write('C:\\Users\\neal.peng\\Documents\\Works\\Motive\\MP BoM+Config creation\\G3 1P configs\\SOC-MPG31VAU-A0\\SOC-MPG31VAU-A0.xml')
        print(sub.find('value').text)
        #print('Boolean key', sub.attrib)'''
#for enty in root.findall('entry'):
    #print(enty)
    #print(enty.find('value').text)

def main():
    createTree()

if __name__ == '__main__':
    main()
