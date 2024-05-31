from mcrcon import MCRcon

class RCONAdmin:
    def __init__(self, host, password):
        self.admin = MCRcon(host, password)
    
    def command(self, command):
        self.admin.connect()
        resp = self.admin.command(command)
        self.admin.disconnect()
        return resp
    
    def playerlist(self):
        resp = self.command("playerlist")
        resp = resp.split("\n")[1:-1]
        players = []
        for i in resp:
            tmplist = i.split('§')
            players.append(tmplist[-1][1:])

        return players


