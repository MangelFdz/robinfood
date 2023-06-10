import requests

resp = requests.get(url="http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
print(resp)
print(resp.text)
# content property returns a byte object so it is prefered over the text attribute if we want to scrap images or videos from a web page
print(resp.content)
print(resp.headers)
print("-----------")
print(resp.request.headers)
resp = requests.get(url="http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
                    headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"})
print(resp.request.headers)