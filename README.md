# SLR-Parser

### First & Follow 

* FIRST and FOLLOW are functions which return a set.  
* One can can directly call FIRST('E') or FOLLOW('E') where either of them return a set containing the elements of first and follow of E. 
* gram is a dictionary with key, value pairs where the key is the symbol on the left and the value contains a 2D list (list of list) of all productions
* Every other data structure used is a set.

1) gram - dictionary  
2) terminals - set  
3) nonterminals - set  
