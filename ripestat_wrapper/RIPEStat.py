from ripestat_wrapper import endpoints
import requests
import time

from ripestat_wrapper.RIPEStatReturn import RIPEStatReturn
from ripestat_wrapper.BGP import BGPRecord, BGPUpdateRecord
from ripestat_wrapper.prefix import Prefix

Session = requests.Session()

class RIPEStatRequestObj:
    def __init__(self,
                 starttime=None,
                 endtime=None,
                 resource=None
                 ):
        self.starttime = starttime
        self.endtime = endtime
        self.resource = resource
        self.query = None
        self.last_query_time = None
        self.last_query_timestamp = None

    def get_request(self, endpoint):
        start_time = time.time()
        resp = Session.get(endpoint)
        while resp.status_code == 400:
            time.sleep(5)
            print(endpoint)
            resp = Session.get(endpoint)
        respObj = RIPEStatReturn(resp)
        end_time = time.time()
        data = respObj.get_data()

        self.last_query_timestamp = respObj.query_time
        self.last_query_time = end_time - start_time
        self.query = endpoint
        return data
    
    def get_query_stats(self):
        return self.query, self.last_query_time 
        
class ASN(RIPEStatRequestObj):
    def __init__(self,resource=None):
        super(ASN, self).__init__(self, resource=resource)
        self.resource_id = resource # resource as int
    
    def get_name(self):
        data = self.get_request(endpoints.ASN_NAME_REGISTRY(self.resource))
        return data['holder'] 

    def get_announced_prefix(self, starttime, endtime):
        data = self.get_request(endpoints.ASN_ANNOUNCED_PREFIXES(self.resource, starttime, endtime))
        prefixes = data['prefixes']
        prefixesObjs = []
        for prefix in prefixes:
            prefixesObjs.append(Prefix(prefix['prefix'], starttime=prefix['timelines'][0]['starttime'], endtime=prefix['timelines'][0]['endtime']))
        return prefixesObjs

class BGP(RIPEStatRequestObj):
    def __init__(self, resource=None, timestamp=None):
        assert type(resource) == ASN or type(resource) == Prefix, 'Resource must be of type ASN/Prefix (or IP with full CIDR mask)'
        super(BGP, self).__init__(self, resource=resource, timestamp=timestamp)
        self.origin = self.resource
        self.resource = self.resource.resource_id
    
    def get_bgp_state(self, timestamp):
        # Gets the current BGP routing paths and communities for prefixes at a given time
        if timestamp is None:
            data = self.get_request(endpoints.BGP_STATUS(asn=self.resource))
        else:
            data = self.get_request(endpoints.BGP_STATUS(asn=self.resource, timestamp=timestamp))
        print(endpoints.BGP_STATUS(asn=self.resource, timestamp=timestamp))    
        route_list = data['bgp_state']
        records = []
        
        for target_prefix in route_list:
            target = target_prefix['target_prefix']
            path = target_prefix['path']
            comm = target_prefix['community']
            brecord = BGPRecord(source=self.origin, target=target, path=path, community=comm)
            records.append(brecord)

        return records    

    def get_bgp_announce(self, starttime, endtime):
        # Get the announce, withdraw, update messages from BGP in a given timeframe
        data =  self.get_request(endpoints.BGP_UPDATES(asn=self.resource, starttime=starttime, endtime=endtime))
        updates_list = data['updates']
        update_record_list = []
        for update in updates_list:
            update_attrs = update['attrs']
            source = update_attrs['source_id'].split('-').pop()
            update_record = BGPUpdateRecord(source=Prefix(source + '/32'), target=Prefix(update_attrs['target_prefix']), 
                                            path=update_attrs['path'], community=update_attrs['community'], 
                                            update_type=update['type'], time=update['timestamp'])
            update_record_list.append(update_record)
        return update_record_list
         

if __name__=='__main__':
    asn = ASN(2568)
    bgp = BGP(resource=asn)
    print(2568, ASN(2568).get_name())
    print(2568, [str(rec) for rec in bgp.get_bgp_announce(starttime='2023-01-01T12:00', endtime='2023-01-02T12:00')])
    print(2568, [str(prefix) for prefix in asn.get_announced_prefix('2023-07-02T16:00:00', '2023-07-16T16:00:00')])

    