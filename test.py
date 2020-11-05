import datetime
import json
import eml_parser


def json_serial(obj):
  if isinstance(obj, datetime.datetime):
      serial = obj.isoformat()
      return serial


with open('conf_emails/1.eml', 'rb') as fhdl:
  raw_email = fhdl.read()

ep = eml_parser.EmlParser(include_raw_body=True)
parsed_eml = ep.decode_email_bytes(raw_email)

print(json.dumps(parsed_eml, default=json_serial))