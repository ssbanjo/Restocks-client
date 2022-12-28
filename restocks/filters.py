from enum import StrEnum

class ListingDuration(StrEnum):

    Days30 = "30"
    Days60 = "60"
    Days90 = "90"
    
class SellMethod(StrEnum):

    Consign = "consign"
    Resell = "resale"
