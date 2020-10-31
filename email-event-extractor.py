import email, en_core_web_sm, nltk, re, spacy
from collections import Counter


nlp = en_core_web_sm.load()


def extractEventDetails(emailFile):
	msg = email.message_from_file(emailFile)

	subject = msg['Subject']
	print('Subject:', subject)

	contents = msg.get_payload()
	print('Contents:')
	print(contents)

	words = nltk.word_tokenize(contents)
	# print(words)

	doc = nlp(contents)
	print((e.text, e.label_) for e in doc.ents)


if __name__ == '__main__':
	extractEventDetails(open('conf_emails/[GAMESNETWORK] G|A|M|E - Call For Papers N.8 - ‘Would you kindly?’_ Claiming Video Game Agency as Interdisciplinary Concept - DEADLINE 19 Jul 2019 - Ivan Girina <ivan.girina@BRUNEL.AC.UK> - 2019-05-30 0923.eml'))