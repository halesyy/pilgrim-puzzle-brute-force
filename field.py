import os
def clear():
    os.system('cls') #change to cls when on macosx or linux
clear()

field_size = 5
field      = []
debt       = 0
operating_at = 4 #the index point where the current action is taking place
for i in range(0, (field_size**2)):
    field.append("#")

def print_field():
    #from 1->end+1 since we're doing even division
    #for mod check
    b = 0 # external iteration
    for i in range(1, (field_size**2)+1):
        b = b + 1
        output = "o" if operating_at == i-1 else field[i-1]

        if b == field_size+1: #placing newline
            print("\n"+output, end=" ")
            b = 1
        else: #printing turf
            print(output, end=" ")

#heavy, needs re-visiting
def possible_decisions():
    #going to check for laneways (on farleft)
    possible = []
    #LEFT CHECK
    a = True
    for i in range(0, field_size):#checking for farleft corner
        if operating_at == i*field_size:#is at farleft corner
            a = False
    if a == True:#somewhere NOT on farleft
        if field[operating_at-1] == '<' or field[operating_at-1] == '>':
            a = False
    # print_pd(a)
    if a == True:
        possible.append("a")
    #RIGHT CHECK
    d = True
    for i in range(0, field_size):#checking for farright corner
        if operating_at == (i*field_size)+(field_size-1):#is at farright corner
            d = False
    if d == True:#somewhere NOT on farright
        if field[operating_at+1] == '<' or field[operating_at+1] == '>':
            d = False
    if d == True:
        possible.append("d")
    #UP CHECK
    w = True
    for i in range(0, field_size):#checking for fartop corner
        if operating_at == (i):#is at fartop corner
            w = False
    if w == True:#somewhere NOT on fartop
        if field[operating_at+(field_size*-1)] == '^' or field[operating_at+(field_size*-1)] == 'v':
            w = False
    if w == True:
        possible.append("w")
    #DOWN CHECK
    s = True
    for i in range((field_size**2)-field_size, field_size**2):#checking for fartop corner
        if operating_at == (i):#is at fartop corner
            s = False
    if w == True:#somewhere NOT on fartop
        if field[operating_at+(field_size)] == '^' or field[operating_at+(field_size)] == 'v':
            s = False
    if s == True:
        possible.append("s")
    return possible


def print_pd(value):
    print("Can you make this movement? "+str(value))


def decision():
    print("pd:"+str(possible_decisions()), end=" ")

    movement = input("\n: ")
    movement_changes = {
        "w": (field_size)*-1,
        "s": (field_size),
        "a": (field_size)-1,
        "d": (field_size)+1
    }
    value = movement_changes[movement]
    #safety net

    # print("you're going to move "+str(value))

#choice
print_field()
decision()
# choice_maker
#
# movement = input("\n: ")
