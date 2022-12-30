import math
from typing import Union

from ..exceptions import LoginException, SessionException
from ..filters import SellMethod, ListingDuration
from .core import ClientCore
from ..product import SIZES_IDS, Product

class Client(ClientCore):
        
    def __init__(self, proxy: Union[dict, list] = None) -> None:
        
        """
        Initializes a Restocks.net client with the option to log into your personal account.

        Args:
            proxy: a single or multiple proxies to use for the requests. Proxies will rotate at each request for methods 
            which do not require a log in. A random static proxy will be used for all the requests after you log in.
        """        
        
        super().__init__(proxy)
        
    def login(self, email: str, password: str):
        
        """
        Logs into your Restocks.net account.

        Args:
            email: your Restocks.net account email.
            password: your Restocks.net account password.
        """

        self._set_locale()
        
        login_page = self._login_page_request()
                
        csrf_token = self._csrf_token_parsing(login_page)
        
        if not csrf_token:
            
            raise LoginException("csrf-token not found")
        
        res = self._login_with_token_request(csrf_token, email, password)
        
        if "loginForm" in res:

            raise LoginException("invalid login credentials")
                
        main_page = self._main_page_request()

        session_token = self._csrf_token_parsing(main_page)

        if not csrf_token:
            
            raise LoginException("session token not found")
        
        self._session_token = session_token    
        
    def get_sales_history(self, query: str = None, page: int = 1) -> list[Product]:              
        
        """
        Gets the account product sales history.

        Args:
            query: query to base the search on. Defaults to None.
            page: the page number. One page contains 48 products. Defaults to 1.

        Raises:
            SessionException: if no sales were found.
            
        Returns:
            List containing the history all the account sold products.
        """        

        res = self._sales_history_request(query or "", page)
        
        src = res["products"]
        
        if "no__listings__notice" in src:
            
            raise SessionException("no sales found")
        
        sales = self._sales_history_parsing(src)
        
        return [Product._from_json(s) for s in sales]
    
    def get_listings_history(self, query: str = None, page: int = 1, sell_method: SellMethod = SellMethod.Resell) -> list[Product]: 
                     
        """
        Gets the account listings history.

        Args:
            query: a query to base the search on. Defaults to None.
            page: the page number. One page contains 48 products. Defaults to 1.

        Raises:
            SessionException: if no listings were found.

        Returns:
            A list containing all the account listed products.
        """        
        
        res = self._listings_request(query or "", page, "consignment" if sell_method == SellMethod.Consign else sell_method)
        
        src = res["products"]
        
        if "no__listings__notice" in src:
            
            raise SessionException("no listings found")
        
        listings = self._listings_parsing(src)
        
        return [Product._from_json(l) for l in listings]
    
    def search_products(self, query: str, page: int = 1) -> list[Product]:
        
        """
        Searches for products based on a provided query. 

        Args:
            query: query to base the search on.
            page: the page number. One page contains 48 products. Defaults to 1.


        Returns:
            List containing the found products and his data.
        """                

        res = self._search_product_request(query, page)

        if not res["data"]:
            
            page = math.ceil(res["total"] / 48)
            
            res = self._search_product_request(query, page)
            
        return [Product._from_json(p) for p in res["data"]]


    def get_product(self, sku_or_query: str) -> Product:
        
        """
        Gets the full data of a product.

        Args:
            sku_or_query: either the SKU code of the sneaker or a name to base the search on.

        Returns:
            The product data
        """        

        res = self._search_product_request(sku_or_query, 1)

        product = res["data"][0]
        
        p = Product._from_json(product)

        src = self._product_request(p.slug)

        variants = self._product_parsing(src)

        product["variants"] = variants
        
        return Product._from_json(res["data"][0])

    def get_size_lowest_price(self, product_id: int, size: str) -> int:
        
        """
        Gets the lowest price for a product size.

        Args:
            product_id: the product id.
            size: the product size.

        Returns:
            The size lowest price.
        """        
        
        size_id = SIZES_IDS.get(size)
        
        if not size:
            
            raise SessionException("invalid size")
        
        res = self._size_lowest_price_request(product_id, size_id)
        
        return int(res)
    
    def list_product(self, product: Union[Product, str], store_price: int, size: str, sell_method: SellMethod, duration: ListingDuration) -> bool:
        
        """
        Lists a product for sale.

        Args:
            product: either the `Product` object or the product sku.
            store_price: the price for the listing.
            size: the product size you are willing to sell.
            sell_method: the selling method.
            duration: the listing duration.

        Returns:
            A boolean that indicates if the product was listed successfuly.
        """        
        
        if not isinstance(product, Product):
            
            product = self.get_product(product)
        
        price = self._get_sell_profit(store_price, sell_method)
        
        size_id = SIZES_IDS.get(size)
        
        if not size:
            
            raise SessionException("invalid size")
                
        res = self._create_listing_request(
            product_id=product.id,
            sell_method=sell_method,
            size_id=size_id,
            store_price=store_price,
            price=price,
            duration=duration
        )
                
        return "success" in res["redirectUrl"]
    
    def edit_listing(self, listing_id: int, new_price: int) -> bool:
        
        """
        Edit the price of a current listing.

        Args:
            listing_id: the listing id.
            new_price: the new price.

        Returns:
            A boolean that indicates if the listing was edited successfuly.
        """        
        
        res = self._edit_listing_request(listing_id, new_price)
        
        return res.get("success", False)
    
    def delete_listing(self, listing_id: int) -> bool:
        
        """
        Delete a current listed product.

        Args:
            listing_id: the listing id.

        Returns:
            A boolean that indicates if the listing was deleted successfuly.
        """        
        
        res = self._delete_listing_request(listing_id)
        
        return res.get("success", False)