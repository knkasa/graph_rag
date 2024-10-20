import wikipedia
import os

# Get data from wikipedia.

os.chdir('C:/Users/knkas/Desktop/GraphRag')

wikipedia.set_lang("ja")
state = "ドラゴンボール"
short_summary = False
directory = './data'

if not os.path.exists(directory):
    os.makedirs(directory)
    
title = wikipedia.page(state).title.lower().replace(" ", "_")
content = (wikipedia.page(state).summary if short_summary else wikipedia.page(state).content)
content = content.strip()
filename = os.path.join(directory, f"{title}.txt")
with open(filename, "w", encoding="utf-8") as f:
    f.write(content)
print(f"Saving {filename}")

