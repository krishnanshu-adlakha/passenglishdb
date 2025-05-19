import json

quotes = '{"quotes":["His bloody life, in my bloody hands", "The drink and drugs wont flush him out"]}'
quotes_json = eval(quotes)

print(quotes_json['quotes'])