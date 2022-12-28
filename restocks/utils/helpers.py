import re

def parse_int(number_str: str) -> int:
        
    return int(re.search(r'\d+', number_str.replace(".", "")).group(0))

def parse_size(size_str: str) -> str:
    
    num = re.search(r'\d+', size_str).group(0)
    
    return num + ".5" if (".5" in size_str or "½" in size_str) else num