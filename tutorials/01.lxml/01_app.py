"""lxml parsing trees"""

import os
from lxml import etree

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "src/web_page.html")

# parse a single html
tree = etree.parse(file_path)
print(tree)
print(etree.tostring(tree))

# find elements in the head or the body of the html
print(tree.find("head/title").text)
print(tree.find("body/p").text)

# find all list elements
list_items = tree.findall("body/ul/li")
for item in list_items:
    a = item.find("a")
    if a is not None:
        print(f"{item.text.strip()} {a.text}")
    else:
        print(f"{item.text}")