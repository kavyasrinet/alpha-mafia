import xml.etree.ElementTree as ET
import requests
import sys

pronouns = ['he','she','it', 'they']
SERVER_PORT='8125'
SERVER_ADDRESS='http://localhost:%s/BARTDemo/ShowText/process/' % SERVER_PORT

def coref_list(root):
    coref_sets = {}
    sentence_count = 0
    for sen in root:
        for item in sen:
            if item.tag != 'coref':
                continue
            set_id = item.get('set-id')
            if set_id not in coref_sets:
                coref_sets[set_id] = (None,None)

            curr_coref = []
            for w in item:
                curr_coref.append(w.text)

            if coref_sets[set_id][0] is None:
                coref_sets[set_id] = (curr_coref, [curr_coref])
            else:
                coref_sets[set_id][1].append(curr_coref)
        #end for
        sentence_count+=1
    #end for
    return coref_sets, sentence_count

def decide_replacement(text, coref):
    if len(text) ==  1 and text[0].lower() in pronouns:
        return coref[0]
    return text

def create_document(root, coref_map):
    sentences = []
    for sen in root:
        document = []
        for item in sen:
            if item.tag == 'w':
                document.append(item.text)
            elif item.tag == 'coref':
                temp = []
                for w in item:
                    temp.append(item.text)
                coref = coref_map[item.get('set-id')]
                replace = decide_replacement(temp, coref)
                document.extend(replace)
        #end for
        sentences.append(document)
    #end for
    return sentences

def coref_server_request(p_text):
    r = requests.post(SERVER_ADDRESS, data = p_text.encode('utf-8',errors='ignore'))
    if (r.status_code, r.reason) == (200, 'OK'):
        return r.text.encode('utf-8',errors='ignore')
    else:
        return None

def get_resolved_sentence(context):
    resp = coref_server_request(' '.join(context))
    if not resp: return context[-1]
    root = None
    try:
        root = ET.fromstring(resp)
    except:
        return context[-1]
    coref_map, sentences = coref_list(root)
    if sentences != len(context):
        #we disagree on the number of sentences
        return context[-1]
    doc = create_document(root, coref_map)
    return ' '.join(doc[-1]).replace('\n',' ')

 #unit test
if __name__ == '__main__':
    if(len(sys.argv) != 2):
        sys.stderr.write('Correct Usage: python coref.py <inputFilePath>\n')
        sys.exit(1)
        #end if

    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    print coref_list(root)
    server_input = 'Bill is the president of the club. He lives in Pittsburgh.'

    print coref_server_response(server_input)
#end if
