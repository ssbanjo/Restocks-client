# Installation
```
pip install restocks-client
```

# Introduction
You can search for products without being logged in, however, there are some client methods which require you to be logged in to your Restocks.net account to be used.

You can either use the client with or without proxies. Proxies will rotate for each client call for those methods which do not require login. The same proxy will be used for all the client calls after you log in if you decide to do so.

| Method  | Description | Login |
| ------------- | ------------- | :-------------: |
| `search_products`  | Searches for products. | NO |
| `get_product`  | Gets all the data of an specific product. | NO |
| `get_size_lowest_price` | Gets the lowest price of a product size. | YES |
| `get_sales_history` | Gets the account sold products. | YES |
| `get_listings_history` | Gets the account current product listings. | YES |
| `list_product` | Lists a product for sale. | YES |
| `edit_listing` | Edits a product listing. | YES |
| `delete_listing` | Deletes a product listing. | YES |

# Example

```python
from restocks.client import Client
from restocks.filters import SellMethod, ListingDuration


proxy = {"https": "https://username:password@ip:port"} 
# or optionally
proxy = [{"https": "https://username:password@ip:port"}, {"https": "https://username:password@ip:port"}]

client = Client(proxy=proxy)


# ---- Get product data ---------------------- #

product = client.get_product("DD1391-100")

print(product.name, product.sku)

# -------------------------------------------- #


# ---- Log in to your Restocks.net account --- #

username = "YOUR_USERNAME"
password = "YOUR_PASSWORD"

client.login(username, password)

# -------------------------------------------- #


# ---- Get the account sales ----------------- #

sales = client.get_sales_history()

for sale in sales:
    
    print(sale.name, sale.price, sale.date)
    
# -------------------------------------------- #


# ---- List a product for sale --------------- #

listed = client.list_product(
    product=product, # DD1391-100
    store_price=3000,
    size="42",
    sell_method=SellMethod.Resell,
    duration=ListingDuration.Days60
)

print(listed)

# -------------------------------------------- #
```
