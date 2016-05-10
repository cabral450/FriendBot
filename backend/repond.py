import nltk
from random import randint
from nltk.tokenize import word_tokenize
from nltk.parse.generate import generate, demo_grammar
from nltk import CFG


def main():
	print("Hello")
	sentence=input('Enter a sentence -->')
	handleInput(sentence)


def respond(keyWord, verb, POS):
	grammar = ""

	if POS == "NNPS" or POS == "NNS":
		grammar = CFG.fromstring("""
		S -> H-NP1 Adj VP'?' | Wh-NP VP'?'
		H-NP1 -> 'How'
		Wh-NP -> 'Who' | 'What' | 'When' | 'Where' | 'What'
		Adj -> 'big' | 'small' | 'happy' | 'sad'
		NP -> Pronoun | Proper-Noun 
		Pronoun -> 'they' | 'those'
		Proper-Noun -> '<>'
		Noun -> '<>'
		VP -> Verb NP  
		Verb -> 'are' 
		""")
	elif POS == "NN" or "NNP":
		grammar = CFG.fromstring("""
		S -> H-NP1 Adj VP'?' | Wh-NP VP'?'
		H-NP1 -> 'How'
		Wh-NP -> 'Who' | 'What' | 'When' | 'Where' | 'What'
		Adj -> 'big' | 'small' | 'happy' | 'sad'
		NP -> Pronoun | Proper-Noun 
		Pronoun -> 'it' | 'that'
		Proper-Noun -> '<>'
		Noun -> '<>'
		VP -> Verb NP  
		Verb -> 'is' 
		""")

	rand_sent_list = []
	for sentence in generate(grammar):
	    rand_sent_list.append(' '.join(sentence))

	num = randint(0, len(rand_sent_list)-1)
	response = rand_sent_list[num]
	print(response)
	


def handleInput(input):
	sentence=input
	tokens=word_tokenize(sentence)
	tokens2=nltk.pos_tag(tokens)
	print(tokens2)
	text = nltk.Text(tokens)
	print(text)

	sentType=1 #statement/declarative/imperative/exclamatory
	if "?" in tokens:
		sentType=2 #question/interrogative

	if sentType == 1:
		print("statement")
		respond("cats", "NNS")
	elif sentType == 2:
		print("question")

if __name__ == "__main__":
    main()