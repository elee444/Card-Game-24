#!/usr/bin/python3
"""
x-game: a generalization of 24-game.
This coumputes the statistical disttribution regarding to x (4-10^4)

compile to C: nuitka --standalone *py
"""
from random import randint
import itertools
import time
from collections import defaultdict
import json

SampleCount=0
Space=defaultdict(lambda:0)

def postfixEval(postfixExpr):
	operandStack = []
	for token in postfixExpr:
		if token in "1023456789":
			operandStack.append(int(token))
		else:
			operand2 = operandStack.pop()
			operand1 = operandStack.pop()
			if token =="/" and (operand2==0 or operand1%operand2 !=0 ):
				return -1
			result = doMath(token,operand1,operand2)
			operandStack.append(result)
	return operandStack.pop()

def doMath(op, op1, op2):
	if op == "*":
		return op1 * op2
	elif op == "/":
		return (op1) / op2
	elif op == "+":
		return op1 + op2
	else:
		return op1 - op2


def funCal(args):
	global SampleCount
	tmset=set()
	for op in itertools.product("+-*/",repeat=3):
		st1=[args[0],args[1],op[0],args[2],op[1],args[3],op[2]]
		st2=[args[0],args[1],op[0],args[2],args[3],op[1],op[2]]
		st3=[args[0],args[1],args[2],op[0],args[3],op[1],op[2]]
		st4=[args[0],args[1],args[2],args[3],op[0],op[1],op[2]]
		st5=[args[0],args[1],args[2],op[0],op[1],args[3],op[2]]
		st=[st1,st2,st3,st4,st5]
		tempcount=0
		
		for m in range (5):
			tm=(postfixEval(st[m]))
			#if tm>=0 and 0.000000001>tm-int(round(tm))>-0.000000001:
			#	tm=int(round(tm))
			if tm>=0:
				tmset.add(tm)
				if tm==931:
					print(st[m])
				#Space[tm]=Space[tm]+1
				#SampleCount=SampleCount+1
		for x in tmset:
			SampleCount=SampleCount+1
			Space[x]=Space[x]+1
		tmset.clear()
	return 0


def testFunc(xc):
	itC=itertools.product(xc, repeat=4)  #generate all sets of 4 numbers
	for x in itC:	
		funCal(x)
	

#main program
#for each target (4-10^4, find if target has a solution
#update count[]

x_choice=list()
for i in range(1,11):
	x_choice.append(str(i))

starttime=time.time()
testFunc(x_choice)
endtime=time.time()
print('Time = ',endtime-starttime)
 
#f_out=open('24_stat.txt','w')

prob=defaultdict(lambda:0)
sumS=0
#totalN=pow(10,4)
for d in Space:
	#prob[d]=Space[d]/SampleCount	
	prob[d]=Space[d] #/SampleCount
	#sumS=sumS+Space[d]

with open('24_stat.txt','w') as handle:
	#json.dump(sorted(prob.values()), handle)
	json.dump(prob, handle)

print('count= ',SampleCount)

#print(sumS,SampleCount)
"""
with open('file.txt', 'rb') as handle:
  b = pickle.loads(handle.read())

for target in range(4,10):
	starttime=time.time()
	tt=testFunc(count,target)
	endtime=time.time()
	print(target,tt, endtime-starttime)
"""


		



