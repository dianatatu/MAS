import json
import time
from time import localtime, strftime
from termcolor import cprint

from resources.constants import NONE_COLOR, TD, MESSAGES
from resources.kestrel_connection import KestrelConnection


class Environment():

    def __init__(self, t, T, grid, agents, lock):
        self.name = 'E-'
        self.t = t
        self.T = T
        self.grid = grid
        self.agents = agents
        self.points = {}
        self.queue_system = KestrelConnection(lock)
        self.lock = lock

    def run(self):
        while self.T > 0:
            #self.display_grid(self.grid)
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

    def respond_entire_state(self, requester):
        message = MESSAGES['response_entire_state']
        message.update({'grid': self.grid})
        self.send(requester, message)

    def send_the_end(self):
        message = MESSAGES['the_end']
        for agent in self.agents:
            self.send(agent.name, message)

    def check_mailbox(self):
        if self.queue_system.peek(self.name):
            return self.queue_system.fetch_from(self.name)
        return None

    def send(self, to, message):
        message.update({'from': self.name})
        r = self.queue_system.send_to(self.name, str(to), message)
        if r is False:
            self._safe_print('Sending message failed')

############################# DISPLAY #################################

    def display_grid(self, grid):
        self.lock.acquire()
        print '--------------------------------'
        for i in range(0, grid['H']):
            for j in range(0, grid['W']):
                self._display_cell(grid['cells'][i][j], self.agents)
            print ''
        print '--------------------------------'
        self.lock.release()

    def _display_cell(self, cell, agents):
        # display height
        if cell['color'] is not NONE_COLOR:
            cprint(' %d\t' % cell['h'], cell['color'], end='')
            return
        if cell['h'] < 0:
            # hole
            print('%d' % cell['h']),
        elif cell['h'] == 0:
            # tile
            print(' %d' % cell['h']),
        else:
            # obstacle
            print(' #'),
        # display agent
        for agent in agents:
            if agent.x == cell['x'] and agent.y == cell['y']:
                cprint(',%d$' % agent.points, agent.color, end='')
                if agent.carry_tile:
                    cprint(' *' % agent.carry_tile.color, end='')
        #display tiles
        if cell['tiles']:
            for tile in cell['tiles']:
                cprint('*', tile, end='')
        print('\t'),

    def _safe_print(self, message):
        self.lock.acquire()
        print message
        self.lock.release()