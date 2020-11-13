# Email-Event-Extractor

## Install Dependencies
```
pip3 install eml_parser, nltk, pyquery, spacy
```

## Usage

Extract details from a .eml file:
```
python3 email_event_extractor.py conf_emails/1.eml
```

Test with webpages listed on Rochester University's NLP Calendar:
```
python3 email_event_extractor.py
```