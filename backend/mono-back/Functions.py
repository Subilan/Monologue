import markdown
import time
import urllib.request
import json
import re

def parseMarkdown(text):
    return markdown.markdown(text, extensions=['sane_lists', 'pymdownx.tilde', 'pymdownx.emoji', 'pymdownx.extra'])

def getDateString():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def getIP():
    with urllib.request.urlopen("https://pv.sohu.com/cityjson?ie=utf-8") as r:
        result = r.read().decode("utf8")
        ip = re.findall(r'\d+.\d+.\d+.\d+', result)
        if ip:
            return ip[0]
    return False