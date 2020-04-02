productions={
    1:'E->E+T',
    2:'E->T',
    3:'T->T*F',
    4:'T->F',
    5:'F->(E)',
    6:'F->id',
}

parsingTable={
    0:{
        'action':{
            'id':'s5',
            '+':None,
            '*':None,
            '(':'s4',
            ')':None,
            '$':None
        },
        'goal':{
            'E':1,
            'T':2,
            'F':3
        }
    },
    1:{
        'action':{
            'id':None,
            '+':'s6',
            '*':None,
            '(':None,
            ')':None,
            '$':'accept'
        },
        'goal':{
            'E':None,
            'T':None,
            'F':None
        }
    },
    2:{
        'action':{
            'id':None,
            '+':'r2',
            '*':'s7',
            '(':None,
            ')':'r2',
            '$':'r2'
        },
        'goal':{
            'E':None,
            'T':None,
            'F':None
        }
    },
    3:{
        'action':{
            'id':None,
            '+':'r4',
            '*':'r4',
            '(':None,
            ')':'r4',
            '$':'r4'
        },
        'goal':{
            'E':None,
            'T':None,
            'F':None
        }
    },
    4:{
        'action':{
            'id':'s5',
            '+':None,
            '*':None,
            '(':'s4',
            ')':None,
            '$':None
        },
        'goal':{
            'E':8,
            'T':2,
            'F':3
        }
    },
    5:{
        'action':{
            'id':None,
            '+':'r6',
            '*':'r6',
            '(':None,
            ')':'r6',
            '$':'r6'
        },
        'goal':{
            'E':None,
            'T':None,
            'F':None
        }
    },
    6:{
        'action':{
            'id':'s5',
            '+':None,
            '*':None,
            '(':'s4',
            ')':None,
            '$':None
        },
        'goal':{
            'E':None,
            'T':9,
            'F':3
        }
    },
    7:{
        'action':{
            'id':'s5',
            '+':None,
            '*':None,
            '(':'s4',
            ')':None,
            '$':None
        },
        'goal':{
            'E':None,
            'T':None,
            'F':10
        }
    },
    8:{
        'action':{
            'id':None,
            '+':None,
            '*':None,
            '(':None,
            ')':None,
            '$':None
        },
        'goal':{
            'E':None,
            'T':None,
            'F':10
        }
    },
    9:{
        'action':{
            'id':None,
            '+':'r1',
            '*':'s7',
            '(':None,
            ')':'r1',
            '$':'r1'
        },
        'goal':{
            'E':None,
            'T':None,
            'F':None
        }
    },
    10:{
        'action':{
            'id':None,
            '+':'r3',
            '*':'r3',
            '(':None,
            ')':'r3',
            '$':'r3'
        },
        'goal':{
            'E':None,
            'T':None,
            'F':None
        }
    },
    11:{
        'action':{
            'id':None,
            '+':'r5',
            '*':'r5',
            '(':None,
            ')':'r5',
            '$':'r5'
        },
        'goal':{
            'E':None,
            'T':None,
            'F':None
        }
    }
}

string='id * id + id $'
stringTemp=string.split(' ')

# To check whether the action
# demands for swapping or not
def isSwap(action):
    if(action[0]=='s'):
        return True
    return False

# To check whether the action
# demands for reduction or not
def isReduce(action):
    if(action[0]=='r'):
        return True
    return False

# Acquires the number that follows
# the action.
# example: r11 results in 11,
# s6 results in 6.
def getActionNumber(action):
    return int(action[1:])


stack=[]
stack.append(str(0)) # Stack initialised at I0

# while stringTemp!=[]:
while(True):
    print(stack)
    print(stringTemp)

    symbol=stringTemp[0]

    stackEnd=''
    for char in str(stack[-1]):
        if char.isdigit():
            stackEnd+=char
    stackEnd=int(stackEnd)

    if(symbol=='$' and parsingTable[stackEnd]['action'][symbol]=='accept'):
        print('ACCEPTED')
        break
    elif(symbol=='$' and parsingTable[stackEnd]['action'][symbol]==None):
        print('REJECTED :(')
        break

    if(isSwap(parsingTable[stackEnd]['action'][symbol])):
        symbol=stringTemp.pop(0)
        action=parsingTable[stackEnd]['action'][symbol]
        value=symbol+str(getActionNumber(action))
        stack.append(value)

    if(isReduce(parsingTable[stackEnd]['action'][symbol])):
        action=parsingTable[stackEnd]['action'][symbol]
        actionNumber=getActionNumber(action)

        productionRHS=productions[actionNumber].split('->')[1:]
        length=len(productionRHS[0])-productionRHS.count('id')

        for char in (range(length)):
            stack.pop(-1)

        productionLHS=productions[actionNumber].split('->')[0]
        tempTwo=''
        for char in str(stack[-1]):
            if(char.isdigit()):
                tempTwo+=str(char)
        stack.append(productionLHS+str(parsingTable[int(tempTwo)]['goal'][productionLHS]))
