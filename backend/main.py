import nltk
from nltk.tokenize import word_tokenize
from nltk.parse.generate import generate, demo_grammar
from nltk import CFG
import re, string
import parser

#list in a map in a map
#Ex: {'I': {'shot': ['elephant']}}
data={}

def main():
	print "Hello"
	#loop while not command \q
	running=True
	while running:
		#get the sentence
		sentence=raw_input("Respond -->")
		if sentence == "\\q":
			print "Goodbye"
			running=False
		else:
			handleInput(sentence)

def addData(parent, foundNP, foundVP, foundOBJ, NP, VP, OBJ):

	for node in parent:

		if type(node) is nltk.Tree:
			if node.label() == "NP" and parent.label() == "S":
				NP=node.leaves()
				foundNP=True
			elif node.label() == "VP" and parent.label() == "S":
				VP=node.leaves()
				foundVP=True
			elif node.label() == "NP" and (parent.label() == "VP"):
				OBJ=node.leaves()
				foundOBJ=True

			#found what we were looking for
			if foundNP and foundVP and foundOBJ:
				#sentence data
				subject=NP[0]
				verb=VP[0]
				obj=OBJ[1]

				#check if we have any data/add it
				if data.has_key(subject):
					if data[subject].has_key(verb):
						#add it to the list if it isnt already
						if obj not in data[subject][verb]:
							data[subject][verb].append(obj)

					#no verb in the subject map, make a new one
					else:
						subCategory=dict()
						subCategory[verb]=list()
						subCategory[verb].append(obj)
						data[subject]=subCategory
				#no subject, make a new one
				else:
					subCategory=dict()
					subCategory[verb]=list()
					subCategory[verb].append(obj)
					data[subject]=subCategory

				break

			addData(node, foundNP, foundVP, foundOBJ, NP, VP, OBJ)
		else:
			continue

def getData(parent, foundNP, foundVP, NP, VP):
#n = noun to look for
#v = verb to look for
	for node in parent:

		if type(node) is nltk.Tree:
			if node.label() == "NP" and parent.label() == "S":
				NP=node.leaves()
				foundNP=True
			elif node.label() == "VP" and parent.label() == "S":
				VP=node.leaves()
				foundVP=True

			#found what we were looking for
			if foundNP and foundVP:
				#sentence data
				subject=NP[0]
				verb=VP[0]

				#check if we have any data/add it
				if data.has_key(subject):
					if data[subject].has_key(verb):
						return data[subject][verb]

					#no verb in the subject map, failed
					else:
						return ""
				#no subject, failed
				else:
					return ""

				break

			getData(node, foundNP, foundVP, NP, VP)
		else:
			continue

	return ""
	

def handleInput(input):
	
	#it knows its running
	#"I am running" grammar function call when that exists
	#addData(parent, foundNP, foundVP, foundOBJ, NP, VP, OBJ)

	sentence=input
	tokens=word_tokenize(sentence)
	tokens2=nltk.pos_tag(tokens)

#=====================================
#temporary grammar but eventually sentence broken down into a grammar
	nouns = ""
	verbs = ""
	preps = ""
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
			if preps == "": #if preps is empty
				preps = "'"+word[0]+"'"
			else: #preps isnt empty
				preps = preps + " | '" + word[0] + "'"
			lookingForComma = True
			continue
		if word[1] == "NN" or word[1] == "NNP" or word[1] == "NNPS" or word[1] == "NNS" or word[1] == "PRP":
			if foundSub:
				obj = word[0]
			else:
				subject = word[0]
				foundSub = True
			if nouns == "": #if nouns is empty
				nouns = "'"+word[0]+"'"
			else: #nouns isnt empty
				nouns = nouns + " | '" + word[0] + "'"
		if word[1] == "VB" or word[1] == "VBG" or word[1] == "VBD" or word[1] == "VBN" or word[1] == "VBP" or word[1] == "VBZ":
			verb = word[0]
			if verbs == "": #if verbs is empty
				verbs = "'"+word[0]+"'"
			else: #verbs isnt empty
				verbs = verbs + " | '" + word[0] + "'"
		if word[1] == ""
	#how should i handle Det and P?
	grammarString = """
	S -> NP VP
	PP -> P NP
	NP -> Det N | Det N PP | '""" + nouns + """'
	VP -> V NP | VP PP
	Det -> 'all' | 'an' | 'another' | 'any' | 'both' | 'del' | 'each' | 'either' | 'every' | 'half' | 'la' | 'many' | 'much' | 'nary' | 'neither' | 'no' | 'some' | 'such' | 'that' | 'the' | 'them' | 'these' | 'this' | 'those'
	N ->  | '""" + nouns + """'
	V -> """ + verbs + """
	P -> """ + preps
	
	grammar = nltk.CFG.fromstring(grammarString)


	#grammar = nltk.CFG.fromstring("""
	#S -> NP VP
	#PP -> P NP
	#NP -> Det N | Det N PP | 'I'
	#VP -> V NP | VP PP
	#Det -> 'an' | 'my'
	#N -> 'elephant' | 'pajamas'
	#V -> 'shot'
	#P -> 'in'
	#""")
	parser = nltk.ChartParser(grammar)

	regex=re.compile('[^a-zA-Z]')
	tempSentence=regex.sub(' ', sentence)
	sent=tempSentence.split()


#=====================================
#make all possible sentences from a grammar, make it a function

	#for sentence in generate(grammar, n=10):
	#	print(' '.join(sentence))

#======================================
#question or statement and handle it

	sentType=1 #statement/declarative/imperative/exclamatory
	if "?" in tokens:
		sentType=2 #question/interrogative
		
	#statement
	if sentType == 1:
		#get trees
		print "HERE1"
		for tree in parser.parse(sent):
			print "LOOP"
			print tree
			addData(tree, False, False, False, 0, 0, 0)
			print data
			print
		print "HERE2"

	#question
	elif sentType == 2:
		#get trees
		for tree in parser.parse(sent):
			print tree
			knowledge=getData(tree, False, False, 0, 0)
			print knowledge
			print

if __name__ == "__main__":
    main()
