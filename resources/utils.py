from copy import copy

from agents.cognitive_agent import CognitiveAgent
from constants import OBSTACLE_HEIGHT, NONE_COLOR
from resources.cell import Cell


def parse_file(input_file,lock):
    """ Returns all necessary values parsed from the input file."""

    f = open(input_file, 'r')
    l = f.read().split()

    N, t, T, W, H = [int(x) for x in l[:5]]
    colors = l[5:5+N]
    pos = []
    for i in range(5+N, 5+3*N, 2):
        pos.append((int(l[i]), int(l[i+1])))

    # skip 'OBSTACLES' token
    index = 5+3*N+1
    obstacles = []
    while l[index] != 'TILES':
        obstacles.append((int(l[index]), int(l[index+1])))
        index = index + 2

    # skip 'TILES' token
    index = index + 1
    tiles = []
    while l[index] != 'HOLES':
        tiles.append((int(l[index]), l[index+1], int(l[index+2]), int(l[index+3])))
        index = index + 4

    # skip 'HOLES' token
    index = index + 1
    holes = []
    while index != len(l):
        holes.append((int(l[index]), l[index+1], int(l[index+2]), int(l[index+3])))
        index = index + 4

    f.close()

    agents = []
    for i in range(0, N):
        agents.append(CognitiveAgent(i, pos[i][0], pos[i][1], colors[i], lock))

    grid = {}
    grid['H'] = H
    grid['W'] = W
    grid['cells'] = []
    for i in range(0, W):
        grid['cells'].append([])
    for i in range(0, H):
        for j in range(0, W):
            h = get_height(i, j, obstacles, holes)
            color = get_color(i, j, holes)
            cell_tiles = get_tiles(i, j, tiles)
            cell_agents = get_agents(i, j, agents)
            grid['cells'][i].append(Cell(i, j, h, color, cell_tiles, cell_agents).__dict__)

    return (t, T, grid, agents)


def get_height(i, j, obstacles, holes):
    """Returns the height of the cell on line i and column j.

    If the cell is an obstacle, then its height will be OBSTACLE_HEIGHT.
    If the cell is a hole, then its height will be negative.
    Otherwise, the cell's height is 0.
    """
    for obs in obstacles:
        if obs[0] == i and obs[1] == j:
            return OBSTACLE_HEIGHT
    for hole in holes:
        if hole[2] == i and hole[3] == j:
            return 0-hole[0];
    return 0;


def get_color(i, j, holes):
    """Returns the color of the cell on line i and column j.

    If the cell is a hole, then its color will be set by the hole's color.
    Otherwise, the cell has no color.
    """
    for hole in holes:
        if hole[2] == i and hole[3] == j:
            return hole[1];
    return NONE_COLOR


def get_tiles(i, j, tiles):
    """Returns all tiles corresponding to a single cell from grid.
    (the one from line i and column j).
    """
    cell_tiles = []
    for tile in tiles:
        if tile[2] == i and tile[3] == j:
            for _ in range(0, tile[0]):
                cell_tiles.append(tile[1])
    return cell_tiles

def get_agents(i, j, agents):
    """Returns all agents situated on a (i, j) tile."""
    cell_agents = []
    for agent in agents:
        if agent.x == i and agent.y == j:
            agent_data = copy(agent.__dict__)
            agent_data.pop('queue_system')
            agent_data.pop('lock')
            cell_agents.append(agent_data)
    return cell_agents
