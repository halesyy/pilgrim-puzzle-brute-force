import os
import json
import random
from datetime import datetime
startTime = datetime.now()

def clear():
    if os.name == 'nt':
        os.system('cls') #windows
    else:
        os.system('clear') #macos/linux
clear()


#// CONFIG VALUES
keep_score_lessthan = -30
field_size = 5
field      = []
points     = 0
operating_at = 0
human_control = False
print_spam = False #only print when there is a value found that meets criteria

for i in range(0, (field_size**2)):
    field.append("#")

def restart_game():
    global field
    global operating_at
    global points

    operating_at = 0
    points = 0

    for i in range(0, (field_size**2)):
        field[i] = '#'

def print_field():
    global field
    global operating_at
    b = 0 # external iteration
    for i in range(1, (field_size**2)+1):
        b = b + 1
        output = "o" if operating_at == i-1 else field[i-1]
        if b == field_size+1: #placing newline
            print("\n"+output, end=" ")
            b = 1
        else: #printing turf
            print(output, end=" ")

def format_field():
    global field
    global operating_at
    b = 0 # external iteration
    format = ""
    for i in range(1, (field_size**2)+1):
        b = b + 1
        output = "o" if operating_at == i-1 else field[i-1]
        if b == field_size+1: #placing newline
            format = format +"\n"+output
            b = 1
        else: #printing turf
            format = format + output
    return format

#// Checking if a point (anchor) equates to any characters
#// in the string provided (equals).
def point_check(anchor, equals):
    global operating_at
    mvms = {
        "w": field_size*-1,
        "s": field_size,
        "a": -1,
        "d": 1
    }
    movement_total = 0
    for movement in anchor:
        movement_total = movement_total + mvms[movement]
    # print("total is "+str(movement_total))
    #where we are checking
    checking_anchor = operating_at+movement_total
    is_equal = False
    for check_str in equals:
        if (len(field)-1) >= checking_anchor:
            if field[checking_anchor] == check_str:
                is_equal = True
    return is_equal

#// Checking if in a zonal range,
#// using simple modifiers.
def in_zone(start, by, multiply_by=1, add_in=0):
    in_zone = False
    #iterating by i
    for i in range(start, by):
        if operating_at == (i*multiply_by)+add_in:
            in_zone = True
    return in_zone

#//anchor=w/s/a/d
def is_corner(anchor):
    corner = False
    if point_check(anchor, "<>"):
        if point_check(anchor+"w", "v^") or point_check(anchor+"s", "v^"):
            corner = True
    if point_check(anchor, "^v"):
        if point_check(anchor+"a", "<>") or point_check(anchor+"d", "<>"):
            corner = True
    return corner

#// Giving the "allowed" decisions that
#// the user can make, and blocking un-usable
#// decisions to the user.
def possible_decisions():
    #going to check for laneways (on farleft)
    possible = []

    #// Left-movement check -> e.g. 0, 5, 10, 15
    # - x # # # #
    # - x # # # #
    # - x # # # #
    # - x # # # #
    # - x # # # #
    a = True
    if in_zone(0, field_size, field_size): a = False
    if a == True and point_check("a", "<>") == True: a = False
    if is_corner("a"): a = False
    if a == True: possible.append("a")

    #// Right-movement check
    # - # # # # x (4)
    # - # # # # x (9)
    # - # # # # x (14)
    # - # # # # x (19)
    # - # # # # x (24)
    d = True
    if in_zone(0, field_size, field_size, field_size-1): d = False
    if d == True and point_check("d", "<>") == True: d = False
    if is_corner("d"): d = False
    if d == True: possible.append("d")

    #// Up-movement check
    # - x x x x x (0, 1, 2, 3, 4)
    # - # # # # #
    # - # # # # #
    # - # # # # #
    # - # # # # #
    w = True
    if in_zone(0, field_size): w = False
    if w == True and point_check("w", "v^") == True: w = False
    if is_corner("w"): w = False
    if w == True: possible.append("w")

    #// Down-movement check
    # - # # # # #
    # - # # # # #
    # - # # # # #
    # - # # # # #
    # - x x x x x (20, 21, 22, 23, 24)
    s = True
    if in_zone((field_size**2)-field_size, (field_size**2)): s = False
    if s == True and point_check("s", "v^") == True: s = False
    if is_corner("s"): s = False
    if s == True: possible.append("s")

    return possible


def print_pd(value):
    print("Can you make this movement? "+str(value))


def decision(human=True):
    global keep_score_lessthan
    global operating_at
    global points
    global print_spam

    if print_spam:
        print("pd:"+str(possible_decisions())+", p: "+str(points)+", oa: "+str(operating_at), end=" ")

    if human:
        movement = input("\n: ")
    else:
        movements_possible = possible_decisions()
        if len(movements_possible) == 0:
            return False
        movement = random.choice(movements_possible)
        # rand_pick = random.random()
        # if rand_pick >= 0.60:
        #     movement = "w"
        # elif rand_pick >= 0.30:
        #     movement = "a"
        # elif rand_pick >= 0.15:
        #     movement = "a"
        # else:
        #     movement = "s"

    movement_changes = {
        "w": (field_size)*-1,
        "s": (field_size),
        "a": -1,
        "d": 1
    }
    movement_points = {
        "w": points/2,
        "s": points*2,
        "a": points-1,
        "d": points+1
    }
    movement_replaces = {
        "w": "^",
        "s": "v",
        "a": "<",
        "d": ">"
    }
    value = movement_changes[movement]
    #safety net
    if movement in possible_decisions():
        field[operating_at] = movement_replaces[movement]
        operating_at = operating_at + value
        points = movement_points[movement]
        if operating_at == (field_size**2)-1:
            if points <= keep_score_lessthan:
                print("score of "+str(points)+" at game "+str(games)+" within "+str(datetime.now() - startTime))
                scores_json = open("score.json", "r")
                scores = json.load(scores_json)
                scores_json.close()
                #add new data
                scores["scores"].append([{
                    "points": points,
                    "assortment": format_field(),
                    "operating_at": operating_at
                }])
                #put into table
                scores_json = open("score.json", "w+")
                scores_json.write(json.dumps(scores, indent=4, sort_keys=True))
                scores_json.close()
            restart_game()
            return True
        return True


#choice
game_running = True
games = 0
inf = True
while inf:
    restart_game()
    game_running = True
    games = games + 1
    while game_running:
        if human_control:
            clear()
            print_field()
        game_running = decision(human_control)
