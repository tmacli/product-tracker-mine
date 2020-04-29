# https://github.com/tnware/product-checker
# by Tyler Woods
# coded for Bird Bot and friends
# https://tylermade.net
import requests
import time
import json
from datetime import datetime
import urllib.parse as urlparse
from urllib.parse import parse_qs
import csv
stockdict = {}
sku_dict = {}
bestbuylist = []
targetlist = []
walmartlist = []
bbdict = {}


webhook_dict = {
#"name_your_webhook": "http://your.webhook.url/123"

# Best Buy - Nintendo

"bb_neon_switch": "https://discordapp.com/api/webhooks/704891256765022208/iXKaouZpwtWdW9vxqKp8OPlFSoCsICNnoAJqvjczYPKtfU6Y6tAhz3lfpP_Q6RefGsTu",
"bb_gray_switch": "https://discordapp.com/api/webhooks/704891256765022208/iXKaouZpwtWdW9vxqKp8OPlFSoCsICNnoAJqvjczYPKtfU6Y6tAhz3lfpP_Q6RefGsTu",
"bb_animalcrossing_switch": "https://discordapp.com/api/webhooks/704891256765022208/iXKaouZpwtWdW9vxqKp8OPlFSoCsICNnoAJqvjczYPKtfU6Y6tAhz3lfpP_Q6RefGsTu",
"bb_ringfit": "https://discordapp.com/api/webhooks/704891256765022208/iXKaouZpwtWdW9vxqKp8OPlFSoCsICNnoAJqvjczYPKtfU6Y6tAhz3lfpP_Q6RefGsTu",

# Best Buy - Webcams

"bb_logitech_c920s": "https://discordapp.com/api/webhooks/704744387615260784/HxNrljwTKMTBnRg5A7NuepkXZOLC-nZVq28xJPe6algexvunX0trPKgugEZbQ7SJB8sc",
"bb_logitech_c920": "https://discordapp.com/api/webhooks/704744387615260784/HxNrljwTKMTBnRg5A7NuepkXZOLC-nZVq28xJPe6algexvunX0trPKgugEZbQ7SJB8sc",
"bb_logitech_c922": "https://discordapp.com/api/webhooks/704744387615260784/HxNrljwTKMTBnRg5A7NuepkXZOLC-nZVq28xJPe6algexvunX0trPKgugEZbQ7SJB8sc",

# Target Nintendo

"target_neon_switch": "https://discordapp.com/api/webhooks/704891256765022208/iXKaouZpwtWdW9vxqKp8OPlFSoCsICNnoAJqvjczYPKtfU6Y6tAhz3lfpP_Q6RefGsTu",
"target_gray_switch": "https://discordapp.com/api/webhooks/704891256765022208/iXKaouZpwtWdW9vxqKp8OPlFSoCsICNnoAJqvjczYPKtfU6Y6tAhz3lfpP_Q6RefGsTu",
"target_ringfit": "https://discordapp.com/api/webhooks/704891256765022208/iXKaouZpwtWdW9vxqKp8OPlFSoCsICNnoAJqvjczYPKtfU6Y6tAhz3lfpP_Q6RefGsTu",

# Walmart Nintendo

"walmart_neon_switch": "https://discordapp.com/api/webhooks/704891256765022208/iXKaouZpwtWdW9vxqKp8OPlFSoCsICNnoAJqvjczYPKtfU6Y6tAhz3lfpP_Q6RefGsTu",
"walmart_gray_switch": "https://discordapp.com/api/webhooks/704891256765022208/iXKaouZpwtWdW9vxqKp8OPlFSoCsICNnoAJqvjczYPKtfU6Y6tAhz3lfpP_Q6RefGsTu",
"walmart_animalcrossing_switch": "https://discordapp.com/api/webhooks/704891256765022208/iXKaouZpwtWdW9vxqKp8OPlFSoCsICNnoAJqvjczYPKtfU6Y6tAhz3lfpP_Q6RefGsTu",
"walmart_ringfit": "https://discordapp.com/api/webhooks/704891256765022208/iXKaouZpwtWdW9vxqKp8OPlFSoCsICNnoAJqvjczYPKtfU6Y6tAhz3lfpP_Q6RefGsTu"
}


