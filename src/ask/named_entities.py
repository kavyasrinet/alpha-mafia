import sys

#returns 'Barack/PERSON' as ('Barack','PERSON') tuple
def parse_ner(ner_tag):
	tags = ner_tag.split('/')
	return (tags[0],tags[1])
#end def

#returns the chunk of NERs from a line of output (from Stanford NER), as a list of tuples ('word', 'NER class')
def named_entities(ner_text):
	#split into discrete NERs
	ner_tags = ner_text.split()

	#return an empty list if no ner tags
	if not ner_tags:
		return []
	#end if

	#convert NERs to tuples
	ner_tags = map(parse_ner, ner_tags)

	ner_list = []
	current_ner = ''
	current_ner_type = 'O'

	for ner_tag in ner_tags:
		if ner_tag[1] != current_ner_type:
			if current_ner_type != 'O':
				ner_list.append((current_ner,current_ner_type))
			#end if
			current_ner = ner_tag[0]
			current_ner_type = ner_tag[1]
		else:
			if ner_tag[1] != 'O':
				current_ner = current_ner + ' ' + ner_tag[0]
			#end if
		#end if
	#end for

	if current_ner_type != 'O':
		ner_list.append((current_ner,current_ner_type))
	#end if

	return ner_list
#end def

#unit test
if __name__ == '__main__':
	if(len(sys.argv) < 2):
		sys.stderr.write("correct usage: ne.py <Stanford NER output>\n")
		sys.exit(1)
	#end if

	stanford_ner_output = ' '.join(sys.argv[1:])

	print named_entities(stanford_ner_output)
#end if