import os
from lxml import etree

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "code.html")

tree = etree.parse(file_path)

# get the div parent of all p elements of id 'unique'
print(tree.xpath("//p[@id='unique']/parent::div"))
# get the parent of all p elements of id 'unique'
print(tree.xpath("//p[@id='unique']/node()"))
# get all parents of all p elements of id 'unique'
print(tree.xpath("//p[@id='unique']/ancestor::node()"))
# get all parents of all p elements of id 'unique' including the p element
print(tree.xpath("//p[@id='unique']/ancestor-or-self::node()"))
# get all siblings of p elements with id 'outside' from the preceding parent
print(tree.xpath("//p[@id='outside']/preceding-sibling::node()"))

