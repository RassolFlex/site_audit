with open('D:/Python/site_audit/audit/main.py', 'rb') as f: content = f.read(); idx = content.find(b' or '); print(repr(content[idx + 3:idx + 60]))
