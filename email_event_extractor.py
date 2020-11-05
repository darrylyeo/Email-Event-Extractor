import eml_parser, en_core_web_sm, nltk, re, spacy, sys
from collections import Counter
from pyquery import PyQuery

nlp = en_core_web_sm.load()

def extractEventDetails(emailFile):
	# Parse email
	email = eml_parser.EmlParser(include_raw_body=True).decode_email_bytes(emailFile.read())

	# Email subject
	subject = email['header']['subject']
	print('Subject:', subject)

	# Email body
	for body in email['body']:
		# Parse HTML
		html = body['content']
		pq = PyQuery(html)
		
		# Get plain text from HTML
		textContent = pq('body').text()
		print(textContent)
		# textNodes = pq('body').contents().filter(lambda i, node: node.nodeType == 3)
		# print(textNodes)

		# Use Spacy to find entities
		doc = nlp(textContent)
		print([(e.text, e.label_) for e in doc.ents])

		# Use NLTK to tokenize contents
		# words = nltk.word_tokenize(textContent)
		# print(words)



if __name__ == '__main__':
	fileName = sys.argv[1]
	with open(fileName, 'rb') as emailFile:
		extractEventDetails(emailFile)