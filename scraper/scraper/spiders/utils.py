import re
from bs4 import BeautifulSoup

def extract_text(html_string):
    text = BeautifulSoup(html_string, 'html.parser').get_text()
    text = re.sub(u"\u00a0", "", text)
    text = re.sub(r"\n", "", text)
    text = re.sub(r"\t", "", text)
    text = re.sub(r"\r", "", text)
    return text

def clean_price(text):
    non_decimal = re.compile(r'[^\d.]+')
    result = non_decimal.sub('', text)
    return result
