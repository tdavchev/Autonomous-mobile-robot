"""
    author: Todor Davchev
    assessment #1 CS3023
    Description: Offline planning with A*. Odometry and sensor navigation used for physically solving the maze.
"""

import time, sys, cProfile
from robot_controller import robot
from copy import copy, deepcopy

grid = [[0, 1, 0, 0],
        [0, 0, 0, 1],
        [1, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 1],
        [0, 0, 0, 1],
        [1, 1, 0, 1]]
        
for z in range (len(grid)-1):
    print grid[z]
init = [0, 0]
print init[0]
goal = [len(grid)-1, len(grid[0])-2]
var = 0.0
delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right 
delta_name = ['^', '<', 'v', '>']
pasta = 0
cost = 1
speed = 98
pi = 3.14
left_duration = 0.0
right_duration = 0.0
left_time = 0.0
right_time = 0.0
frqngyl = []
speedo1 = 0.0
speedo2 = 0.0
check = 0
trackWidth = 65.0
wheelRadius = 32.5
blah = True

def repairME(r):    #advise taken from Cyril
    global val
    while True:
        try:
            left = sensors[13]
            right = sensors[15]
            center = sensors[14]
            break
        except Exception:
            print "I am in the EXCEPTION"
            r.connect
            time.sleep(5)
            val = read_sensors(r)
            break

# decide on time needed to turn a particular angle    
def divide(angle, speedy):
    global pi
    global left_duration
    t=((angle*(trackWidth*pi))/(2.0*pi*speedy*wheelRadius))*10.0
    return t

def cal(r):
    global speedo1
    global speedo2
    calibration = r.get_encoders()
    if(len(calibration) != 2):
        calibration = r.get_encoders()
        time.sleep(0.2) 
    speed1 = calibration[0]
    speed2 = calibration[1]
    speedo1 = float(speed1)/5.0
    speedo2 = float(speed2)/5.0
    left_speed = speed-4
    right_speed = speed
    left_duration2 = 5.0
    right_duration2 = 5.0
    time.sleep(0.1)
    r.set_motors(left_speed, left_duration2, right_speed, right_duration2)
    calibration = r.get_encoders()
    time.sleep(0.1) 	


def calibrate():
    global left_time
    global right_time
    global pi
    global frqngyl
    cal(r)
    left_time = divide((pi/2.0), speedo1)
    time.sleep(0.1)
    right_time = divide((pi/2.0), speedo2)
    time.sleep(0.1)
    frqngyl = [left_time, right_time]
    print "left duration",
    print left_time
    print "right duration",
    print right_time
    
#increased value right ... test proof
def turn_right():   #90deg turn
    global speed
    global frqnyl
    global right_duration
    global left_duration
    left_speed = 0
    right_speed = 0
    left_duration = frqngyl[0]
    right_duration = frqngyl[1]
    time.sleep(0.1)
    r.set_motors(speed-6, right_duration, -speed, left_duration)
    left_speed = speed-6
    right_speed = -speed
    time.sleep(right_duration)
    time.sleep(0.1)

def turn_left():    #90deg turn
    global speed
    global frqnyl
    global right_duration
    global left_duration
    left_speed = 0
    right_speed = 0
    left_duration = frqngyl[0]
    right_duration = frqngyl[1]
    time.sleep(0.1)
    r.set_motors(-(speed-4), right_duration, speed, left_duration)
    left_speed = -(speed-4)
    right_speed = speed
    time.sleep(right_duration)
    time.sleep(0.1)

def hundred_eighty():
    global speed
    global pi, trackWidth, wheelRadius
    global speedo1
    global speedo2
    left_speed = 0
    right_speed = 0
    lefty=((pi*(trackWidth*pi))/(2.0*pi*(speedo1)*wheelRadius))*10.0
    righty = ((pi*(trackWidth*pi))/(2.0*pi*(speedo2)*wheelRadius))*10.0
    time.sleep(0.1)
    r.set_motors(-(speed-4), lefty, speed, righty)
    left_speed = -(speed-4)
    right_speed = speed
    time.sleep(righty)
    time.sleep(0.1)

def go_back(dist):
    global speed
    global speedo1, speedo2
    global right_duration
    global left_duration
    global check
    real = 40.0 #distance checking for a wall
    if(dist >= real):
        left_speed = -(speed-4)
        right_speed = -speed
        left_duration = 10.0/speedo1
        right_duration = 10.0/speedo2
        time.sleep(0.2)
        r.set_motors(-(speed-4), right_duration, -speed, left_duration)
        left_speed = 0
        right_speed = 0
        time.sleep(right_duration)
        check = 1
        distance = 0.0
        
def read_sensors(r):
    global val
    r.setPT(90, 135)
    time.sleep(0.1)
    val = r.get_sensors() 
    if(len(val) != 16):
        time.sleep(1)
        val = r.get_sensors()
        repairME(r)
    return val
    
