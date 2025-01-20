"""Script to webscrape a page of cryptocurrencies info. This page renders in
HTML just the top 10 cryptocurrencies for each page, so this is just a
prototype."""

import requests
from lxml import html
import pandas as pd
from enum import Enum
from loguru import logger

BASE_URL = "https://coinmarketcap.com"
HEADERS_VALUE = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"


class XPathsCryptos(Enum):
    NAME        = ".//div[contains(@class, 'hide-ranking-number')]/p/text()"
    ACRONYM     = ".//p[contains(@class, 'coin-item-symbol')]/text()"
    PRICE       = ".//a[contains(@class, 'cmc-link')]/span//text()"
    PERC_CHANGE = ".//span[contains(@class, 'icon-Caret')]/parent::span/text()"
    MARKET_CAP  = ".//td[contains(@style, 'text-align:end')][position() = 5]//p/span[position() = 2]/text()"
    MARKET_CAP_MISSING = ".//td[contains(@style, 'text-align:end')][position() = 5]/div/text()"


def request_page(page_num: int) -> html.HtmlElement:
    """Request page number :param:`page_num` from BASE_URL."""

    # get data
    resp = requests.get(url=f"{BASE_URL}/?page={page_num}", 
                        headers={"User-Agent": HEADERS_VALUE})
    
    # get main data from requested data
    tree = html.fromstring(html=resp.text)
    
    return tree

def is_next_button_disable(tree: html.HtmlElement) -> bool:
    """Detect if a given page has the 'next' button disable. If the 'next'
    button is disable it means there is no more pages available in the
    pagination."""
    
    # get all next disable elements
    next_disable_elements = tree.xpath("//ul[contains(@class, 'pagination')]/li[contains(@class, 'next disable')]")
    
    # check if there exist any disable button
    exist_next_disable = len(next_disable_elements) > 0

    return exist_next_disable

def get_currency_table_rows_from_page(tree: html.HtmlElement) -> list[html.HtmlElement]:
    """Get the table of currencies from page."""

    # get the table of currency data
    currency_table = tree.xpath("//table")[0]
    table_rows = currency_table.xpath("./tbody/tr")

    return table_rows

def get_main_data_from_currency_table_rows(
        currency_table_rows: list[html.HtmlElement],
        ) -> pd.DataFrame:
    """Get main data from each row of the currency table."""

    # get the main data from each table row 
    df_currencies = pd.DataFrame()
    for row in currency_table_rows[:10]:  # we scrape just the first 10th because the rest are in Javascript
        
        # get data
        _perc_changes = row.xpath(XPathsCryptos.PERC_CHANGE.value)
        _name = row.xpath(XPathsCryptos.NAME.value)
        _acronym = row.xpath(XPathsCryptos.ACRONYM.value)
        _price = row.xpath(XPathsCryptos.PRICE.value)
        try:
            _market_cap = row.xpath(XPathsCryptos.MARKET_CAP.value)
            assert len(_market_cap) > 0
        except AssertionError:
            if row.xpath(XPathsCryptos.MARKET_CAP_MISSING.value)[0] == '--':
                _market_cap = "missing"
                logger.warning(f"  _market_cap missing for crypto: {_name}")
            else:
                raise ValueError()
        
        _df_currency = pd.DataFrame({
            "name": _name,
            "acronym": _acronym,
            "price": _price,
            "perc_change_1h": [_perc_changes[0]],
            "perc_change_24h": [_perc_changes[1]],
            "perc_change_7d": [_perc_changes[2]],
            "market_cap": _market_cap,
            })

        if df_currencies.empty:
            df_currencies = _df_currency
        else:
            df_currencies = pd.concat([df_currencies, _df_currency])

    return df_currencies

page_num = 1
tree = request_page(page_num=page_num)
currency_table_rows = get_currency_table_rows_from_page(tree)
df_currencies = get_main_data_from_currency_table_rows(currency_table_rows)

while not is_next_button_disable(tree):
    page_num += 1
    logger.info(f"scraping page: {page_num}")

    tree = request_page(page_num=page_num)
    currency_table_rows_new = get_currency_table_rows_from_page(tree)
    df_currencies_new = get_main_data_from_currency_table_rows(currency_table_rows_new)

    df_currencies = pd.concat([df_currencies, df_currencies_new], axis=0)

df_currencies.to_csv("tutorials/05.projects/project2/currencies.csv", index=False)
