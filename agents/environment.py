import time

from resources.constants import ENVIRONMENT
from resources.utils import display_cell

class Environment():

    def __init__(self, t, T, grid, agents, stdout_lock, queue_system):
        self.name = ENVIRONMENT
        self.t = t
        self.T = T
        self.grid = grid
        self.agents = agents
        self.points = {}
        self.queue_system = queue_system
        self.stdout_lock = stdout_lock

    def run(self):
        while self.T > 0:
            self.display_grid(self.grid)
            message = self.check_mailbox()
            if message:
                if message['type'] == 'request_entire_state':
                    self.respond_entire_state(message['from'])
                self.T = self.T - self.t
            else:
                self.T = self.T - 1
            time.sleep(1)

        self.send_the_end()

########################### COMMUNICATION ###########################

    def check_mailbox(self):
        if self.queue_system.peek(self.name):
            return self.queue_system.fetch_from(self.name)
        return None

    def send(self, to, message):
        message.update({'from': self.name})
        r = self.queue_system.send_to(self.name, str(to), message)
        if r is False:
            self._safe_print('Sending message failed')

    def respond_entire_state(self, requester):
        message = {
            'type': 'response_entire_state',
            'grid': self.grid
        }
        self.send(requester, message)

    def send_the_end(self):
        message = {'type': 'the_end'}
        for agent in self.agents:
            self.send(agent.name, message)


############################# DISPLAY #################################

    def display_grid(self, grid):
        self.stdout_lock.acquire()
        print '--------------------------------'
        for i in range(0, grid['H']):
            for j in range(0, grid['W']):
                display_cell(grid['cells'][i][j], self.agents)
            print ''
        print '--------------------------------'
        self.stdout_lock.release()

    def _safe_print(self, message):
        self.stdout_lock.acquire()
        print message
        self.stdout_lock.release()