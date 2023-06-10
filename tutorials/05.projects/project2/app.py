import requests
from lxml import html
import pandas as pd

# request data
resp = requests.get(url="https://coinmarketcap.com/",
                    headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"})

# get main data from requested data
tree = html.fromstring(html=resp.text)

# get the table of currency data
currencies_table = tree.xpath("//table")[0]
table_rows = currencies_table.xpath("./tbody/tr")

# get the main data from each table row 
df_currencies = pd.DataFrame()
for row in table_rows[:10]:  # we scrape just the first 10h because the rest are in Javascript
    perc_changes = row.xpath(".//span[contains(@class, 'icon-Caret')]/parent::span/text()")
    currency_data = {
        "name": row.xpath(".//div[contains(@class, 'name-area')]/p/text()"),
        "acronym": row.xpath(".//p[contains(@class, 'coin-item-symbol')]/text()"),
        "price": row.xpath(".//a[contains(@class, 'cmc-link')]/span/text()"),
        "perc_change_1h": [perc_changes[0]],
        "perc_change_24h": [perc_changes[1]],
        "perc_change_7d": [perc_changes[2]],
        "market_cap": row.xpath(".//span[contains(@class, 'gqomIJ')]/text()"),
    }
    df_currency = pd.DataFrame(currency_data)

    if df_currencies.empty:
        df_currencies = df_currency
    else:
        df_currencies = pd.concat([df_currencies, df_currency])

df_currencies