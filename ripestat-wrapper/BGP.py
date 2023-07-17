class BGPRecord:
    def __init__(self, source, target, path, community) -> None:
        self.source = source
        self.target = target
        self.path = path
        self.community = community 

    def is_blackhole(self):
        assert self.community is not None, 'No community path detected'
        if '666' in ':'.join(self.community).split(':'):
            return True
        else:
            return False
        
    def get_origin_as(self):
        return self.path[-1]
        
    def path_length(self):
        return len(set(self.path))
        
    def __str__(self):
        return f'Subnet {self.source} to subnet {self.target} via {"->".join(self.path[::-1])}. Communities {self.community}'
    

class BGPUpdateRecord(BGPRecord):
    def __init__(self, update_type, time, source, target, path=None, community=None) -> None:
        super().__init__(source, target, path, community)
        self.type = update_type
        self.time = time
        self.path = list(map(str, self.path))

    def __str__(self):        
        if self.type == 'W':
            return f'WITHDRAW route from {self.source} to {self.target} at {self.time}'
        if self.type == 'A':
            return f'ANNOUNCE route from {self.source} to {self.target} at {self.time}. Path {"->".join(self.path[::-1])}. Communities {self.community}'

