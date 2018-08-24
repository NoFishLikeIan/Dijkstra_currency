import pandas as pd
import numpy as np
import collections
import math
import sys
import heapq

import time
from forex_python.converter import CurrencyRates
import pdb

currency_codes = ['EUR', 'USD', 'GBP', 'JPY', 'CNY', 'INR', 'AUD']


def get_currency(list_codes, sleeping=0):
    print('Lazy-search for real time rates')
    c = CurrencyRates()
    rate_matrix = np.zeros((len(list_codes), len(list_codes)))

    for n, currency in enumerate(list_codes):
        print(f'Rate {n+1} out of {len(list_codes)}')
        for m, other_currency in enumerate(list_codes):
            rate = c.get_rate(currency, other_currency)
            time.sleep(sleeping)
            rate_matrix[m][n] = rate

    df_rates = pd.DataFrame(rate_matrix, index=list_codes, columns=list_codes)
    return df_rates

# Stolen from http://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php


matrix = np.log(get_currency(currency_codes))


class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        self.distance = sys.maxsize
        self.visited = False
        self.previous = None

    def __lt__(self, other):
        return self.distance < other.distance

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.id)


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous


def shortest(v, path):
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return


def dijkstra(aGraph, start, target):
    print(f'Calculating shortest from {start.get_id()} to {target.get_id()}')
    start.set_distance(0)

    unvisited_queue = []
    for v in aGraph:
        heapq.heappush(unvisited_queue, (v.get_distance(), v))

    while len(unvisited_queue):
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        for nxt in current.adjacent:
            if nxt.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(nxt)

            if new_dist < nxt.get_distance():
                nxt.set_distance(new_dist)
                nxt.set_previous(current)
                print(
                    f'Updated: current = {current}, nxt = {nxt}, new_dist = {new_dist}')

            else:
                print(
                    f'Not updated: current = {current}, nxt = {nxt}, new_dist = {new_dist}')

        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)

        unvisited_queue = []
        for v in aGraph:
            if not v.visited:
                heapq.heappush(unvisited_queue, (v.get_distance(), v))


g = Graph()
currency_list = matrix.columns.values.tolist()

for cur in currency_list:
    g.add_vertex(cur)
    for other_cur in [c for c in currency_list if c != cur]:
        g.add_edge(cur, other_cur, cost=matrix[cur][other_cur])


def get_distance(a, b, g):
    return g.get_vertex(a).adjacent[g.get_vertex(b)]


def get_path(a='EUR', b='USD'):

    dijkstra(g, g.get_vertex(a), g.get_vertex(b))
    target = g.get_vertex(b)
    path = [target.get_id()]
    shortest(target, path)
    print(f'The shortest path {path[::-1]}')

    straight_distance = get_distance(a, b, g)
    actual_distance = 0

    for n in range(len(path) - 1):
        actual_distance += get_distance(path[n + 1], path[n], g)

    print(
        f'The straight distance: {straight_distance} and the optimum distance: {actual_distance}')


if __name__ == '__main__':
    a = input('Type the first currency\n').replace(' ', '').upper()
    if a not in currency_codes:
        raise AssertionError(f'Currency {a} not available')
    b = input('Type the second currency\n').replace(' ', '').upper()
    if b not in currency_codes:
        raise AssertionError(f'Currency {b} not available')

    get_path(a, b)
