import nltk
from random import randint
from nltk.tokenize import word_tokenize
from nltk.parse.generate import generate, demo_grammar
from nltk import CFG


def main():
	print("Hello")
	sentence=input('Enter a sentence -->')
	handleInput(sentence)

def knowledgeRep(sentence):
	tokens=word_tokenize(sentence)
	tokens2=nltk.pos_tag(tokens)
	subject = ""
	verb = ""
	obj = ""
	foundSub = False
	lookingForComma = False

	for word in tokens2:
		if lookingForComma:
			if word[1] == ",":
				lookingForComma = False
			continue
		if (word[1] == "TO" or word[1] == "IN") and "," in sentence:
			lookingForComma = True
			continue
		if word[1] == "NN" or word[1] == "NNS" or word[1] == "NNP" or word[1] == "NNPS" or word[1] == "PRP":
			if foundSub:
				obj = word[0]
			else:
				subject = word[0]
				foundSub = True

		if word[1] == "VB" or word[1] == "VBG" or word[1] == "VBD" or word[1] == "VBN" or word[1] == "VBP" or word[1] == "VBZ":
			verb = word[0]

	print("subject: " + subject)
	print("verb: " + verb)
	print("object: " + obj)

	tempList = data[subject][verb]
	if subject == "I":
		sentence = "You " + verb + ' '.join(tempList)
		return sentence
	else:
		sentence = subject + verb + ' '.join(tempList)
		return sentence



#Not really AI
#keyVerb is just the main verb
#keyPhrase is the first word (who, what, where etc.)
def respondSentence(sentence):
	grammar = ""
	sentence = sentence.lower()
	location_keys = ["live", "reside", "stay", "where are"]
	name_keys = ["called", "who are"]
	knowledge_rep = "What" #not done

	if any(word in sentence for word in location_keys):
		responses = ["I live in the Internet.", "I live in a mansion.", "In Bermuda."]
		num = randint(0, len(responses)-1)
		print(responses[num])
	elif any(word in sentence for word in name_keys):
		responses = ["My name is FriendBot!", "Some call me FriendBot.", "I am Friendbot."]
		num = randint(0, len(responses)-1)
		print(responses[num])
	else:
		print("I don't want to answer that. Tell me more about yourself.")




def respondQuestion(sentence, keyWord, POS, dataMap):
	sentence = sentence.lower();
	if "tell me" not in sentence:
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
	else:
		knowledgeRep(sentence)





		


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
		respondQuestion(sentence, "cats", "NNS", {})
	elif sentType == 2:
		print("question")
		respondSentence(sentence)

if __name__ == "__main__":
    main()