import csv, eml_parser, nltk, sys
from pyquery import PyQuery
import utility_functions


def extractEventDetails(textContent):
	# Get dates
	dates = utility_functions.get_dates_spacy(textContent)
	if len(dates) == 0:
		print("No dates found")
	for date in dates:
		print(date)

	# Get names
	names = utility_functions.get_names(textContent)
	if len(names) == 0:
		print("No conference chair names found")
	for name in names:
		print('text:', name.text, 'label:', name.label_)


	# Use NLTK to tokenize contents
	# words = nltk.word_tokenize(textContent)
	# print(words)

	# Search for 'Call for Proposals' 'Call for Papers'

	# return {
	# 	'Event Name': '',
	# 	'Notfication Date': '',
	# 	'Conference Date': ''
	# }


def extractEventDetailsFromEmail(emailFile):
	# Parse email
	email = eml_parser.EmlParser(include_raw_body=True).decode_email_bytes(emailFile.read())

	# Email subject
	subject = email['header']['subject']
	print('Subject:', subject)

	# Get plain text from HTML
	htmlContent = email['body'][0]['content']
	return extractEventDetails(htmlContent)

	# pq = PyQuery(htmlContent)
	# textContent = pq('body').text()
	# return extractEventDetails(textContent)

	# textNodes = pq('body').contents().filter(lambda i, node: node.nodeType == 3)
	# print(textNodes)


def extractEventDetailsFromURL(url):
	# Get plain text from HTML
	pq = PyQuery(url=url)
	textContent = pq('body').text()
	return extractEventDetails(textContent)


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
			extractEventDetailsFromEmail(emailFile)
	else:
		testNLPCalendar()
