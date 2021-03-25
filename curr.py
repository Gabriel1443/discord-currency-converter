import re
import json
import requests as rq

def get_currency(key):
    # commonly use rmb instead of CNY
    key = key.replace("RMB", "CNY")
    url = f"https://finance.yahoo.com/quote/{key}"
    res = rq.get(url)
    res_text = res.text
    m = re.search("root.App.main.+\\;", res_text)
    json_string = m.group(0)[16:-1]
    content = json.loads(json_string)
    try:
        currency = content["context"]["dispatcher"]["stores"]["StreamDataStore"]["quoteData"][key]["regularMarketPrice"]["raw"]
    except:
        print(content["context"]["dispatcher"]["stores"]["StreamDataStore"]["quoteData"][key])
    return float(currency)


if __name__ == "__main__":
    get_rmb_usd_currency()
