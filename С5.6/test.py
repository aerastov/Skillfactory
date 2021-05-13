
import json
import requests





API_KEY = "fbd38bdf2013b40abda7"
html = requests.get(f'https://free.currconv.com/api/v7/currencies?apiKey={API_KEY}')
result = (json.loads(html.content)["results"])
print(result)

for key,value in result.items():
    print(key, ':', value)
    print(value["currencyName"] + " : " + value["id"])
    # for key, value in value.items():
    #     print(key, ':', value)

# res_base = requests.get(f'{link}&symbols={base_formated}')
# result = (json.loads(res_base.content)["rates"][base_formated])
#
# tree = lxml.html.document_fromstring(html)
# title = tree.xpath('/html/head/title/text()')
# print(title)  # выводим полученный заголовок страницы

