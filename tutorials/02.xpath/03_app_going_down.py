import os
from lxml import etree

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "code.html")

tree = etree.parse(file_path)

# get the p childs of div elements of class 'intro'
print(tree.xpath("//div[@class='intro']/child::p"))
# get all elements after a div element of class 'intro'
print(tree.xpath("//div[@class='intro']/following::node()"))
# get all sibling elements after a div element of class 'intro'
print(tree.xpath("//div[@class='intro']/following-sibling::node()"))
