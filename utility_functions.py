import re
import sys
import spacy
from itertools import *
from spacy.attrs import ENT_IOB
from spacy.matcher import Matcher


def fix_space_tags(doc):
    ent_iobs = doc.to_array([ENT_IOB])
    for i, token in enumerate(doc):
        if token.is_space:
            # Sets 'O' tag (0 is None, so I is 1, O is 2)
            ent_iobs[i] = 2
    doc.from_array([ENT_IOB], ent_iobs.reshape((len(doc), 1)))
    return doc


def get_dates_spacy(email):
    dates = []
    labels = []
    solo_dates = []

    nlp = spacy.load('en_core_web_md')
    nlp.add_pipe(fix_space_tags, name='fix-ner', before='ner')
    doc = nlp(email)

    matcher = Matcher(nlp.vocab)
    pattern = [{"IS_ALPHA": True},
               {"IS_SPACE": True, "OP": "*"},
               {"IS_PUNCT": True},
               {"IS_SPACE": True, "OP": "*"},
               {"ENT_TYPE": "DATE", "OP": "+"}]
    matcher.add("DATE_PATTERN", None, pattern)
    matched = matcher(doc)
    results = [max(list(group), key=lambda x: x[2]) for key, group in groupby(matched, lambda prop: prop[1])]
    for match_id, start, end in results:
        matched_span = doc[start:end]
        dates.append(matched_span)

    for date in dates:
        s_token = date.start
        s_char = date.start_char
        text = doc.text
        for i in range(len(text)):
            if text[s_char-1] == '\n' or text[s_char-1] == '\t':
                break
            s_char -= 1

        for i in range(len(doc)):
            if doc[s_token - 1].idx < s_char:
                break
            s_token -= 1

        labels.append(doc[s_token:date.start+1])

    for date in dates:
        start_token = date.start
        for i in range(len(doc)):
            if doc[start_token].ent_type_ == 'DATE':
                break
            start_token += 1

        solo_dates.append(doc[start_token:date.end])

    return [(labels[i], solo_dates[i]) for i in range(len(dates))]


def get_dates_regexp(email):
    date_pattern = r'((0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d)|' \
                   r'((0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d)'
    # mmdd_pattern = r'^(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d$'
    # ddmm_pattern = r'^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$'
    return [x for x in re.finditer(date_pattern, email)]


if __name__ == '__main__':
    filename = sys.argv[1]
    f = open(filename)
    raw = f.read()

    dates_regexp = get_dates_regexp(raw)
    dates_spacy = get_dates_spacy(raw)
    print('returns')
    for date_out in dates_spacy:
        print(date_out.text)
