import sys
import threading
import time

from agents.environment import Environment
from agents.cognitive_agent import CognitiveAgent
from resources.constants import DEFAULT_INPUT_FILE
from resources.utils import parse_file


# check parameters
if len(sys.argv) > 2:
    print "Invalid arguments. Usage: tile_world.py [input_file]"
    sys.exit(0)

input_file = DEFAULT_INPUT_FILE
if len(sys.argv) == 2:
    input_file = sys.argv[1]

# lock for stdout printing
lock = threading.Lock()

# read input_file
# N: the number of agents
# t: time that it takes to perform an operation on the environment
# T: total time of the simulation
# W, H: width and height of the grid
# colors: N colors of the agents
# pos: N zero-based integers - the initial positions of the agents
# obstacles: pairs of coordinates for obstacles
t, T, grid, agents = parse_file(input_file, lock)
#N = len(agents)

# run environment agent
threads = []
environment = Environment(t, T, grid, agents, lock)
thread = threading.Thread(target=environment.run)
thread.start()
threads.append(thread)

# run cognitive agent on different threads
for agent in agents:
    thread = threading.Thread(target=agent.run)
    thread.start()
    threads.append(thread)

# wait for T milliseconds
time.sleep(T)

for thread in threads:
    thread.join()

print "Done."
