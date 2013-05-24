class Cell():

    def __init__(self, x, y, h, color, tiles=None, agents=None):
        self.x = x
        self.y = y
        self.h = h
        self.color = color
        if tiles:
            self.tiles = tiles
        else:
            self.tiles = []
        if agents:
            self.agents = agents
        else:
            self.agents = []

    def __unicode__(self):
        return '(%s,%s) -> %s' % (self.x, self.y, self.h)

    def put_tile(self):
        if self.h >= 0:
            print "Tile does not allow any more tiles."
            return
        self.h = self.h + 1
