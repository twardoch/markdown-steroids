RE_SMART_CONTENT = r'((?:[^\|]|\|(?=[^\W_]|\||\s)|(?<=\s)\|+?(?=\s))+?\|*?)'
RE_DUMB_CONTENT = r'((?:[^\|]|(?<!\|)\|(?=[^\W_]|\|))+?)'
RE_SMART_KBD_BASE = r'(\|{2})(?![\s\|])%s(?<!\s)\|{2}' % RE_SMART_CONTENT
RE_SMART_KBD = r'(?:(?<=_)|(?<![\w\|]))%s(?:(?=_)|(?![\w\|]))' % RE_SMART_KBD_BASE
RE_KBD_BASE = r'(\|{2})(?!\s)%s(?<!\s)\|{2}' % RE_DUMB_CONTENT
RE_KBD = RE_KBD_BASE
print(RE_SMART_KBD_BASE)
print(RE_SMART_KBD)

print(RE_KBD)
