import re
import json
import requests as rq

def get_usd_rmb_currency():
    url = "https://finance.yahoo.com/quote/USDCNY=X"
    res = rq.get(url)
    res_text = res.text
    m = re.search("root.App.main.+\\;", res_text)
    json_string = m.group(0)[16:-1]
    content = json.loads(json_string)
    currency = content["context"]["dispatcher"]["stores"]["StreamDataStore"]["quoteData"]["USDCNY=X"]["regularMarketPrice"]["raw"]
    return float(currency)

def get_rmb_usd_currency():
    url = "https://finance.yahoo.com/quote/CNYUSD=X/"
    res = rq.get(url)
    res_text = res.text
    m = re.search("root.App.main.+\\;", res_text)
    json_string = m.group(0)[16:-1]
    content = json.loads(json_string)
    currency = content["context"]["dispatcher"]["stores"]["StreamDataStore"]["quoteData"]["CNYUSD=X"]["regularMarketPrice"]["raw"]
    return float(currency)

if __name__ == "__main__":
    get_rmb_usd_currency()
