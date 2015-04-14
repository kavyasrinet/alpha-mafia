import xml.etree.ElementTree as ET
import requests
import sys
import re

pronouns = ['he','she','it', 'they']
SERVER_PORT='8125'
SERVER_ADDRESS='http://localhost:%s/BARTDemo/ShowText/process/' % SERVER_PORT


def coref_map_gen(root):
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

def coref_list(dom, coref_map):
    temp = []
    for item in dom:
        if item.tag == 'w':
            temp.append(item.text)
        if item.tag == 'coref':
            temp.extend(coref_list(item ,coref_map))
    map_id = item.get('set_id')
    if map_id not in coref_map:
        return temp
    coref = coref_map[map_id]
    print "CONFLICT"
    print temp
    print coref[0]
    if len(text) ==  1 and text[0].lower() in pronouns:
        return coref[0]
    return temp

def create_document(root, coref_map):
    sentences = []
    for sen in root:
        document = []
        for item in sen:
            if item.tag == 'w':
                document.append(item.text)
            elif item.tag == 'coref':
                document.extend(coref_list(item, coref_map))
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

def formatting(output_list):
   out_string = ' '.join(output_list)
   no_newline = out_string.replace('\n',' ')
   sing_space = re.sub(r'(\s+)',r' ', no_newline)
   punc_fixed = re.sub(r'\s([\.\,\?\!\:])',r'\g<1>', sing_space)
   return punc_fixed

def get_resolved_sentence(context):
    resp = coref_server_request(' '.join(context))
    if not resp: return context[-1]
    root = None
    try:
        root = ET.fromstring(resp)
    except:
        return context[-1]
    coref_map, sentences = coref_map_gen(root)
    if sentences != len(context):
        #we disagree on the number of sentences
        return context[-1]
    doc = create_document(root, coref_map)
    return formatting(doc[-1])

 #unit test
if __name__ == '__main__':
    if(len(sys.argv) != 2):
        sys.stderr.write('Correct Usage: python coref.py <inputFilePath>\n')
        sys.exit(1)
        #end if

    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    print coref_map_gen(root)
    server_input = 'Bill is the president of the club. He lives in Pittsburgh.'

    print coref_server_response(server_input)
#end if
