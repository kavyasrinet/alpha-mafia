import xml.etree.ElementTree as ET
import sys

def coref_list(root):
	coref_sets = {}

	for sen in root:
		for item in sen:
			if item.tag == 'coref':
				set_id = item.get('set-id')
				
				if set_id not in coref_sets:
					coref_sets[set_id] = (None,None)
				#end if

				curr_coref = []
				for w in item:
					curr_coref.append(w.text)
				#end for

				if coref_sets[set_id][0] is None:
					coref_sets[set_id] = (curr_coref, [curr_coref])
				else:
					coref_sets[set_id][1].append(curr_coref)
				#end if
			#end if
		#end for
	#end for

	return coref_sets
#end def

#unit test
if __name__ == '__main__':
	if(len(sys.argv) != 2):
		sys.stderr.write('Correct Usage: python coref.py <inputFilePath>\n')
		sys.exit(1)
	#end if

	#f = open(sys.argv[1], 'r')
	#xml_text = f.read()

	tree = ET.parse(sys.argv[1])
	root = tree.getroot()

	print coref_list(root)
#end if