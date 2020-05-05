import markdown
import time

def parseMarkdown(text):
    return markdown.markdown(text, extensions=['sane_lists', 'pymdownx.tilde', 'pymdownx.emoji', 'pymdownx.extra'])

def getDateString():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())