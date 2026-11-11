with open('D:/Python/site_audit/audit/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Заменяем линию с 8 backslash-n на обратную новую строку
old_pattern = r'''or \\\\\n                       re.search(r"<meta\s+property=["']og:description["'][^>]*content=["'](.*?)["']"'''
new_code = ''' or
                       re.search(r"<meta\s+property=["']og:description["'][^>]*content=["'](.*?)["']", response.text, re.IGNORECASE)'''

import re as pyregex
# Поиск через byte-string для точности
if b'or \\\\\\
                       ' in content.encode():
    content = content.replace(b' or \\\\\\\\\\\\\\
                       re.search', b' or\n                       re.search')
    with open('D:/Python/site_audit/audit/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fixed!')
else:
    print('Pattern not found, trying alternate...')
