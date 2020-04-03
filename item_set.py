"""
Grammar: (Non augmented):
G=(V,T,S,P)
S = E
T = +, *, id
V = E,T,F
P =>
E -> E+T
E -> T
T -> T*F
T -> F
F -> (E)
F -> id

"""
class ItemSet:
	item_set = {}
	gram = {}
	term = []#change later. same for below.
	non_term = []
	start_sym = ''
	goto_table = {}
	
	def __init__(self,v,t,s,p):
		self.non_term = v
		self.term = t
		self.start_sym = s
		self.gram = p

	def construct(self):
		"""
		All main calculations including the caluclation of the item_set and the goto table is done here.
		calls goto and closure and all supporting methods. 
		input: nothing.
		output: computed item_set and goto_table. (both 2D dictionaries)
		goto table = eg. goto_table[I][x] = either a set/ -1 if not present.
		"""
		#construct the first part of c
		self.item_set['I0'] = self.closure({self.start_sym+'\'':'.'+self.start_sym})#closure returns a dictionary.
		# print("Aftet the first closure:",self.item_set)
		self.display(self.item_set)

		#as itemset is changing have to do the queue thing again
		i=1
		queue = ['I0']#this naming convention is followed throughut 
		fin = []
		while(queue!=[]):
			el = queue.pop(0)
			self.goto_table[el] = {}   #empty ditionary for new itemset.
			val = self.item_set[el] #its the 2nd dictionary
			#call goto for each I,X were I = var and X is all term + non_term
			for x in self.non_term+self.term:
				new_set = self.goto(val,x)
				temp = -1
				if(new_set!={}):
					#calulate closure
					new_set = self.closure(new_set) #send a dictionary to calulate closure

					#check if it is same with some other set:
					truth,set_comp = self.compare_sets(new_set)
					if(truth):
						#modify the goto table 
						# set_comp is the number of the set it matches 
						temp = set_comp
					else:
						self.item_set['I'+str(i)] = new_set
						queue.append('I'+str(i))
						temp = 'I'+str(i)
						i+=1
				self.goto_table[el][x] = temp
			fin.append(el)
		return self.item_set,self.goto_table

	def goto(self,item,x):#item is the current dictionary and x is the item for which we have to calculate.
		"""
		Calculates the goto value for a given item set and a X = terminals + variables.
		input: item set (dicitonary) and x (terminal or non terminal string)
		return: A new dictionary swapping '.x' with 'x.'
		"""
		ans = {}
		for lhs,rhs in item.items():
			#if rhs has .x then:
			parts_of_rhs = rhs.split('|')
			for rhs in parts_of_rhs:
				if(rhs.find('.'+x)!=-1):
					#add the production rhs->lhs with x.
					rhs = (x+'.').join(rhs.split('.'+x)) #swapping .x for x.
					#swap those two positions
					ans[lhs] = rhs
		return ans

	def closure(self,item):#item is a dictionary.
		"""
		computes closure of a dicitonary that is input using the grammar attribute of this class.
		input: Dicitonary of eleements already present.
		output: same dicitonary augemented to include the closure elements calculated.
		"""
		queue = []
		# fin = [x for x in item.keys()]#for all lhs that are already present in item then dont add that later.
		fin = []
		for val in item.values():
			temp = self.is_dot(val)
			if(temp!=[]):
				for x in temp:#if temp has repeated non terminals then dont add that vlaue multiple times in queue.
					if x not in queue:
						queue.append(x)
		while(queue!=[]):
			el = queue.pop()
			temp = self.gram[el]
			parts = ['.'+y for y in temp.split('|') ]
			for x in parts:
				temp = self.is_dot(x)
				for y in temp:
					if((y not in queue)and(y not in fin)and (y != el)):
						queue.append(y)
			#we know el is not in item. Adding productions:
			if(el in item.keys()):
				parts = parts + [item[el]]
			item[el] = '|'.join(parts) #add that .gamma to the right.
			fin.append(el)
		return item
	
	def is_dot(self,rhs):#returns list of all non_terminals found.
		"""
		This function takes a string of the rhs of the grammar as input and reyturns all the Non_terminals or varaibles that 
		are preceeded by '.' and returns that. 
		input: rhs of grammar (string)
		output: list of varaibles preeceeded by '.'
		"""
		found = []
		for i in range(0,len(rhs)):
			if rhs[i]=='.' and i!=len(rhs)-1:
				found.append(rhs[i+1])
		found = [x for x in found if x in self.non_term]
		return found

	def compare_sets(self,incoming):
		'''Compares the incoming set to match any of the previous 
		sets already present in the item_set dictionary 
		param: the set with which we compare 
		returns: true or false, if true, then the set number that matches (in string)
		'''
		num = -1
		for var,x in self.item_set.items():
			if x.items() == incoming.items():
				num = var
				break
		if(num!=-1):
			return True,num
		return False,-1
				

	def display(self,dict1):
		"""
		To display any 2D dictionaries including goto_table and Item_set
		input: dicitonary to display. returns nothing.
		"""
		for x in dict1:
			print(x+" {")
			for y in dict1[x]:
				print('  ',y,'->',dict1[x][y])
			print("}")
#%%

prod = {'E': 'E+T|T', 'T': 'T*F|F', 'F': '(E)|id'}
s = 'E'
v  = ['E','T','F']
t = ['id','+','*','(',')']

	#object:
imset = ItemSet(v,t,s,prod)
item_set,goto_tab = imset.construct()
imset.display(item_set)
imset.display(goto_tab)
#%%
with open('itemset.txt','w') as f:
	for ki,vi in item_set.items():
		print(ki)
		f.write('{}:{}'.format(ki,'{'))
		for k,v in item_set[ki].items():
			f.write(f'{k};{v}  ')
		f.write('}\n')
#%%
with open('gototab.txt','w') as f:
	for ki,vi in goto_tab.items():
		print(ki)
		f.write('{}:{}'.format(ki,'{'))
		for k,v in goto_tab[ki].items():
			f.write(f'{k};{v}  ')
		f.write('}\n')
#%%
			
with open('columns.txt','w') as f:
	for i in t:
		f.write(f'{i}\n')
	f.write('$')
#%%
p="""E -> E+T
E -> T
T -> T*F
T -> F
F -> (E)
F -> id"""			
i=1
with open('productions.txt','w') as f:
	for item in p.splitlines():
		f.write(f'{i}:{item}\n')
		i+=1
#%%	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		