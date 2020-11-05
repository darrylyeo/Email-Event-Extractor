import re
import sys
import nltk


def get_dates(email):
    date_pattern = r'((0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d)|' \
                   r'((0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d)'
    # mmdd_pattern = r'^(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d$'
    # ddmm_pattern = r'^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$'
    return [x for x in re.finditer(date_pattern, email)]


if __name__ == '__main__':
    filename = sys.argv[1]
    f = open(filename)
    raw = f.read()

    dates = get_dates(raw)
    print(len(dates))
    for date in dates:
        print(date.group(0))
