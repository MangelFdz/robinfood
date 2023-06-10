"""lxml using xpath"""

import os
from lxml import etree

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "src/web_page.html")

# parse a single html
tree = etree.parse(file_path)

# using xpath
# ... find all titles in the html
print(tree.xpath("//title"))
# ... get the text from all titles in the html
print(tree.xpath("//title/text()"))
# ... get the text from all paragraphs in the html
print(tree.xpath("//p/text()"))

# find all list elements
list_items = tree.xpath("//li")
for item in list_items:
    # using . as a relative path for xpath
    text = item.xpath(".//text()")
    # removing breaklines
    text = ''.join(map(str.strip, text))
    print(f"{text}")