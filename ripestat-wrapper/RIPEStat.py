import endpoints
import requests

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
        

class ASN(RIPEStatRequestObj):
    def __init__(self,resource=None):
        super(ASN, self).__init__(self, resource=resource)
    
    def get_name(self):
        resp = requests.get(endpoints.ASN_NAME_REGISTRY(self.resource))
        respObj = RIPEStatReturn(resp)
        data = respObj.get_data()
        return data['holder']
    

if __name__=='__main__':
    asn = ASN(resource=2568)
    print(2568, asn.get_name())

    