urldict = {
#"http://product.url/123": "name_your_webhook",
# Best Buy - Nintendo
"https://www.bestbuy.com/site/nintendo-switch-32gb-console-neon-red-neon-blue-joy-con/6364255.p?skuId=6364255": "bb_neon_switch",
"https://www.bestbuy.com/site/nintendo-switch-32gb-console-gray-joy-con/6364253.p?skuId=6364253": "bb_gray_switch",
"https://www.bestbuy.com/site/nintendo-switch-animal-crossing-new-horizons-edition-32gb-console-multi/6401728.p?skuId=6401728": "bb_animalcrossing_switch",
"https://www.bestbuy.com/site/ring-fit-adventure-nintendo-switch/6352149.p?skuId=6352149": "bb_ringfit",

# Best Buy - Webcams
"https://www.bestbuy.com/site/logitech-c920s-hd-webcam/6321794.p?skuId=6321794": "bb_logitech_c920s",
"https://www.bestbuy.com/site/logitech-c920-pro-webcam-black/4612476.p?skuId=4612476": "bb_logitech_c920",
"https://www.bestbuy.com/site/logitech-c922-pro-stream-webcam/5579380.p?skuId=5579380": "bb_logitech_c922",

# Target Nintendo

"https://www.target.com/p/nintendo-switch-with-neon-blue-and-neon-red-joy-con/-/A-77464001": "target_neon_switch",
"https://www.target.com/p/nintendo-switch-with-gray-joy-con/-/A-77464002": "target_gray_switch",
"https://www.target.com/p/ring-fit-adventure---nintendo-switch/-/A-76593324": "target_ringfit",

# Walmart Nintendo

"https://www.walmart.com/ip/Nintendo-Switch-Console-with-Neon-Blue-Red-Joy-Con/709776123?selectedSellerId=0&irgwc=1&sourceid=imp_URNysUUQixyORUtwUx0Mo38XUki2dTUUET5x3c0&veh=aff&wmlspartner=imp_10078&clickid=URNysUUQixyORUtwUx0Mo38XUki2dTUUET5x3c0": "walmart_neon_switch",
"https://www.walmart.com/ip/Nintendo-Switch-Console-with-Gray-Joy-Con/994790027?selectedSellerId=0&irgwc=1&sourceid=imp_URNysUUQixyORUtwUx0Mo38XUki2dRU0ET5x3c0&veh=aff&wmlspartner=imp_10078&clickid=URNysUUQixyORUtwUx0Mo38XUki2dRU0ET5x3c0": "walmart_gray_switch",
"https://www.walmart.com/ip/Nintendo-Switch-Console-Animal-Crossing-New-Horizons-Edition/539083068?selectedSellerId=0&irgwc=1&sourceid=imp_URNysUUQixyORUtwUx0Mo38XUki2dRU0ET5x3c0&veh=aff&wmlspartner=imp_10078&clickid=URNysUUQixyORUtwUx0Mo38XUki2dRU0ET5x3c0": "walmart_animalcrossing_switch",
"https://www.walmart.com/ip/Nintendo-Switch-Ring-Fit-Adventure-Black/434503657?selectedSellerId=0&irgwc=1&sourceid=imp_URNysUUQixyORUtwUx0Mo38XUki2dRU0ET5x3c0&veh=aff&wmlspartner=imp_10078&clickid=URNysUUQixyORUtwUx0Mo38XUki2dRU0ET5x3c0": "walmart_ringfit"
}

class Target:

    def __init__(self, url, hook):
        self.url = url
        self.hook = hook
        webhook_url = webhook_dict[hook]
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        page = requests.get(url)
        al = page.text
        title = al[al.find('"twitter":{"title":') + 20 : al.find('","card')]
        #print(title)
        if "Temporarily out of stock" in page.text:
            print("[" + current_time + "] " + "Sold Out: (Target.com) " + title + "\n")
            stockdict.update({url: 'False'})
        else: 
            print("[" + current_time + "] " + "In Stock: (Target.com) " + title + " - " + url)
            slack_data = {'content': current_time + " " + title + " in stock at Target - " + url}
            if stockdict.get(url) == 'False':
                response = requests.post(
                webhook_url, data=json.dumps(slack_data),
                headers={'Content-Type': 'application/json'})
            stockdict.update({url: 'True'})
        #print(stockdict)

