import sys, os
from nltk import word_tokenize
from nltk import pos_tag
import common.stanford as stanford
from named_entities import named_entities as ne

#returns a list of features from the question text
def question_features(question_text, pronoun_or_noun = 0, num_ners = 0, subj_length = 0, obj_length = 0):
	features = []

	#find number of tokens in a question
	tokens = word_tokenize(question_text)
	num_tokens = len(tokens)
	features.append(num_tokens)

	what_binary = 0
	if tokens[0].lower() == 'what':
		what_binary = 1
	#end if

	which_binary = 0
	if tokens[0].lower() == 'which':
		which_binary = 1
	#end if

	who_binary = 0
	if tokens[0].lower() == 'who':
		who_binary = 1
	#end if

	#add binary features for wh type questions
	features.extend((what_binary, which_binary, who_binary))

	#add binary feature for pronoun or noun type question
	features.append(pronoun_or_noun)

	#add binary feature for negations
	negation_binary = 0
	for token in tokens:
		tok_lcase = token.lower()
		if tok_lcase in ['no', 'not', 'never'] :
			negation_binary = 1
		#end if
	#end for

	features.append(negation_binary)

	#pos tag counts
	det = 0
	nouns = 0
	verbs = 0
	adj = 0
	prp = 0

	pos_tags = pos_tag(tokens)

	for tag in pos_tags:
		if tag[1].startswith('D'):
			det += 1
		elif tag[1].startswith('N'):
			nouns += 1
		elif tag[1].startswith('V'):
			verbs += 1
		elif tag[1].startswith('J'):
			adj += 1
		elif tag[1].startswith('P'):
			prp += 1
		#end if
	#end for

	features.extend((det, nouns, verbs, adj, prp))

	#add number of NERs as a feature
	features.append(num_ners)

	#lengths of subject and object phrase
	features.extend((subj_length,obj_length))

	return features
#end def

#question_list is [((question_text, type),(subj, verb, obj))]
def question_ranking(question_list):
	features_list = []

	all_questions = []
	for question in question_list:
		all_questions.append(question[0][0].encode('utf-8'))
	#end for

	stanford_ner_output = stanford.ner(all_questions).split('\n')
	ner_len_list = []
	for output in stanford_ner_output:
		ner_len_list.append(len(ne(output)))
	#end for

	ctr = 0
	for question in question_list:
		question_text = question[0][0]
		#question_type = question[0][1]
		question_type = 0

		num_ners = ner_len_list[ctr]
		ctr += 1

		subj_length = len(word_tokenize(question[1][0]))
		obj_length = len(word_tokenize(question[1][2]))

		features_list.append(question_features(question_text,question_type,num_ners,subj_length,obj_length))
	#end for

	return features_list
#end def

def ranked_questions(question_list):
	weight_vector = [0.0433, 0.8499, 0.7612, 2.1735, 0, -0.2381, -0.0154, 0.002, -0.0716, 0.005, 0.0579, 0.032, -0.0102, -0.0245]

	features_list = question_ranking(question_list)
	
	wh_scores = []
	verb_scores = []

	wh_features = []
	verb_features = []

	question_text_list = []
	for question in question_list:
		question_text_list.append(question[0][0])
	#end for

	wh_questions = []
	verb_questions = []

	idx = 0
	for features in features_list:
		if (features[1] == 0 and features[2] == 0 and features[3] == 0):
			verb_features.append(features)
			verb_questions.append(question_text_list[idx])
		else:
			wh_features.append(features)
			wh_questions.append(question_text_list[idx])
		#end if
		idx += 1
	#end for

	for feature_vector in wh_features:
		wh_scores.append(sum([a*b for a,b in zip(weight_vector,feature_vector)]))
	#end for	

	for feature_vector in verb_features:
		verb_scores.append(sum([a*b for a,b in zip(weight_vector,feature_vector)]))
	#end for

	wh_ranked_questions_list = []
	verb_ranked_questions_list = []

	ctr=0
	for question in wh_questions:
		wh_ranked_questions_list.append((question,wh_scores[ctr]))
		ctr += 1
	#end for

	ctr=0
	for question in verb_questions:
		verb_ranked_questions_list.append((question,verb_scores[ctr]))
		ctr += 1
	#end for	

	wh_ranked_questions_list.sort(key=lambda tup: -tup[1])
	verb_ranked_questions_list.sort(key=lambda tup: -tup[1])

	wh_sorted_questions_list = []
	verb_sorted_questions_list = []
	for question in wh_ranked_questions_list:
		wh_sorted_questions_list.append(question[0])
	#end for
	for question in verb_ranked_questions_list:
		verb_sorted_questions_list.append(question[0])
	#end for

	return (wh_sorted_questions_list, verb_sorted_questions_list)
#end def

#unit test
if __name__ == '__main__':
	if(len(sys.argv) < 2):
		sys.stderr.write("correct usage: question_ranking.py <question_text>\n")
		sys.exit(1)
	#end if

	question_text = ' '.join(sys.argv[1:])

	print question_features(question_text)

	a = [(("Who is the President of the United States with Michelle Obama?",1),("Who","is","the President of the United States")), (("Who is the President of the United States with Michelle Obama?",1),("Who","is","the President of the United States")), (("Is Evan typing?",1),("Evan","is","typing"))]
	print ranked_questions(a)
#end if
