#import sys; args=sys.argv[1:]
from math import pi, acos, sin, cos, log
from tkinter import *
from PIL import Image, ImageTk
import time

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
    return acos(min(1, sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1))) * r #law of cosines

def aStar(start, goal):
    if start == goal: return [start]
    openSet = [(calcDist(start,goal), 0, start, None)] #estimate, cumulative distance, station, parent
    closedSet = {}
    timeSinceUpdate = time.time()
    updateInterval = (calcDist(start, goal)/10000)**2 #updates canvas based on how far away goal is
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
        if p[2] in closedSet:
            timeSinceUpdate = drawClosedSet(p[2], closedSet[p[2]][0], timeSinceUpdate, updateInterval)
            continue
        closedSet[p[2]] = (p[3], p[1]) #maps to parent, cumulative dist
        if p[3]: timeSinceUpdate = drawClosedSet(p[2], p[3], timeSinceUpdate, updateInterval)
        if p[2] == goal: return closedSet
        for nbr in edges[p[2]]:
            if nbr in closedSet:
                timeSinceUpdate = drawClosedSet(p[2], nbr, timeSinceUpdate, updateInterval)
                continue
            element = (calcDist(nbr,goal)+p[1]+calcDist(p[2],nbr),calcDist(p[2],nbr)+closedSet[p[2]][1],nbr,p[2])
            idx = len(openSet) #adds nbr to openset
            openSet.append(element)
            timeSinceUpdate = drawOpenSet(p[2],nbr, timeSinceUpdate, updateInterval)
            while idx>0 and openSet[(newidx := (idx-1)//2)]>element:
                openSet[idx], openSet[newidx] = openSet[newidx], element
                idx = newidx

def path(start, goal, closedSet):
    toRet = [goal]
    p = goal
    #timeSinceUpdate = time.time()
    #updateInterval = dist(goal, closedSet)/100000
    while p!=start:
        canvas.create_line(*canvasCoords(p), *canvasCoords(closedSet[p][0]), width=3, fill='green')
        p = closedSet[p][0]
        toRet.append(p)
        #if time.time()-timeSinceUpdate > updateInterval:
        #    canvas.update()
        #    timeSinceUpdate = time.time()
    canvas.update()
    return toRet[::-1]

def dist(goal, closedSet):
    return closedSet[goal][1]

def printablePath(path):
    return ' '.join(station for station in path)

def canvasCoords(station): #tells canvas where to plot the city
    lat = locations[station][0]*pi/180
    long = locations[station][1]*pi/180
    x = 815*((long+pi)) - 586
    y = 820*((pi-log(sin(pi/4+lat/2)/cos(pi/4+lat/2)))) - 1649
    return [x, y]

def drawOpenSet(s1, s2, timeSinceUpdate, updateInterval):
    #time.sleep(delay)
    canvas.create_line(*canvasCoords(s1), *canvasCoords(s2), width=2, fill='red')
    if time.time()-timeSinceUpdate>updateInterval: #only updates canvas after a given amount of time
        canvas.update()
        return time.time()
    return timeSinceUpdate

def drawClosedSet(s1, s2, timeSinceUpdate, updateInterval):
    #time.sleep(delay)
    canvas.create_line(*canvasCoords(s1), *canvasCoords(s2), width=2, fill='blue')
    if time.time()-timeSinceUpdate>updateInterval:
        canvas.update()
        return time.time()
    return timeSinceUpdate

def drawAllEdges():
    for elem in edges:
        for edge in edges[elem]:
            canvas.create_line(*canvasCoords(elem), *canvasCoords(edge), width=1, fill='orange')
    canvas.update()

def doAStar():
    start = startG.get()
    goal = goalG.get()
    canvas.create_rectangle(890, 460, 1210, 580, outline='white', fill='white')
    label1 = Label(root)
    label1.config(text=f'\nFinding a path from \n {start} to {goal}\n')
    label1.config(font=('helvetica', 15))
    label1.config(bg='white')
    canvas.create_window(1050, 520, window=label1)
    
    closedSet = aStar(stations[start], stations[goal])
    canvas.create_rectangle(890, 480, 1210, 560, outline='white', fill='white')
    path(stations[start], stations[goal], closedSet)
    label1.config(text=f'Path of length {round(dist(stations[goal], closedSet),2)} miles \n found from {start} \n to {goal}')
    #label1.config(font=('helvetica', 15))
    #label1.config(bg='white')
    #canvas.create_window(1050, 520, window=label1)

root = Tk()
canvas = Canvas(root, width = 1223, height = 700, bg = 'white')
canvas.pack(expand = YES, fill = BOTH)

image = Image.open("rrMap.png")
img = ImageTk.PhotoImage(image)
canvas.create_image(0, -100, image = img, anchor = NW)
drawAllEdges()
#canvas.create_rectangle(1040, 310, 1200, 490, outline="#ddd", fill="#ddd")
OPTIONS = [*stations]

labelStart = Label(root, text=f'Enter start:')
labelStart.config(font=('helvetica', 12))
canvas.create_window(1120, 300, window=labelStart)
startG = StringVar(root)
startG.set(OPTIONS[0]) # default value
smenu = OptionMenu(root, startG, *OPTIONS)
canvas.create_window(1120, 330, window=smenu)

labelEnd = Label(root, text=f'Enter destination:')
labelEnd.config(font=('helvetica', 12))
canvas.create_window(1120, 370, window=labelEnd)
goalG = StringVar(root)
goalG.set(OPTIONS[0]) # default value
emenu = OptionMenu(root, goalG, *OPTIONS)
canvas.create_window(1120, 400, window=emenu)

button = Button(root, text="Find Path", command=doAStar)
canvas.create_window(1120, 440, window=button)
canvas.update()

canvas.mainloop()