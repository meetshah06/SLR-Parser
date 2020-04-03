import pprint
import copy

productions={
    1:'E->E+T',
    2:'E->T',
    3:'T->T*F',
    4:'T->F',
    5:'F->(E)',
    6:'F->id',
}

variables=['E','F','T']
terminals=['(','*','+',')','id']

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

string='id*id+id$'

# Input string must be space delimeted
string='id * id + id $' # Need to think of a more dynamic logic
stringTemp=string.split(' ')

# To check whether the action
# demands for swapping or not
# example: r11 returns False
# s6 returns True
def isSwap(action):
    if(action[0]=='s'):
        return True
    return False

# To check whether the action
# demands for reduction or not
# example: r11 returns True
# s6 returns False
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

info={
    'stackInfo':[],
    'stringInfo':[]
}
while(True):
    info['stackInfo'].append(copy.copy(stack))
    info['stringInfo'].append(copy.copy(stringTemp))

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

    # Logic for action swap
    if(isSwap(parsingTable[stackEnd]['action'][symbol])):
        symbol=stringTemp.pop(0) # Pop and acquire the latest symbol from the string (id)
        action=parsingTable[stackEnd]['action'][symbol] # Acquire the swap action with its number from the Parsing Table (s5)
        value=symbol+str(getActionNumber(action)) # Acquire the swap number using getActionNumber() as defined above and append it to the symbol (id5)
        stack.append(value) # Push the value (id5) to the stack

    # Logic for action reduce
    if(isReduce(parsingTable[stackEnd]['action'][symbol])):
        action=parsingTable[stackEnd]['action'][symbol] # Acquire the reduce action with its number from the Parsing table (r6)
        actionNumber=getActionNumber(action) # Acquire the reduce number using getActionNumber() as defined above (6)

        productionRHS=productions[actionNumber].split('->')[1:] # RHS (everything after ->) of the production defined at actionNumber (6)
        # length=len(productionRHS[0])-productionRHS.count('id')

        # Logic to calculate number of variables
        # and terminals present within the production rule
        # at the actionNumber
        length=0
        for item in list(variables+terminals):
            length+=productionRHS[0].count(item)

        # Pop 'length' number of elements from stack
        for char in (range(length)):
            stack.pop(-1)

        productionLHS=productions[actionNumber].split('->')[0] # LHS (everything before ->) of the production defined at actionNumber (6)
        tempTwo=''
        for char in str(stack[-1]):
            if(char.isdigit()):
                tempTwo+=str(char)

         # Push the LHS of the production along with
         # the necessary number
        stack.append(productionLHS+str(parsingTable[int(tempTwo)]['goal'][productionLHS]))

# pprint.pprint(info)
