import email
import en_core_web_sm
import nltk

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
	extractEventDetails(open('conf_emails/1.eml'))