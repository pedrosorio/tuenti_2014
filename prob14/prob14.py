from math import sqrt
from collections import defaultdict
from copy import deepcopy

#modify the graph by applying the ford-fulkerson algorithm
#i.e. introducing edges between all pairs of nodes
def ford_fulkerson(graph):
  for frm in graph:
    for to in graph:
      if to == frm:
        continue
      if to not in graph[frm]:
        graph[frm][to] = 1e12
  for step in graph:
    for frm in graph:
      if step == frm:
        continue
      for to in graph:
        if to == frm or step == to:
          continue
        if graph[frm][to] > graph[frm][step] + graph[step][to]:
          graph[frm][to] = graph[frm][step] + graph[step][to]


#fancy classes (lol)
class Wagon():
  def __init__(self, dest, value):
    self.dest = dest
    self.value = value
    self.dist = 0

class Station():
  def __init__(self, line):
    fields = line.split()
    self.name = fields[0]
    self.coords = map(int, fields[1].split(","))
    self.wagons = set([Wagon(fields[2], int(fields[3]))])

  def distance(self, station):
    return sqrt(sum([(station.coords[i] - self.coords[i])**2 for i in xrange(2)]))

class Route():
  def __init__(self, line, F, station_dict):
    fields = line.split()
    self.train = [fields[0], F]
    self.last_carry = -1
    self.graph = defaultdict(dict)
    for conn in fields[1:]:
      frm, to = conn.split("-")
      dist = station_dict[frm].distance(station_dict[to])
      self.graph[frm][to] = dist
      self.graph[to][frm] = dist
    #Ford-Fulkerson
    ford_fulkerson(self.graph)
    self.min_dists = {}
    for frm in self.graph:
      self.min_dists[frm] = min([v for k,v in self.graph[frm].items()])


#simple silly backtrack - should have used C++ =)
#every time a move is decided the train can go to any
#node in the route, but must not move the same wagon (or go empty)
#two times in a row
#No wagon is ever taken to the same station twice
#The trains move in "sequences" and we only switch between trains
#when a train has exhausted fuel or left a wagon in a station that is
#shared by the routes
#Also prune a lot of branches by computing an upper bound to the value
#that can be obtained from the remaining wagons using their distances to
#the destinations and the total fuel in the trains
#It's a pretty loose upper bound but this alone has a huge effect on the time
def explore(value, last_move):
  global global_best, routes, stations, station_dict, wagons_past, all_pairs, wagons_sorted
  best_val = value
  if best_val > global_best:
    global_best = best_val
  else:
    #compute upper bound of value that can be achieved
    #the problem of getting the value from the remaining wagons (which were sorted by value previously)
    #is dealt with efficiently as a continuous relaxation of the corresponding knapsack problem
    upper_bound = value
    total_fuel = sum([route.train[1] for route in routes])
    i = len(wagons_sorted) - 1
    while i >= 0 and total_fuel > 0 and upper_bound <= global_best:
      wagon_value, wagon_dist = wagons_sorted[i].value, wagons_sorted[i].dist
      if wagon_value == 0:
        i -= 1
        continue
      fuel_spend = min(total_fuel, wagon_dist)
      upper_bound += wagon_value * fuel_spend/wagon_dist
      total_fuel -= fuel_spend
      i -= 1
    if upper_bound <= global_best:
      return value


  #for each train
  for route in routes:
    #check if the train in this route can move or we should continue moving the other one
    last_move_route, last_move_name, swap = last_move
    if id(last_move_route) != id(route):
      if last_move_route != -1:
        if swap:
          if last_move_name not in route.graph:
            continue
        elif last_move_route.train[1] >= last_move_route.min_dists[last_move_name]:
          continue
    cur_name = route.train[0]
    cur_fuel = route.train[1]
    if cur_fuel < route.min_dists[cur_name]:
      continue
    cur_station = station_dict[cur_name]
    cur_last_carry = route.last_carry
    #for all the stations that can be reached by this train
    for dest_name, dist in route.graph[cur_name].items():
      if dist > cur_fuel:
        continue
      dest_station = station_dict[dest_name]
      #move the train to the destination, discounting fuel
      route.train[0] = dest_name
      route.train[1] -= dist
      cur_wagons = list(cur_station.wagons)
      #what happens if we try to take each of the wagons at the current station
      #with us?
      for wagon in cur_wagons:
        if cur_last_carry == id(wagon):
          continue
        wagon_hash = (id(wagon), id(dest_station))
        #ensure the wagon has never been at the destination station
        if wagon_hash in wagons_past:
          continue
        #record in the logs that the wagon has visited the destination
        #and take it from the current station
        wagons_past.add(wagon_hash)
        cur_station.wagons.remove(wagon)
        route.last_carry = id(wagon)
        #if the destination is the goal of the wagon, add the value but
        #don't place the wagon at the destination (we're done with it)
        if wagon.dest == dest_name:
          wagon.dist = 0
          cur_wagon_value = wagon.value
          wagon.value = 0
          best_val = max(best_val, explore(value + cur_wagon_value, (route, dest_name, False)))
          wagon.value = cur_wagon_value
        #otherwise, place the wagon at the destination
        else:
          wagon.dist = all_pairs[dest_name][wagon.dest]
          dest_station.wagons.add(wagon)
          best_val = max(best_val, explore(value, (route, dest_name, True)))
          dest_station.wagons.remove(wagon)
        #put everything as it was to test another branch
        wagons_past.remove(wagon_hash)
        cur_station.wagons.add(wagon)
        route.last_carry = cur_last_carry
        wagon.dist = all_pairs[cur_name][wagon.dest]
      #also, attempt to move the train without transporting wagons
      if cur_last_carry != 0:
        route.last_carry = 0
        best_val = max(best_val, explore(value, (route, dest_name, False)))
        route.last_carry = cur_last_carry
      #move the train to where it was to attempt another branch
      route.train[0] = cur_name
      route.train[1] = cur_fuel
  return best_val

N = int(raw_input())
for test in xrange(N):
  S,R,F = map(int,raw_input().split(","))
  stations = [Station(raw_input()) for i in xrange(S)]
  station_dict = {}
  for station in stations:
    station_dict[station.name] = station
  routes = [Route(raw_input(), F, station_dict) for i in xrange(R)]
  wagons_past = set()
  for station in stations:
    wagons_past.add((id(list(station.wagons)[0]), id(station)))


  all_pairs = defaultdict(list)
  for route in routes:
    for frm in route.graph:
        all_pairs[frm].extend(route.graph[frm].copy().items())
  for frm in all_pairs:
    all_pairs[frm] = dict(all_pairs[frm])

  ford_fulkerson(all_pairs)

  wagons_sorted = sorted([[wagon, all_pairs[station.name][wagon.dest]] for station in stations for wagon in station.wagons], key = lambda x : x[0].value)
  for wagon in wagons_sorted:
    wagon[0].dist = wagon[1]
  wagons_sorted = [wagon[0] for wagon in wagons_sorted]


  global_best = 0
  print explore(0, (-1, -1, False))
