import endpoints
from RIPEStat import RIPEStatRequestObj, RIPEStatReturn

def get_country_asn(country, time):
    requestObj = RIPEStatRequestObj()
    data = requestObj.get_request(endpoints.COUNTRY_ASN_LIST(country, time))
    return data['asn']
