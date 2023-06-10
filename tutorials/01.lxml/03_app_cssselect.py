"""lxml using cssselect"""

import os
from lxml import etree

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "src/web_page.html")

# parse a single html
tree = etree.parse(file_path)
html = tree.getroot()

# using cssselect
# ... find all titles in the html
print(html.cssselect("title"))
# ... find all paragraphs in the html
print(html.cssselect("p"))

# find all list elements
list_items = html.cssselect("li")
for item in list_items:
    print(item)
    a = item.cssselect("a")
    if len(a) == 0:
        print(item.text)
    else:
        print(f"{item.text.strip()} {a[0].text}")
