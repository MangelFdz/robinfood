import os
from lxml import etree

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "code.html")

tree = etree.parse(file_path)

# get all h1 in the html
print(tree.xpath("//h1"))
# get div elements of class intro
print(tree.xpath("//div[@class='intro']"))
# get p elements inside div elements of class intro
print(tree.xpath("//div[@class='intro']/p"))

# conditionals
# ... get p elements of div elements of class intro or outro
print(tree.xpath("//div[@class='intro' or @class='outro']/p"))
# ... get the text of p elements of div elements of class intro or outro
print(tree.xpath("//div[@class='intro' or @class='outro']/p/text()"))
# ... get the href values from a elements
print(tree.xpath("//a/@href"))
# ... get the href values starting with https from a elements
print(tree.xpath("//a[starts-with(@href, 'https')]"))
# ... get the href values containing google from a elements
print(tree.xpath("//a[contains(@href, 'google')]"))
# ... get a elements whose text contains France
print(tree.xpath("//a[contains(text(), 'France')]"))
# ... get the first element of a list element with id items
print(tree.xpath("//ul[@id='items']/li[1]"))
# ... get the first and forth element of a list element with id items
print(tree.xpath("//ul[@id='items']/li[position() = 1 or position() = 4]"))
