import endpoints
import requests
import time

from RIPEStatReturn import RIPEStatReturn

class RIPEStatRequestObj:
    def __init__(self,
                 starttime=None,
                 endtime=None,
                 resource=None,
                 ):
        self.starttime = starttime
        self.endtime = endtime
        self.resource = resource

    def get_request(self, endpoint):
        start_time = time.time()
        resp = requests.get(endpoint)
        respObj = RIPEStatReturn(resp)
        end_time = time.time()
        data = respObj.get_data()
        return data, end_time - start_time
        

class ASN(RIPEStatRequestObj):
    def __init__(self,resource=None):
        super(ASN, self).__init__(self, resource=resource)
    
    def get_name(self):
        data, elapsed_time = self.get_request(endpoints.ASN_NAME_REGISTRY(self.resource))
        return data['holder'], elapsed_time
        

if __name__=='__main__':
    asn = ASN(resource=2568)
    print(2568, asn.get_name())

    