from mcrcon import MCRcon

class RCONAdmin:
    def __init__(self, host, password):
        self.admin = MCRcon(host, password)
    
    def command(self, command):
        self.admin.connect()
        resp = self.admin.command(command)
        self.admin.disconnect()
        return resp


