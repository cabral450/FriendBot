import nltk
from random import randint
from nltk.tokenize import word_tokenize
from nltk.parse.generate import generate, demo_grammar
from nltk import CFG


def main():
	print("Hello")
	sentence=input('Enter a sentence -->')
	handleInput(sentence)

def respondSentence(keyWord):
	grammar = ""


def respondQuestion(keyWord, verb, POS):
	grammar = ""

	if POS == "NNPS" or POS == "NNS":
		grammar = CFG.fromstring("""
		S -> H-NP1 Adj VP'?' | Wh-NP VP'?'
		H-NP1 -> 'How'
		Wh-NP -> 'Who' | 'What' | 'Where' | 'What'
		Adj -> 'big' | 'small' | 'happy' | 'sad'
		NP -> Pronoun | Proper-Noun | Noun
		Pronoun -> 'they' | 'those'
		Proper-Noun -> '[]'
		Noun -> 'the <>'
		VP -> Verb NP  
		Verb -> 'are' 
		""")
	elif POS == "NN" or "NNP":
		grammar = CFG.fromstring("""
		S -> H-NP1 Adj VP'?' | Wh-NP VP'?'
		H-NP1 -> 'How'
		Wh-NP -> 'Who' | 'What' | 'Where' | 'What'
		Adj -> 'big' | 'small' | 'happy' | 'sad'
		NP -> Pronoun | Proper-Noun | Noun
		Pronoun -> 'it' | 'that'
		Proper-Noun -> '[]'
		Noun -> 'the <>'
		VP -> Verb NP  
		Verb -> 'is' 
		""")

	rand_sent_list = []
	for sentence in generate(grammar):
	    rand_sent_list.append(' '.join(sentence))
	while True:
		num = randint(0, len(rand_sent_list)-1)
		response = rand_sent_list[num]
		if "<>" in response and (POS == "NNS" or POS == "NN"):
			index = response.index("<>")
			response = response[:index] + keyWord + response[index+2:]
			break
		if "[]" in response and (POS == "NNPS" or POS == "NNP"):
			index = response.index("[]")
			response = response[:index] + keyWord + response[index+2:]
			break
		if "<>" not in response and "[]" not in response:
			break
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
		respondQuestion("cats", "n/a", "NNS")
	elif sentType == 2:
		print("question")

if __name__ == "__main__":
    main()