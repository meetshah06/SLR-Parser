# SLR-Parser

gram is a dictionary containing key as the symbol on the left and the value containing a list of list of all productions
Everything else is a set

gram - dictionary
terminals - set
nonterminals - set
FIRST AND FOLLOW are functions which return a set
In your code you can directly call FOLLOW('E') which will return a set containing all elements in follow of E