class BestBuy:

    def __init__(self, sku, hook):
         self.sku = sku
         self.hook = hook
         webhook_url = webhook_dict[hook]
         now = datetime.now()
         current_time = now.strftime("%H:%M:%S")
         url = "https://www.bestbuy.com/api/tcfb/model.json?paths=%5B%5B%22shop%22%2C%22scds%22%2C%22v2%22%2C%22page%22%2C%22tenants%22%2C%22bbypres%22%2C%22pages%22%2C%22globalnavigationv5sv%22%2C%22header%22%5D%2C%5B%22shop%22%2C%22buttonstate%22%2C%22v5%22%2C%22item%22%2C%22skus%22%2C" + sku + "%2C%22conditions%22%2C%22NONE%22%2C%22destinationZipCode%22%2C%22%2520%22%2C%22storeId%22%2C%22%2520%22%2C%22context%22%2C%22cyp%22%2C%22addAll%22%2C%22false%22%5D%5D&method=get"
         headers2 = {
         "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
         "accept-encoding": "gzip, deflate, br",
         "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
         "cache-control": "max-age=0",
         "upgrade-insecure-requests": "1",
         "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.69 Safari/537.36"
         }
         page = requests.get(url, headers=headers2)
         link = "https://www.bestbuy.com/site/" + sku + ".p?skuId=" + sku
         al = page.text
         search_string = '"skuId":"' + sku + '","buttonState":"'
         stock_status = al[al.find(search_string) + 33 : al.find('","displayText"')]
         product_name = sku_dict.get(sku)
         if stock_status == "SOLD_OUT":
             print("[" + current_time + "] " + "Sold Out: (BestBuy.com) " + product_name + "\n")
             stockdict.update({sku: 'False'})
         elif stock_status == "CHECK_STORES":
             print(product_name + " sold out @ BestBuy (check stores status)")
             stockdict.update({sku: 'False'})
         else: 
             if stock_status == "ADD_TO_CART":
                 print("[" + current_time + "] " + "In Stock: (BestBuy.com) " + product_name + " - " + url)
                 slack_data = {'content': current_time + " " + product_name + " In Stock @ BestBuy " + link}
                 if stockdict.get(sku) == 'False':
                     response = requests.post(
                     webhook_url, data=json.dumps(slack_data),
                     headers={'Content-Type': 'application/json'})
                 stockdict.update({sku: 'True'})
                 #print(stockdict)

class Walmart:

    def __init__(self, url, hook):
        self.url = url
        self.hook = hook
        webhook_url = webhook_dict[hook]
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        page = requests.get(url)   
        al = page.text        
        title = al[al.find('<meta property="twitter:title" content="') + 40 : al.find('- Walmart.com"/><script>window._wml.seoTags')]
        #print(title)
        if page.status_code == 200:
            if "Add to cart" in page.text:
                print("[" + current_time + "] " + "In Stock: (Walmart.com) " + title)
                slack_data = {'content': current_time + " " + url + " in stock at Walmart"}
                if stockdict.get(url) == 'False':
                    response = requests.post(
                    webhook_url, data=json.dumps(slack_data),
                    headers={'Content-Type': 'application/json'})
                stockdict.update({url: 'True'})
            else: 
                print("[" + current_time + "] " + "Sold Out: (Walmart.com) " + title + "\n")
                stockdict.update({url: 'False'})

for url in urldict:
    hook = urldict[url]
    if "bestbuy.com" in url:
        print("BestBuy URL detected " + hook + "\n")
        parsed = urlparse.urlparse(url)
        sku = parse_qs(parsed.query)['skuId']
        sku = sku[0]
        bestbuylist.append(sku)
        headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "cache-control": "max-age=0",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.69 Safari/537.36"
        }
        page = requests.get(url, headers=headers)
        al = page.text
        title = al[al.find('<title >') + 8 : al.find(' - Best Buy</title>')]
        sku_dict.update({sku: title})
        bbdict.update({sku: hook})

    elif "target.com" in url:
        targetlist.append(url)
        print("Target URL detected " + hook + "\n")
    elif "walmart.com" in url:
        walmartlist.append(url)
        print("Walmart URL detected " + hook + "\n")
for url in urldict:
    stockdict.update({url: 'False'}) #set all URLs to be "out of stock" to begin
for sku in sku_dict:
    stockdict.update({sku: 'False'}) #set all SKUs to be "out of stock" to begin
while True:

# Target
    for url in targetlist:
        try:
            hook = urldict[url]
            Target(url, hook)
        except:
            print("Some problem occurred. Skipping instance...")

# Best Buy
    for sku in bestbuylist:
        try:
            hook = bbdict[sku]
            BestBuy(sku, hook)
        except:
            print("Some problem occurred. Skipping instance...")

# Walmart            
    for url in walmartlist:
        try:
            hook = urldict[url]
            Walmart(url, hook)
            time.sleep(2)
        except:
            print("Some problem occurred. Skipping instance...")
            time.sleep(2)

    time.sleep(2)
    
