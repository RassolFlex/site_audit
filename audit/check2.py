with open('D:/Python/site_audit/audit/main.py', 'rb') as f:
    content = f.read()
idx = content.find(b' or ')
pattern = b' or \\\n                       re.search'
new = b' or\n                       re.search'
content2 = content.replace(pattern, new)
open('D:/Python/site_audit/audit/main.py', 'wb').write(content2)
print("Fixed!")
with open("D:/Python/site_audit/audit/main.py", "rb") as f: content = f.read(); idx = content.find(b" or "); pattern = b" or \\\\n                       re.search"; new = b" or
                       re.search"; content2 = content.replace(pattern, new); open("D:/Python/site_audit/audit/main.py", "wb").write(content2); print("Fixed!")