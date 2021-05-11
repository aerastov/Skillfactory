import json
import requests
from config import API_KEY
from config import list_of_currencies

class APIException(Exception):
    pass

# quote - валюта 1
# base - валюта, в которую переводим
# amount - кол-во валюты 1

class Convertor:
    @staticmethod
    def get_price(values):
        if len(values) != 3:
            raise APIException("Неверное количество параметров")
        quote, base, amount = values
        if quote == base:
            raise APIException(f"Вы ввели одинаковые валюты {base}")
        try:
            quote_formated = list_of_currencies[quote]
        except KeyError:
            raise APIException(f"Такая валюта не поддерживается {quote}")
        try:
            base_formated = list_of_currencies[base]
        except KeyError:
            raise APIException(f"Такая валюта не поддерживается {base}")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не корректно введено количество валюты {amount}")

        link = f'http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}'
        res_quote = requests.get(f'{link}&symbols={quote_formated}')
        res_base = requests.get(f'{link}&symbols={base_formated}')
        result = ((json.loads(res_base.content)["rates"][base_formated]) * amount) / (json.loads(res_quote.content)["rates"][quote_formated])
        return round(result, 2)



# exchanger = list_of_currencies