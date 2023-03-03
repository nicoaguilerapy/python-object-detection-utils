import xml.etree.ElementTree as ET
tree = ET.parse('modelo.xml')
root = tree.getroot()

class DATAtoXML():
    filename = ""
    width = ""
    height = ""
    xmin = ""
    ymin = ""
    xmax = ""
    ymax = ""
    def __init__(self) -> None:
        pass

    def setXML(self):
        root[1].text = self.filename
        root[2][0].text = str(self.width)
        root[2][1].text = str(self.height)
        root[4][5][0].text = str(self.xmin)
        root[4][5][1].text = str(self.ymin)
        root[4][5][2].text = str(self.xmax)
        root[4][5][3].text = str(self.ymax)
    
    def __str__(self) -> str:
        return "{}, {}, {}".format(self.filename,self.width, self.height)

    def save(self, count):
        tree.write('result/Cars{}.xml'.format(count))