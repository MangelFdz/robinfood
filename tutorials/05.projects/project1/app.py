import os
import re
import json
import click
import requests
import pandas as pd
from lxml import html
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output/")

def _create_output_dir():
    
    if not Path(OUTPUT_DIR).exists():
        os.makedirs(OUTPUT_DIR)

def write_json(book_info, filename):
    
    _create_output_dir()
    
    file_path_json = os.path.join(OUTPUT_DIR, filename)
    with open(file_path_json) as f:
        f.write(json.dumps(book_info))

def write_csv(book_info, filename):
    
    _create_output_dir()

    file_path_csv = os.path.join(OUTPUT_DIR, filename)
    pd.DataFrame(book_info).to_csv(file_path_csv)

@click.command()
@click.option("--book_url", default="http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
@click.option("--filename", default="data.csv")
def scrape(book_url, filename):

    # request data
    resp = requests.get(url=book_url,
                        headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"})

    # get main data from requested data
    tree = html.fromstring(html=resp.text)
    product_main = tree.xpath("//div[contains(@class, 'product_main')]")[0]

    # get raw data
    title = product_main.xpath(".//h1/text()")[0]
    price = product_main.xpath(".//p[1]/text()")[0].replace("Â", "")
    availability = product_main.xpath(".//p[2]/text()")[1].strip()
    description = tree.xpath("//div[@id='product_description']/following-sibling::p/text()")[0]

    # clean raw data
    availability = re.compile(r"\d+").findall(availability)

    # structure data
    book_info = {
        "title": title,
        "price": price,
        "in_stock": availability,
        "description": description,
    }
    print(book_info)

    # write data
    filename_extention = filename.split(".")[1]
    # ... json
    if filename_extention == "json":
        write_json(book_info, filename)
    # ... csv
    elif filename_extention == "csv":
        write_csv(book_info, filename)
    else:
        click.echo("The extention provided is not supported")

if __name__ == "__main__":
    scrape()
