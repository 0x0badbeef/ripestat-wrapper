from ripestat_wrapper import endpoints
from ripestat_wrapper.RIPEStat import RIPEStatRequestObj, RIPEStatReturn, ASN

def get_country_asn(country, time):
    requestObj = RIPEStatRequestObj()
    data = requestObj.get_request(endpoints.COUNTRY_ASN_LIST(country, time))
    return [ASN(asn) for asn in data['resources']['asn']]
