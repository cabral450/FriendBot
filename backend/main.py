import nltk
from random import randint
from nltk.tokenize import word_tokenize
from nltk.parse.generate import generate, demo_grammar
from nltk import CFG
import re, string
import parser
nltk.grammar._STANDARD_NONTERM_RE = re.compile('( [\w/][\w$/^<>-]* ) \s*', re.VERBOSE)

class stack(list):
	def __init__(self, x):
		self.x=x
	def push(self, item):
		self.append(item)
	def isEmpty(self):
		return not self

#list in a map in a map
#Ex: {'I': {'shot': ['elephant']}}
data={}
queuedTopics = stack([])
allTopics = stack([])
topicsDic = {}

def main():
	return "Hello"
	#loop while not command \q
	running=True
	while running:
		#get the sentence
		sentence=raw_input("Respond -->")
		if sentence == "\\q":
			return "Goodbye"
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
				if len(OBJ) == 0:
					continue
				subject=NP[0]
				verb=VP[0]
				obj=OBJ[0]

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

	if data.has_key(subject):
		if data[subject].has_key(verb):
			tempList = data[subject][verb]
			if subject.lower() == "i":
				sentence = "You " + verb + " " + tempList[0]
				for x in range(1,len(tempList)-1):
					sentence = sentence + ", " + tempList[x]
				sentence = sentence + ", and " + tempList[len(tempList)-1]
				return sentence
			elif subject.lower() == "you":
				sentence = "I " + verb + " " + tempList[0]
				for x in range(1, len(tempList)-1):
					sentence = sentence + ", " + tempList[x]
				sentence = sentence + ", and " + tempList[len(tempList)-1]
				return sentence
			else:
				sentence = subject + verb + " " + ' '.join(tempList)
				return sentence
		else:
			return("I don't want to talk about about that. Let's talk about something else.")
	else:
		return("I don't want to talk about about that. Let's talk about something else.")



#Not really AI
#keyVerb is just the main verb
#keyPhrase is the first word (who, what, where etc.)
def respondSentence(sentence):
	grammar = ""
	location_keys = ["live", "reside", "stay", "where are"]
	name_keys = ["called", "who are"]
	knowledge_rep = "What" #not done

	if any(word in sentence for word in location_keys) and "you" in sentence:
		responses = ["I live in the Internet.", "I live in a mansion.", "In Bermuda."]
		num = randint(0, len(responses)-1)
		return(responses[num])
	elif any(word in sentence for word in name_keys) and "you" in sentence:
		responses = ["My name is FriendBot!", "Some call me FriendBot.", "I am Friendbot."]
		num = randint(0, len(responses)-1)
		return(responses[num])
	else:
		knowledgeRep(sentence)




