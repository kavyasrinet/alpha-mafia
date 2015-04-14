import nltk
from nltk.corpus import wordnet as wn
import sys
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')

topics = ['person','city','language','constellation','musical_instrument','time_period']
general_topics = ['whole','location','plant','animal','matter','thing','process','abstraction']

#returns one of the above topics or an empty string
def object_class(word):
    #wordnet needs '_' instead of spaces
    word = word.replace(' ','_')

    #obtain all synsets
    word = word.encode('utf-8')
    word_synsets = wn.synsets(word)

    if(word_synsets):
        first_synset = word_synsets[0]
        synset_pos = first_synset.pos()

        if(synset_pos == 'n'):
            first_hypernym_path = first_synset.hypernym_paths()[0]

            #search for specific topics
            for synset_entry in first_hypernym_path:
                class_name = synset_entry.name().split('.')[0]
                if class_name in topics:
                    return class_name
                #end if
            #end for

            #search for general_topics
            for synset_entry in first_hypernym_path:
                class_name = synset_entry.name().split('.')[0]
                if class_name in general_topics:
                    return class_name
                #end if
            #end for
        #end if
    #end if

    return ''
#end def

#question word mappings
question_words = {}

#specific topics
question_words['person'] = 'Who'
question_words['time_period'] = 'When'
question_words['city'] = 'Which'
question_words['language'] = 'Which'
question_words['constellation'] = 'Which'
question_words['musical_instrument'] = 'Which'

#general_topics
question_words['whole'] = 'What'
question_words['location'] = 'Which'
question_words['plant'] = 'Which'
question_words['animal'] = 'Which'
question_words['matter'] = 'What'
question_words['thing'] = 'What'
question_words['process'] = 'What'
question_words['abstraction'] = 'What'

#returns question word and category as a tuple (i.e. 2 return outputs)
def question_word(word):
    word_class = object_class(word)

    if word_class in question_words:
        return (question_words[word_class], word_class)
    #end if

    return ('','')
#end def

#returns a list of triples from the subject [(subject_part, question_word, word_class)]
def subject_supersense(subject_text):
    supersense_list = []

    words = subject_text.split()
    num_words = len(words)
    subsets = []

    #obtain different subsets of the subject
    for i in range(1,num_words+1):
        for j in range(num_words-i+1):
            subsets.append('_'.join(words[j:j+i]))
        #end for
    #end for

    for subset in subsets:
        qw = question_word(subset)
        if qw[0]:
            supersense_list.append((subset.replace('_',' '), qw[0], qw[1]))
        #end if
    #end for

    return supersense_list
#end def

#unit test
if __name__ == '__main__':
    if(len(sys.argv) < 2):
        sys.stderr.write("correct usage: wn.py <word/phrase>\n")
        sys.exit(1)
    #end if

    word = ' '.join(sys.argv[1:])

    for w in sys.argv[1:]:
        if question_word(w):
            print w + ": " + question_word(w)[0] + " " + question_word(w)[1]
        #end if
    #end for

    if question_word(word):
        print word + ": " + question_word(word)[0] + " " + question_word(word)[1]
    #end if

    print subject_supersense(word)
#end if
