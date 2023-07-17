import ipaddress

class Prefix:
    def __init__(self, ip, starttime=None, endtime=None):
        if '/' not in ip:
            raise TypeError("IP requires CIDR notation 255.255.255.255/32")
        
        ip_mask = ip.split('/')
        self.cidr_mask = ip_mask.pop()
        self.ip = ip_mask[0]
        self.starttime = starttime
        self.endtime = endtime
        self.resource_id = self.ip # resource as a string
        assert ipaddress.ip_address(self.ip)
        
    def get_ip_base(self):
        # Gets the prefix IP
        return self.ip
    
    def get_mask(self):
        # Gets the CIDR mask
        return self.cidr_mask

    def get_ips(self):
        if self.cidr_mask == 32:
            return (self.get_ip_base, self.get_ip_base)
        network_ips = [str(ip) for ip in ipaddress.IPv4Network(self.ip + '/' + self.cidr_mask, strict=False)]
        return network_ips
    
    def get_range(self):
        network_ips = self.get_ips()
        # Gets the range of the CIDR IP
        if self.cidr_mask == 32:
            return (self.ip, self.ip)
        return network_ips[0], network_ips[-1]
    
    def __str__(self) -> str:
        if self.starttime is not None and self.endtime is not None:
            return f'Prefix {self.ip + "/" + self.cidr_mask} announced from {self.starttime} to {self.endtime}'
        else:
            return f'Prefix {self.ip}'

class IPv4(Prefix):
    def __init__(self, ip, starttime=None, endtime=None):
        ip_mask = int(ip.split('/').pop())
        if ip_mask == 32 and type(ipaddress.ip_address(ip)) == ipaddress.IPv4Address or \
            ip_mask == 64 and type(ipaddress.ip_address(ip)) == ipaddress.IPv6Address:
            super().__init__(ip, starttime, endtime)

        else:
            raise TypeError('Invalid IPv4 address. Check CIDR mask must be 32 or 64')
    
    def __str__(self) -> str:
        return self.ip
    
class IPv6(Prefix):
    def __init__(self, ip, starttime=None, endtime=None):
        ip_mask = int(ip.split('/').pop())
        if ip_mask == 64 and type(ipaddress.ip_address(ip)) == ipaddress.IPv6Address:
            super().__init__(ip, starttime, endtime)
        else:
            raise TypeError('Invalid IPv6 address. Check CIDR mask must be 64')
    
    def __str__(self) -> str:
        return self.ip

    
if __name__ =='__main__':
    ip_obj = Prefix('98.252.230.49/18')
    print(ip_obj.get_range())





        


        
    