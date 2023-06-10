import os
from lxml import etree

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "code.html")

tree = etree.parse(file_path)
html = tree.getroot()

# get all h1 elements
print(html.cssselect("h1"))
# get all elements of class intro
print(html.cssselect(".intro"))
# get the div elements of class intro
print(html.cssselect("div.intro"))
# get elements with id location
print(html.cssselect("#location"))
# get span elements with id location
print(html.cssselect("span#location"))
# get elements of multiple classes
print(html.cssselect(".bold.italic"))

# get elements with non-standard attributes different than class and id
print(html.cssselect("li[data-identifier='7']"))
# get all elements with a specific attribute different than class and id
print(html.cssselect("[data-identifier='7']"))

# conditionals
# ... get a elements with href attributes starting with 'https'
print(html.cssselect("a[href^='https']"))
# ... get a elements with href attributes ending with 'fr'
print(html.cssselect("a[href$='fr']"))
# ... get a elements with href attributes containing 'google'
print(html.cssselect("a[href*='google']"))

# get elements by position
# ... get all p elements inside an elements div of class intro
print(html.cssselect("div.intro p"))
# ... get all p elements inside an elements div of class intro with all nested sub-elements
print(html.cssselect("div.intro p, span#location"))
# ... get all p elements that are direct children of a div elements of class intro
print(html.cssselect("div.intro > p"))
# ... get all p elements immidiate after a div of class intro
print(html.cssselect("div.intro + p"))
# ... get the 1st and 3rd li elements
print(html.cssselect("li:nth-child(1), li:nth-child(3)"))
# ... get all odd li elements
print(html.cssselect("li:nth-child(odd)"))
# ... get all even li elements
print(html.cssselect("li:nth-child(even)"))