start = ''
gram = {}
nonterminals = set([])
terminals = set([])

with open('./Text Files/grammar2.txt') as grammar_file:
	grammar = grammar_file.read().splitlines()

# print(grammar)
for g in grammar:
	# Middle part contains the string with which you split
	head, _, prods = g.partition(' -> ')
	# print(head, prod)
	# print(f'{head} -> {prods}')
	temp = prods.split('|')
	# print(temp)

	# Store each production in separate list
	prods = [p.split() for p in temp]
	# print(prods)

	# To create fake start element E' -> E
	if start == '':
		start = head + '\''
		# Add to grammar list
		gram[start] = [[head]]

	# If nonterminal symbol is not present in grammar: 
	if head not in gram:
		gram[head] = []
		# Add it to nonterminal list
		nonterminals.add(head)

	# Iterate through every production
	for prod in prods:
		# Add it to grammar list
		gram[head].append(prod)

		for symbol in prod:
			# not upper == symbol or lower case; epsilon = ^
			if not symbol.isupper() and symbol != '^':
				terminals.add(symbol)
			elif symbol.isupper():
				nonterminals.add(symbol)

print('Augmented Grammar:-')

for head, prod in gram.items():
	print(head, '->', prod)

print('\nNonterminals:-')
print(nonterminals)

print('\nTerminals:-')
print(terminals)


first_seen = []
def FIRST(X):
	if X in terminals:
		return {X}

	else:
		global first_seen
		first = set([])

		while(True):
			# Add X to visited list
			first_seen.append(X)
			first_len = len(first)

			for prod in gram[X]:
				# If production is not epsilon
				if prod != ['^']:
					for symbol in prod:
						if symbol == X and '^' in first:
							continue

						# If it is a new symbol which has not been visited
						if symbol not in first_seen:
							# Get the first of that symbol
							symbol_first = FIRST(symbol)

							for sf in symbol_first:
								if sf != '^':
									first.add(sf)
							if '^' not in symbol_first:
								break

						else:
							break

						# If all visited symbols have epsilon, then add epsilon to first set
						first.add('^')
				
				# Else production is epsilon, add epsilon to first set
				else:
					first.add('^')

			first_seen.remove(X)

			if first_len == len(first):
				return first

follow_seen = []
def FOLLOW(A):
	global follow_seen
	follow_seen.append(A)
	
	follow = set([])
	if A == start:
		follow.add('$')

	for head, prods in gram.items():
		for prod in prods:
			if A in prod[:-1]:
				first = FIRST(prod[prod.index(A) + 1])
				follow |= (first - set('^'))

				if '^' in first and head not in follow_seen:
					follow |= FOLLOW(head)

			elif A in prod[-1] and head not in follow_seen:
				follow |= FOLLOW(head)

	follow_seen.remove(A)
	
	# print("printed follow =", follow)
	return follow 
#%%
print('\nFIRST:-')
with open('./Text Files/first.txt','w') as f:
	for head in gram:
		print(f'{head} = {FIRST(head)}')
		f.write(f'{head}:{FIRST(head)}\n')
	

print('\nFollow:-')
with open('./Text Files/follow.txt','w') as f:
	for head in gram:
		print(f'{head} = {FOLLOW(head)}')
		temp=FOLLOW(head)
		s=''
		for i in temp:
			s+=i+';'
		f.write(f'{head}:{s}\n')
#%%
with open('./Text Files/columns.txt','w') as f:
	for i in t:
		f.write(f'{i}\n')