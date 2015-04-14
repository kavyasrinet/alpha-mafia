import xml.etree.ElementTree as ET

tree = ET.parse('out.txt')
root = tree.getroot()
sen = root[0]
for sen in root:
    for item in sen:
        if item.tag == 'w':
            print item.text
        elif item.tag == 'coref':
            print item.get('set-id')
            print 'coref'
            for w in item:
                print w.text
            print 'end coref'

