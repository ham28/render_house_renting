import logging

logger = logging.getLogger("django")
def get_region(province=None):
    region = None
    match province.lower():
        case 'fianarantsoa':
            region = ["AMORON'I MANIA", "ATSIMO-ATSINANANA", "HAUTE MATSIATRA", "IHOROMBE", "FITOVINANY",
                      "VATOVAVY"]
        case 'toliara':
            region = ["ANDROY", "ANOSY", "ATSIMO-ANDREFANA", "MENABE"]
        case 'antananarivo':
            region = ["ANALAMANGA", "BONGOLAVA", "ITASY", "VAKINANKARATRA"]
        case 'toamasina':
            region = ["ANALANJIROFO", "ATSINANANA", "ALAOTRA-MANGORO"]
        case 'mahajanga':
            region = ["MELAKY", "BOENY", "SOFIA", "BETSIBOKA"]
        case 'antsiranana':
            region = ["DIANA", "SAVA"]

    return region