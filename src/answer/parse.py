import xml.etree.ElementTree as ET

pronouns = ['he','she','it']

def decide_replacement(text, coref):
    if len(text) ==  1 and text[0].lower() in pronouns:
        return coref[0]
    return text


def create_document(root, coref_map):
    document = []
    for sen in root:
        for item in sen:
            if item.tag == 'w':
                document.append(item.text)
            elif item.tag == 'coref':
                temp = []
                for w in item:
                    temp.append(item.text)
                coref = coref_map[item.get('set-id')]
                replace = decide_replacement(text, coref)
                document.extend(replace)


if __name__ == '__main__':
    tree = ET.parse('out.txt')
    root = tree.getroot()
    create_document(root, {})
