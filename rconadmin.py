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
        resp = self.command("tsplist")
        players = resp.split("|")

        return players
    
    def givedoc(self, player, document):
        self.command(f"givedoc {player} {document}")

    def giveweapon(self, player, weapon):
        command = f"qa give {weapon} {player}"
        self.command(command)

    def giveitem(self, player, item):
        command = f"give {player} {item} 1"
        print(command)
        self.command(command)