def respondQuestion(sentence, keyWord, POS):
	if "Tell me" not in sentence:
		grammar = ""

		if POS == "NNPS" or POS == "NNS":
			grammar = CFG.fromstring("""
			S -> H-NP1 Adj VP'?' | Wh-NP VP'?'
			H-NP1 -> 'How'
			Wh-NP -> 'Who' | 'What' | 'Where' | 'What'
			Adj -> 'big' | 'small' | 'happy' | 'sad' | 'large' | 'difficult' | 'emotional' | 'old' | 'healthy' | 'strong' | 'cute' | 'hungry'
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
			Adj -> 'big' | 'small' | 'happy' | 'sad' | 'large' | 'difficult' | 'emotional' | 'old' | 'healthy' | 'strong' | 'cute' | 'hungry'
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
		return(response)
	else:
		knowledgeRep(sentence)

def handleInput(input):
	
	#it knows its running
	#"I am running" grammar function call when that exists
	#addData(parent, foundNP, foundVP, foundOBJ, NP, VP, OBJ)

	sentence=input
	tokens=word_tokenize(sentence)
	tokens2=nltk.pos_tag(tokens)

	#priority queue
	for taggedWord in tokens2:
		#if topic hasn't already been brought up, and it is a noun
		if taggedWord[0] not in allTopics and (taggedWord[1] == "NN" or taggedWord[1] == "NNP" or taggedWord[1] == "NNPS" or taggedWord[1] == "NNS"):
			#push word to topics queue, list of all topics, and topics dictionary
			queuedTopics.push(taggedWord[0])
			allTopics.push(taggedWord[0])
			topicsDic[taggedWord[0]] = taggedWord[1]

#=====================================
#temporary grammar but eventually sentence broken down into a grammar

	nouns = ""
	verbs = ""
	preps = ""
	wdts = ""
	wps = ""
	wrbs = ""

	dets = ""
	rbs = ""
	rbrs = ""
	rbss = ""
	rps = ""
	prps = ""
	pdts = ""
	mds = ""
	jjs = ""
	jjrs = ""
	jjss = ""
	exs = ""
	ccs = ""
	prpds = ""
	wpds = ""



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

		if word[1] == "DT":
			if dets == "": #if dets is empty
				dets = "'"+word[0]+"'"
			else: #dets isnt empty
				dets = dets + " | '" + word[0] + "'"
		if word[1] == "RB":
			if rbs == "": #if rbs is empty
				rbs = "'"+word[0]+"'"
			else: #rbs isnt empty
				rbs = rbs + " | '" + word[0] + "'"
		if word[1] == "RBR":
			if rbrs == "": #if rbrs is empty
				rbrs = "'"+word[0]+"'"
			else: #rbrs isnt empty
				rbrs = rbrs + " | '" + word[0] + "'"
		if word[1] == "RBS":
			if rbss == "": #if rbss is empty
				rbss = "'"+word[0]+"'"
			else: #rbss isnt empty
				rbss = rbss + " | '" + word[0] + "'"
		if word[1] == "RP":
			if rps == "": #if rps is empty
				rps = "'"+word[0]+"'"
			else: #rps isnt empty
				rps = rps + " | '" + word[0] + "'"
		if word[1] == "PRP":
			if prps == "": #if prps is empty
				prps = "'"+word[0]+"'"
			else: #prps isnt empty
				prps = prps + " | '" + word[0] + "'"
		if word[1] == "PDT":
			if pdts == "": #if pdts is empty
				pdts = "'"+word[0]+"'"
			else: #pdts isnt empty
				pdts = pdts + " | '" + word[0] + "'"
		if word[1] == "MD":
			if mds == "": #if mds is empty
				mds = "'"+word[0]+"'"
			else: #mds isnt empty
				mds = mds + " | '" + word[0] + "'"				
		if word[1] == "JJ":
			if jjs == "": #if jjs is empty
				jjs = "'"+word[0]+"'"
			else: #jjs isnt empty
				jjs = jjs + " | '" + word[0] + "'"
		if word[1] == "JJR":
			if jjrs == "": #if jjrs is empty
				jjrs = "'"+word[0]+"'"
			else: #jjrs isnt empty
				jjrs = jjrs + " | '" + word[0] + "'"
		if word[1] == "JJS":
			if jjss == "": #if jjss is empty
				jjss = "'"+word[0]+"'"
			else: #jjss isnt empty
				jjss = jjss + " | '" + word[0] + "'"
		if word[1] == "EX":
			if exs == "": #if exs is empty
				exs = "'"+word[0]+"'"
			else: #exs isnt empty
				exs = exs + " | '" + word[0] + "'"
		if word[1] == "CC":
			if ccs == "": #if ccs is empty
				ccs = "'"+word[0]+"'"
			else: #ccs isnt empty
				ccs = ccs + " | '" + word[0] + "'"

		if word[1] == "PRP$":
			if prpds == "": #if prpds is empty
				prpds = "'"+word[0]+"'"
			else: #prpds isnt empty
				prpds = prpds + " | '" + word[0] + "'"
		if word[1] == "WP$":
			if wpds == "": #if wpds is empty
				wpds = "'"+word[0]+"'"
			else: #wpds isnt empty
				wpds = wpds + " | '" + word[0] + "'"
		if word[1] == "WDT":
			if wdts == "": #if wdts is empty
				wdts = "'"+word[0]+"'"
			else: #wdts isnt empty
				wdts = wdts + " | '" + word[0] + "'"
		if word[1] == "WP":
			if wps == "": #if wps is empty
				wps = "'"+word[0]+"'"
			else: #wps isnt empty
				wps = wps + " | '" + word[0] + "'"
		if word[1] == "WRB":
			if wrbs == "": #if wrbs is empty
				wrbs = "'"+word[0]+"'"
			else: #wrbs isnt empty
				wrbs = wrbs + " | '" + word[0] + "'"
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

	grammarString = """
	S -> NP VP
	PP -> P NP
	NP -> Det N | Det N PP | """ + nouns + """
	VP -> V NP | VP PP
	Det -> """ + dets + """
	N ->  | """ + nouns + """
	V -> """ + verbs + """
	P -> """ + preps + """
	WRB -> """ + wrbs + """
	WP -> """ + wps + """
	WDT -> """ + wdts + """
	RB -> """ + rbs + """
	RBR -> """ + rbrs + """
	RBS -> """ + rbss + """
	RP -> """ + rps + """
	PRP -> """ + prps + """
	PDT -> """ + pdts + """
	MD -> """ + mds + """
	JJ -> """ + jjs + """
	JJR -> """ + jjrs + """
	JJS -> """ + jjss + """
	EX -> """ + exs + """
	CC -> """ + ccs + """
	PRP$ -> """ + prpds + """
	WP$ -> """ + wpds
	
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
		for tree in parser.parse(sent):
			#print tree
			addData(tree, False, False, False, 0, 0, 0)
			#print data
		if len(queuedTopics) > 0:
			topic = queuedTopics.pop()
			return respondQuestion(sentence, topic, topicsDic[topic])
		else:
			return "Tell me other cool facts about yourself."

	#question
	elif sentType == 2:
		#get trees
		for tree in parser.parse(sent):
			#print tree
			knowledge=getData(tree, False, False, 0, 0)
			#print knowledge
		return respondSentence(sentence)

if __name__ == "__main__":
    main()
