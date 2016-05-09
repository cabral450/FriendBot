import nltk
from nltk.tokenize import word_tokenize
from nltk.parse.generate import generate, demo_grammar
from nltk import CFG
import dependencies
import parser
import standoff

class stack(list):
    def push(self, item):
        self.append(item)
    def isEmpty(self):
        return not self

def main():
	#print "Hello"
	sentence=input("Enter a sentence -->")
	handleInput(sentence)

	#grammar = CFG.fromstring(demo_grammar)
	#print demo_grammar
	#for sentence in generate(grammar, n=10):
	#	print(' '.join(sentence))
	

def handleInput(input):
	sentence=input
	tokens=word_tokenize(sentence)
	tagged_tokens=nltk.pos_tag(tokens)
	#text = nltk.Text(tokens)
	#print text

	queuedTopics = []
	pastTopics = []
	topicsDic = {}

	for taggedWord in tagged_tokens:
		#if topic hasn't already been brought up, and it is a noun
		if taggedWord[0] not in allTopics and (taggedWord[1] == "NN" or taggedWord[1] == "NNP" or taggedWord[1] == "NNPS" or taggedWord[1] == "NNS" or taggedWord[1] == "PRP" or taggedWord[1] == "PRP$"):
			#push word to topics queue, list of all topics, and topics dictionary
			queuedTopics.push(taggedWord[0])
			allTopics.push(taggedWord[0])
			topicsDic[taggedWord[0]] = taggedWord[1]



	#parsed = parser.parse(sentence)
	#print(parsed)


	sentType=1 #statement/declarative/imperative/exclamatory
	if "?" in tokens:
		sentType=2 #question/interrogative

	#if sentType == 1:
	#	print "statement"
	#elif sentType == 2:
	#	print "question"

if __name__ == "__main__":
    main()



def treeToCFG(tree):
	t=tree