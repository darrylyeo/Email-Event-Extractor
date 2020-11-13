import csv, eml_parser, en_core_web_sm, nltk, re, spacy, sys
from collections import Counter
from pyquery import PyQuery

nlp = en_core_web_sm.load()


def extractEventDetails(pq):
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

	# Search for 'Call for Proposals' 'Call for Papers'

	return {
		'Event Name': '',
		'Notfication Date': '',
		'Conference Date': ''
	}


def extractEventDetailsFromEmail(emailFile):
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
		return extractEventDetails(pq)


def extractEventDetailsFromURL(url):
	pq = PyQuery(url=url)
	return extractEventDetails(pq)


def testNLPCalendar():
	with open('rochester-nlp-calendar.tsv', newline='') as file:
		nlpCalendar = csv.reader(file, delimiter='\t')

		header = next(nlpCalendar)
		events = [
			{header[i]: value for i, value in enumerate(event)}
			for event in nlpCalendar
		]

		# Test all events
		for event in [events[1]]: # for event in events:
			extractEventDetailsFromURL(event['Link'])
			event = event[0]
			details = extractEventDetailsFromURL(event['Link'])

			# Compare
			print(details['Notfication Date'], event['Notification'])
			print(details['Conference Date'], event['Conference'])


if __name__ == '__main__':
	if len(sys.argv) == 2:
		fileName = sys.argv[1]
		with open(fileName, 'rb') as emailFile:
			extractEventDetails(emailFile)
	else:
		testNLPCalendar()