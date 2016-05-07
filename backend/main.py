import nltk
from nltk.tokenize import word_tokenize
from nltk.parse.generate import generate, demo_grammar
from nltk import CFG

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
			handleInput("I shot an elephant in my pajamas.")#sentence

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

	grammar = nltk.CFG.fromstring("""
	S -> NP VP
	PP -> P NP
	NP -> Det N | Det N PP | 'I'
	VP -> V NP | VP PP
	Det -> 'an' | 'my'
	N -> 'elephant' | 'pajamas'
	V -> 'shot'
	P -> 'in'
	""")
	sent=['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']
	parser = nltk.ChartParser(grammar)

#=====================================
#make all possible sentences from a grammar, make it a function

	#grammar = nltk.CFG.fromstring(demo_grammar)
	#print grammar
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
		for tree in parser.parse(sent):
			print tree
			addData(tree, False, False, False, 0, 0, 0)
			print data
			print

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