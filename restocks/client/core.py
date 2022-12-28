import re
from typing import Union
import requests
from bs4 import BeautifulSoup

from ..utils.helpers import parse_int, parse_size
from ..utils.request import validate_response, _ProxyPool

class ClientCore:

    _headers = {
        'Host': 'restocks.net',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
    }
    
    def __init__(self, proxy: Union[dict, list] = None) -> None:

        self._session = requests.Session()

        self._proxy_pool = _ProxyPool(proxy=proxy)
        self._session.proxies = self._proxy_pool.get_proxy()
        
        self._base_url = "https://restocks.net"

        self._session_token = None

    @staticmethod
    def _csrf_token_parsing(src: str) -> Union[str, None]:

        soup = BeautifulSoup(src, "lxml")

        csrf_token = soup.find("meta", {"name": "csrf-token"})

        return csrf_token.get("content") if csrf_token else None

    def _set_locale(self):
        
        url = self._base_url

        self._session.headers = {
            'Host': 'restocks.net',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
        }

        res = self._session.get(url)
        
        self._base_url = res.url
        
    def _main_page_request(self) -> str:

        url = self._base_url

        self._session.headers = {
            'Host': 'restocks.net',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': self._base_url,
        }

        res = self._session.get(url)

        return validate_response(res, 200).text

    def _login_page_request(self) -> str:

        url = self._base_url + "/login"

        self._session.headers = {
            'Host': 'restocks.net',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': self._base_url,
        }

        res = self._session.get(url)

        return validate_response(res, 200).text

    def _login_with_token_request(self, token: str, username: str, password: str) -> str:

        url = self._base_url + "/login"

        self._session.headers = {
            'Host': 'restocks.net',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'origin': 'https://restocks.net',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': self._base_url + '/login',
        }

        params = {
            "_token": token,
            "email": username,
            "password": password
        }

        res = self._session.post(url, params=params)

        return validate_response(res, 200).text

    def _sales_history_request(self, query: str, page: int) -> dict:

        url = self._base_url + "/account/sales/history"

        self._session.headers = {
            'Host': 'restocks.net',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
        }

        params = {
            'page': page,
            'search': query,
        }

        res = self._session.get(url, params=params)

        return validate_response(res, 200).json()

    @staticmethod
    def _sales_history_parsing(src: str) -> dict:

        soup = BeautifulSoup(src, "lxml")

        sales = soup.find("tbody").find_all("tr")

        products = []

        for product in sales:

            img = product.find("img")["src"]
            name, size, id, price, date = list(product.stripped_strings)

            products.append({"name": name, "size": size, "id": id, "storeprice": price, "date": date, "image": img})

        return products

    def _search_product_request(self, query: str, page: int) -> dict:

        url = self._base_url + "/shop/search"

        headers = ClientCore._headers

        params = {
            "q": query,
            "page": page,
            "filters[0][range][price][gte]": 1
        }

        res = requests.get(url, headers=headers, params=params, proxies=self._proxy_pool.get_proxy())

        return validate_response(res, 200).json()

    def _product_request(self, slug: str) -> str:

        headers = ClientCore._headers

        res = requests.get(slug, headers=headers, proxies=self._proxy_pool.get_proxy())

        return validate_response(res, 200).text

    @staticmethod
    def _product_parsing(src: str) -> dict:

        soup = BeautifulSoup(src, "lxml")

        variants_list = soup.find("ul", {"class": "select__size__list"})

        variants = variants_list.find_all("li", {"data-type": "all"})

        sizes = {}

        for variant in variants:

            oos = "out__of__stock" in variant.get("class")
            
            size = variant.find("span", {"class": "text"}).text
            size = parse_size(size)
            
            price = variant.find("span", {"class": "float-right price"}).find_next("span").text
            price = None if oos else parse_int(price)

            sizes[size] = price

        return sizes

    def _sell_profit_request(self, store_price: int, sell_method: str) -> dict:

        url = self._base_url + "/pricing"

        self._session.headers = {
            'Host': 'restocks.net',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            "x-csrf-token": self._session_token,
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'origin': 'https://restocks.net',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
        }

        params = {
            "_token": self._session_token,
            'storeprice': store_price,
            'sell_method': sell_method,
        }

        res = self._session.post(url, params=params)

        return validate_response(res, 200).json()

    def _get_sell_profit(self, store_price: int, sell_method: str) -> float:

        res = self._sell_profit_request(store_price, sell_method)

        return res["payout"]["decimal"]

    def _validate_listing_request(self, product_id: int, size_id: int, store_price: int, price: float, sell_method: str, duration: str) -> dict:

        url = self._base_url + "/account/sell/validate"

        self._session.headers = {
            'Host': 'restocks.net',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'origin': 'https://restocks.net',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
        }

        params = {
            '_token': self._session_token,
            'amount': '1',
            'baseproduct_id': product_id,
            'condition': '1',
            'size_id': size_id,
            'price': price,
            'store_price': store_price,
            'sell_method': sell_method,
            'duration': duration,
            'checkbox1_resale': '1',
            'checkbox2_resale': '1',
            'checkbox1_consignment': '1',
            'checkbox2_consignment': '1',
        }

        res = self._session.post(url, params=params)

        return validate_response(res, 200).json()

    def _create_listing_request(self, product_id: int, sell_method: str, size_id: int, store_price: int, price: float, duration: str) -> dict:

        url = self._base_url + "/account/sell/create"
        
        self._session.headers = {
            'Host': 'restocks.net',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'origin': 'https://restocks.net',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
        }

        params = {
            "_token": self._session_token,
            "listings[0][amount]": "1",
            "listings[0][sell_method]": sell_method,
            "listings[0][baseproduct_id]": product_id,
            "listings[0][condition]": "1",
            "listings[0][size_id]": size_id,
            "listings[0][store_price]": store_price,
            "listings[0][price]": price,
            "listings[0][duration]": duration,
            "listings[0][checkbox1_resale]": '1',
            "listings[0][checkbox2_resale]": '1',
            "listings[0][checkbox1_consignment]": '1',
            "listings[0][checkbox2_consignment]": '1'
        }
        
        res = self._session.post(url, params=params)

        return validate_response(res, 200, "invalid listing data").json()
    
    def _size_lowest_price_request(self, product_id: int, size_id: int) -> str:

        url = self._base_url + f"/product/get-lowest-price/{product_id}/{size_id}"
        
        headers = {
            'Host': 'restocks.net',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
        }

        res = self._session.get(url)         

        return validate_response(res, 200).text
    
    def _listings_request(self, query: str, page: int, sell_method: str) -> dict:
        
        url = self._base_url + f"/account/listings/{sell_method}"

        self._session.headers = {
            'Host': 'restocks.net',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
        }

        params = {
            'page': page,
            'search': query,
        }
        
        res = self._session.get(url, params=params)

        return validate_response(res, 200).json()
    
    
    @staticmethod
    def _listings_parsing(src: str) -> dict:

        soup = BeautifulSoup(src, "lxml")

        sales = soup.find("tbody").find_all("tr")

        products = []

        for product in sales:
            
            img = product.find("img")["src"]
            id = product.find("input", {"class", "baseproductid"})["value"]
            
            name, size, listing_id, price, date = list(product.stripped_strings)

            date = re.search(r'(\d+/\d+/\d+)', date).group(0)
            
            products.append({"name": name, "size": size, "listing_id": listing_id, "id": id, "storeprice": price, "date": date, "image": img})

        return products
    
    def _edit_listing_request(self, listing_id: int, new_price: int) -> dict:
        
        url = self._base_url + "/account/listings/edit"
        
        self._session.headers = {
            'Host': 'restocks.net',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'origin': 'https://restocks.net',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
        }

        params = {
            '_token': self._session_token,
            'id': listing_id,
            'store_price': new_price,
        }
        
        res = self._session.post(url, params=params)

        return validate_response(res, 200, "invalid listing id").json()
    
    def _delete_listing_request(self, listing_id: int) -> dict:
        
        url = self._base_url + "/account/listings/delete"
        
        self._session.headers = {
            'Host': 'restocks.net',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'origin': 'https://restocks.net',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
        }

        params = {
            '_token': self._session_token,
            'id': listing_id,
        }

        res = self._session.post(url, params=params)
        
        return validate_response(res, 200).json()