# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 15:47:16 2020

@author: Sanket SS
"""

#PARSER table and goto table
f1 = open('first.txt','r').read().splitlines()
first = dict({})
for i in f1:
	x,y=i.split(':')
	#y = y[1:-1]
	first[x]=y
del f1

f2 = open('follow.txt','r').read().splitlines()
follow = dict({})
for i in f2:
	x,y=i.split(':')
	follow[x]=y
del f2
#%%
f3 = open('columns.txt','r').read().splitlines()
columns = []
for i in f3:
	columns.append(i)

f4 = open('itemset.txt','r').read().splitlines()
itemset = dict([])
for i in f4:
	x,y=i.split(':')
	y = y[1:-3]
	temp = y.split('  ')
	tempdict = dict([])
	for item in temp:
		#print(item)
		k,v = item.split(';')
		tempdict[k]=v
	itemset[x]=tempdict

f5 = open('gototab.txt','r').read().splitlines()
gototab = dict([])
for i in f5:
	x,y=i.split(':')
	y = y[1:-3]
	temp = y.split('  ')
	tempdict = dict([])
	for item in temp:
		#print(item)
		k,v = item.split(';')
		tempdict[k]=v
	gototab[x]=tempdict

productions = dict([])
f6 = open('productions.txt','r').read().splitlines()
for i in f6:
	print(i)
	x,y = i.split(':')
	productions[x]=y

del f3,f4,f5,f6,i,item,k,v,x,y,temp,tempdict
#%%
import pandas as pd
columns.extend(['E','T','F'])
parsetable = pd.DataFrame(columns=columns)
#parsetable.columns = columns
#print(parsetable)
#%%
for i in range(len(gototab)):
	name = 'I'+str(i)
	#print(name)
	gg = gototab[name]
	keys=gg.keys()
	temp=dict([])
	values = gg.values()
	for k in keys:
		if gg[k]!='-1':
			if k.isupper():
				temp[k] = gg[k].lstrip('I')
			else:
				temp[k] = 's'+gg[k].lstrip('I')
		else:
			temp[k]='-'
	temp['$'] = '-'
	#print(temp)
	parsetable.loc[i]=temp
del i,k,name,temp
#%%
def getProductionNum(src,dest):
	new = src+' -> '+dest[:-1]
	print(src,dest)
	for k,v in productions.items():
		if v==new:
			return k

#%%	
for k,y in follow.items():
	print(k)
	for state,prods in itemset.items():
		for src,dest in prods.items():
			temp = dest.split('|')
			for item in temp:
				loc = item.find('.')
				if loc!=0 and loc==len(item)-1:
					#parsetable.at[int(state.lstrip('I')),]
					#print(state,item)
					which = getProductionNum(src,item)
					#print(which)
					new = follow[k].replace("'",'')
					new = follow[k].replace("{",'')
					new = follow[k].replace("}",'')
					new = follow[k].replace(",",'')
					for i in new:
						parsetable.at[int(state.lstrip('I')),i]='r'+str(which)
#%%
		
	
	
	





