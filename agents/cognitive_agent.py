from resources.constants import ENVIRONMENT



class CognitiveAgent():

    def __init__(self, name, x, y, color, stdout_lock, queue_system):
        self.points = 0
        self.carry_tile = None
        self.name = 'A%s' % name
        self.x = x
        self.y = y
        self.color = color
        self.queue_system = queue_system
        self.stdout_lock = stdout_lock

    def __unicode__(self):
        return '<%s, (%s,%s) -> %s>' % (self.name, self.x, self.y, self.color)

    def run(self):
        self.request_entire_state()
        # wait for entire state response
        while True:
            if self.queue_system.peek(self.name):
                message = self.queue_system.fetch_from(self.name)
                if message and message['type'] == 'response_entire_state':
                    grid = message['grid']
                    break

        # get the most efficient plan
        plans = self.get_most_efficient_plan(grid)

        while True:
            message = self.check_mailbox()
            if message:
                if message['type'] == 'the_end':
                    break
                if message['type'] == 'response_entire_state':
                    grid = message['grid']
            

########################### COMMUNICATION ###########################

    def request_entire_state(self):
        message = {'type': 'request_entire_state'}
        self.send(ENVIRONMENT, message)

    def check_mailbox(self):
        if self.queue_system.peek(self.name):
            return self.queue_system.fetch_from(self.name)
        return None

    def send(self, to, message):
        # Sign message.
        message.update({'from': self.name})
        # Send message.
        r = self.queue_system.send_to(self.name, to, message)
        if r is False:
            self._safe_print('Sending message failed')


########################### ACTIONS ###########################

    def pickup(self, tile):
        if self.carry_tile:
            self._safe_print("Agent already has picked up a tile.")
            return
        self.carry_tile = tile

    def drop(self, tile):
        if not self.carry_tile:
            self._safe_print("Agent has no picked up tile.")
            return
        self.carry_tile = None


########################## UTILS ##############################

    def get_most_efficient_plan(self, grid):
        pass

    def _safe_print(self, message):
        self.stdout_lock.acquire()
        print message
        self.stdout_lock.release()

