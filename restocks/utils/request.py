import random
from typing import Optional, Union
from requests import Response
from ..exceptions import RequestException

class _ProxyPool():
    
    def __init__(self, proxy: Union[dict, list] = None) -> None:
        
        match proxy:
            case dict(): self.pool = [proxy]
            case list(): self.pool = proxy
            case _: self.pool = [None]
                
    def get_proxy(self) -> Optional[dict]:
        
        return random.choice(self.pool)
    
def validate_response(response: Response, status_code: int, msg: str = None) -> Response:

    if response.status_code != status_code:

        err = f"request failed with status code {response.status_code}" + (f": {msg}" if msg else "")
        
        raise RequestException(err)
    
    return response
                
    