def go_block(r, dist = 30.0):   #go 30cm forward
    global speedo1, speedo2, speed, frqngyl
    right_duration = frqngyl[0]
    left_duration = frqngyl[1]
    distance = 0.0
    righty = (30.0/speedo1)/5.0
    lefty = (30.0/speedo2)/5.0
    while(distance <= dist):
        time.sleep(0.2)
        forward(r, righty, lefty)
        val = read_sensors(r)
        oldLeft = val[13]
        oldRight = val[15]
        leftAll = 0
        rightAll = 0
        for i in range(0,5):
            leftAll += val[13]
            rightAll += val[15]
        averageLeft = leftAll/5
        if(oldLeft - averageLeft >50):
            right(r,0.5)
        oldLeft = averageLeft
        averageRight = rightAll/5
        print "averageLeft is ", averageLeft
        print "averageRight is ", averageRight
        if(oldRight - averageRight > 50):
            print "going left for 2 seconds"
            left(r, 0.5)
        oldRight = averageRight
        if(averageLeft > (averageRight+50) and (averageLeft < averageRight+200) and (averageLeft > 200 and averageRight > 200)) or (averageLeft>450):
            print "going right because ", averageLeft, "is the value for the left and the right is ", averageRight
            right(r, 0.5)
            time.sleep(0.5)
        elif(averageRight > (averageLeft + 50) and (averageRight < averageLeft + 200) and (averageRight > 200 and averageLeft > 200)) or (averageRight>450):
            print "going left because ", averageLeft, " is the value for the left and the right is ", averageRight
            left(r, 0.5)
            time.sleep(0.5)
        distance += 30.0/5.0
    distance = 0.0
    
def forward(r, t1=0.2, t2= 0.2):
    global speed
    r.set_motors(speed-4, t1, speed, t2)
    time.sleep(t1)
    
def left(r, t=0.2): #adjust from walls
    global speed
    r.set_motors(-(speed-4), 0.2, speed, 0.2)
    time.sleep(0.2) 
     
def right(r, t=0.2):    #adjust from walls
    global speed
    r.set_motors(speed-4, 0.2, -speed, 0.2)
    time.sleep(0.2)

def connect():
    global r
    address = "localhost"
    if len(sys.argv) == 2:
        address = "robo-wifi"+sys.argv[1]+".csd.abdn.ac.uk"    
    r = robot()
    r.connect(address) 
        
def main():
    global r
    connect()
    calibrate()
    print "Do you wish to continue? y/n"
    ans = raw_input("> ")
    if (ans == "y"):
        search()
    elif(ans == "n"):
        r.disconnect()
    r.disconnect()

