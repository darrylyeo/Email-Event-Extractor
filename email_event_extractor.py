import eml_parser, en_core_web_sm, nltk, re, spacy, sys
from collections import Counter
from pyquery import PyQuery

nlp = en_core_web_sm.load()

def extractEventDetails(emailFile):
	email = eml_parser.EmlParser(include_raw_body=True).decode_email_bytes(emailFile.read())

	for body in email['body']:
		html = body['content']
		pq = PyQuery(html)

		textContent = pq('body').text()
		print(textContent)

		# textNodes = pq('body').contents().filter(lambda i, node: node.nodeType == 3)
		# print(textNodes)

	# subject = msg['Subject']
	# print('Subject:', subject)

	# contents = [
	# 	base64.b64decode(part.get_payload())
	# 	for part in msg.walk()
	# 	if part.get_content_type() == 'text/plain'
	# ]
	# print(dir(msg))
	# contents = msg.get_body(preferencelist=('related', 'html', 'plain')).get_content()
	# print('Contents:')
	# print(contents)

	# words = nltk.word_tokenize(contents)
	# print(words)

	# doc = nlp(contents)
	# print([(e.text, e.label_) for e in doc.ents])


if __name__ == '__main__':
	fileName = sys.argv[1]
	with open(fileName, 'rb') as emailFile:
		extractEventDetails(emailFile)