import sys; args=sys.argv[1:]
from math import pi, acos, sin, cos
from tkinter import *
from PIL import Image, ImageTk
beginning = args[0]
end = args[1]

rawLoc = open('rrNodes.txt', 'r').read().splitlines()
rawEdges = open('rrEdges.txt', 'r').read().splitlines()
rawCities = open('rrNodeCity.txt', 'r').read().splitlines()
locations = {} #get (lat, long) of a station
edges = {} #get the set of edges that a city maps to
cities = {} #get the city of a station
stations = {} #get the station id of a city
for s in rawLoc:
    loc = s.split()
    locations[loc[0]] = (float(loc[1]), float(loc[2]))
for s in rawEdges:
    e = s.split()
    if e[0] not in edges:
        edges[e[0]] = set()
    edges[e[0]].add(e[1])
    if e[1] not in edges:
        edges[e[1]] = set()
    edges[e[1]].add(e[0])
for s in rawCities:
    stationid = s[:7]
    c = s[8:]
    cities[stationid] = c
    stations[c] = stationid

def calcDist(s1, s2):
    r = 3958.76 # in miles, equivalent to 6371 km
    y1 = locations[s1][0]*pi/180.0
    x1 = locations[s1][1]*pi/180.0
    y2 = locations[s2][0]*pi/180.0
    x2 = locations[s2][1]*pi/180.0
    return acos(sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1)) * r #law of cosines

def aStar(start, goal):
    if start == goal: return [start]
    openSet = [(calcDist(start,goal), 0, start, None)] #estimate, cumulative distance, station, parent
    closedSet = {}
    while True:
        p = openSet[0]
        idx = len(openSet)-1
        openSet[0] = openSet[idx]
        openSet.pop(idx)
        idx = 0
        while idx<(len(openSet)-1)//2:
            newidx = 2*idx+2
            if openSet[2*idx+1]<openSet[newidx]: newidx = 2*idx+1
            if openSet[newidx]>openSet[idx]: break
            openSet[idx], openSet[newidx] = openSet[newidx], openSet[idx]
            idx = newidx
        if p[2] in closedSet: continue
        closedSet[p[2]] = (p[3], p[1]) #maps to parent, cumulative dist
        if p[2] == goal: return closedSet
        for nbr in edges[p[2]]:
            if nbr in closedSet: continue
            element = (calcDist(nbr,goal)+p[1]+calcDist(p[2],nbr),calcDist(p[2],nbr)+closedSet[p[2]][1],nbr,p[2])
            idx = len(openSet) #adds nbr to openset
            openSet.append(element)
            while idx>0 and openSet[(newidx := (idx-1)//2)]>element:
                openSet[idx], openSet[newidx] = openSet[newidx], element
                idx = newidx

def heapAdd(lst, element):
    idx = len(lst)
    lst.append(element)
    while idx>0 and lst[(newidx := (idx-1)//2)]>element:
        lst[idx], lst[newidx] = lst[newidx], element
        idx = newidx
    return lst

def heapRemove(lst):
    idx = len(lst)-1
    lst[0] = lst[idx]
    lst.pop(idx)
    idx = 0
    while idx<(len(lst)-1)//2:
        newidx = 2*idx+2
        if lst[2*idx+1]<lst[newidx]: newidx = 2*idx+1
        if lst[newidx]>lst[idx]: break
        lst[idx], lst[newidx] = lst[newidx], lst[idx]
        idx = newidx
    return lst

def path(start, goal, closedSet):
    toRet = [goal]
    p = goal
    while p!=start:
        p = closedSet[p][0]
        toRet.append(p)
    return toRet[::-1]

def dist(goal, closedSet):
    return closedSet[goal][1]

def printablePath(path):
    return ' '.join(station for station in path)

start, goal = stations[beginning], stations[end]
closedSet = aStar(stations[beginning], stations[end])
print(f'Path: {printablePath(path(start, goal, closedSet))}')
print(f'Distance: {dist(goal, closedSet)} mi')