"""learned from CS3023 and Udacity
   a method which finds the right path and executes it
"""
def search():    
    global r, init, goal, pasta, frqngyl, check, speedo1, blah, right_duration, var
    left_duration = frqngyl[0]
    right_duration = frqngyl[1]
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1
    expand = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))] #represents how the maze has been expanded
    action = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))] #represents the action taken
    storage = [' ' for row in range((len(grid[0]))*len(grid))] #stores the right direction

    x = init[0]
    y = init[1]
    g = 0

    open = [[g, x, y]]

    found = False  # flag that is set when search is complete
    resign = False # flag set if we can't find expand
    count = 0

    while not found and not resign:
        if len(open) == 0:
            resign = True
            return 'fail'
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[1]
            y = next[2]
            g = next[0]
            expand[x][y] = count
            count += 1  
            if x == goal[0] and y == goal[1]:
                found = True
            else:
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            g2 = g + cost
                            open.append([g2, x2, y2])
                            closed[x2][y2] = 1
                            action[x2][y2] = i
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    x = goal[0]
    y = goal[1]
    policy[x][y] = '*'
    countme = 0
    #visible right direction
    while x != init[0] or y != init[1]:
        x2 = x - delta[action[x][y]][0]
        y2 = y - delta[action[x][y]][1]
        policy[x2][y2] = delta_name[action[x][y]]
        if (policy[x2][y2] == 'v'):
          storage[countme] = policy[x2][y2]  
        elif (policy[x2][y2] == '>'):
            storage[countme] = policy[x2][y2]
        elif (policy[x2][y2] == '<'):
            storage[countme] = policy[x2][y2]
        elif (policy[x2][y2] == '^'):
            storage[countme] = policy[x2][y2]
        x = x2
        y = y2
        countme += 1
    br = 0
    for i in range(len(storage)):
        if(storage[i] != ' '):
            br += 1
    temp2 = br-1
    blah = True
    dista = 0.0
    #movement
    while br >= 0 :
        if(storage[br-1] == 'v'):
            if(br-1 == temp2):
                print "I go v"
                go_block(r)
                time.sleep(0.1)
            elif(br-1 < temp2):
                if(storage[br-1] == storage[br]):
                    print "I go v "
                    go_block(r)
                    time.sleep(1)
                elif(storage[br-1] != storage[br]):
                    print "I go v and", storage[br], " is where I am coming from"
                    forward(r,1,1)
                    forward(r)
                    valba = read_sensors(r)
                    #check if there is a wall infront, if not go back jalf a block and turn
                    while((valba[14] < 350) and (valba[14] > 100) and blah):
                        forward(r)
                        dista += (0.2*speedo1)
                        go_back(dista)
                        valba = read_sensors(r)
                        if check == 1:
                            blah = False
                            time.sleep(0.1)
                    check = 0
                    #turn 90 deg
                    if(storage[br] == '>'):
                        print "from v go >"
                        #turn left!
                        turn_right()
                        time.sleep(0.1)
                        go_block(r,30.0)
                    elif(storage[br] == '<'):
                        print "from v go <"
                        #turn right!
                        turn_left()
                        time_sleep(0.1)
                        go_block(r,30.0)
                    elif(storage[br] == '^'):
                        #turn 180deg
                        hundred_eighty()
                        time.sleep(0.2)
                        
        elif(storage[br-1] == '>'):
            #go forward
            if(br-1 == temp2):
                print "I go >"
                go_block(r)
                time.sleep(0.1)
            elif(br-1 < temp2):
                if(storage[br-1] == storage[br]):
                    print "I go >"
                    go_block(r)
                    time.sleep(0.1)
                elif(storage[br-1] != storage[br]):
                    print "I go > and", storage[br], " is where I am coming from"
                    forward(r)
                    go_block(r,15)
                    forward(r)
                    valba = read_sensors(r)
                    time.sleep(0.2)
                    #check if there is a wall infront, if not go back jalf a block and turn
                    while((valba[14] < 350) and (valba[14] > 100) and blah):
                        forward(r)
                        dista += (0.2*speedo1)
                        time.sleep(0.1)
                        go_back(dista)
                        valba = read_sensors(r)
                        if check == 1:
                            blah = False
                            time.sleep(0.1)
                    check = 0
                    #turn 90 deg
                    if(storage[br] == 'v'):
                        print "from > go v"
                        #turn right!
                        turn_left()
                        time.sleep(0.2)
                        go_block(r,30.0)
                    elif(storage[br] == '^'):
                        print "from > go ^"
                        #turn left!
                        turn_right()
                        time.sleep(0.2)
                        go_block(r,30.0)
                    elif(storage[br] == '<'):
                        #turn 180deg
                        hundred_eighty()
                        time.sleep(0.2)
                            
                            
        elif(storage[br-1] == '<'):
            #go forward
            if(br-1 == temp2):
                go_block(r)
                time.sleep(0.1)
            elif(br-1 < temp2):
                if(storage[br-1] == storage[br]):
                    go_block(r)
                    time.sleep(0.1)
                elif(storage[br-1] != storage[br]):
                    forward(r)
                    go_block(r,15)
                    forward(r)
                    valba = read_sensors(r)
                    time.sleep(0.2)
                    #check if there is a wall infront, if not go back jalf a block and turn
                    while((valba[14] < 350) and (valba[14] > 100) and blah):
                        forward(r)
                        dista += (0.2*speedo1)
                        time.sleep(0.1)
                        go_back(dista)
                        valba = read_sensors(r)
                        if check == 1:
                            blah = False
                            time.sleep(0.1)
                    check = 0
                    #turn 90 deg
                    if(storage[br] == '^'):
                        #turn right!
                        turn_left()
                        time.sleep(0.2)
                        go_block(r,30.0)
                    elif(storage[br] == 'v'):
                        #turn left!
                        turn_right()
                        time.sleep(0.2)
                        go_block(r,30.0)
                    elif(storage[br] == '>'):
                        #turn 180deg
                        hundred_eighty()
                        time.sleep(0.2)
                        
        elif(storage[br-1] == '^'):
            #go forward
            if(br-1 == temp2):
                go_block(r)
                time.sleep(0.1)
            elif(br-1 < temp2):
                if(storage[br-1] == storage[br]):
                    go_block(r)
                    time.sleep(0.1)
                elif(storage[br-1] != storage[br]):
                    forward(r)
                    go_block(r,15)
                    forward(r)
                    valba = read_sensors(r)
                    time.sleep(0.2)
                    #check if there is a wall infront, if not go back jalf a block and turn
                    while((valba[14] < 350) and (valba[14] > 100) and blah):
                        forward(r)
                        dista += (0.2*speedo1)
                        time.sleep(0.1)
                        go_back(dista)
                        valba = read_sensors(r)
                        if check == 1:
                            blah = False
                            time.sleep(0.1)
                    check = 0
                    #turn 90 deg
                    if(storage[br] == '>'):
                        #turn left
                        turn_left()
                        time.sleep(0.2)
                        go_block(r,30.0)
                    elif(storage[br] == '<'):
                        #turn right
                        turn_right()
                        time.sleep(0.2)
                        go_block(r,30.0)
                    elif(storage[br] == 'v'):
                        #turn 180deg
                        hundred_eighty()
                        time.sleep(0.2)
                                         
        br -= 1
    # go one block forward to reach the goal
    go_block(r)
    for i in range(len(policy)):
        print policy[i]
    #reverse path
    temp = deepcopy(goal)
    goal = deepcopy(init)
    init = temp
    if (pasta == 0):
        print "Please, write -p if you want to find your path back"
        ans = raw_input("> ")
        if (ans == "-p"):
            hundred_eighty()
            go_block(r)
            time.sleep(0.2)
            print "Initialize going back"
            pasta = 1 
            search()
                    
                    
            


if __name__ == "__main__":
    main()
