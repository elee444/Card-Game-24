# you enter 4 integers (1-10) or it can generate 4 integers.
# Determine if 24 can be the outcome after applying +,-,*,+ on these
# 4 numbers (each is used one and only one time). Furthermore, it is
##required that each operation results in integer.
# Use post-order representation to avoid parentheses
##
#!/usr/bin/python3
# python 24_post.py
from random import randint
import itertools




# Evaluate the post-order representation
def postfixEval(postfixExpr):
    operandStack = []
    for token in postfixExpr:
        if token in "1023456789":
            operandStack.append(int(token))
        else:
            operand2 = operandStack.pop()
            operand1 = operandStack.pop()
            if (token =="/"): #true division not integer division
                if (operand2==0 or operand1 % operand2!=0):  #watch out exceptions
                    return 0
            result = doMath(token, operand1, operand2)
            operandStack.append(result)
    return operandStack.pop()

# Make it human readable


def doMath(op, op1, op2):
    if op == "*":
        return op1 * op2
    elif op == "/":
        return op1 / op2
    elif op == "+":
        return op1 + op2
    else:
        return op1 - op2


def done(mylist):
    print('\nAnswer is: ')
    print(mylist)
    quit()




def compute(listx):
#if __name__ == "__main__":
    x = listx
    target = 24
    #print('\nThe numbers are : ')
    #print(x)

    input('\nCan you find 24 ? Hit Enter key to see the answer.')

    found=False
    ans=[]
# Each 4-tuple of number needs only 3 opeartions
# Let's run through all possible collections of 3-operation, i.e. chooses
# 3 out of 4 operations with replacement.
    for y in itertools.permutations(x):
        for op in itertools.product("+-*/", repeat=3):
           # for each 4-tuple of numbers and 3-tuple of operations, there are
           # only 4 possible valid formats (in post-order)
            st1 = [y[0], y[1], op[0], y[2], op[1], y[3], op[2]]
            st2 = [y[0], y[1], op[0], y[2], y[3], op[1], op[2]]
            st3 = [y[0], y[1], y[2], op[0], y[3], op[1], op[2]]
            st4 = [y[0], y[1], y[2], y[3], op[0], op[1], op[2]]
            st = [st1, st2, st3, st4]
            res = [postfixEval(pl) for pl in st]
            for idx, val in enumerate(res):
                if (val == target):
                    found=True
                    ans.append(st[idx])
                    #done(st[idx])
    if (found==False):
        print("No Answer found!")
    else:
        print("Number of answers is :",len(ans))
        for a in ans:
            print(a)

#compute(['6','8','9','10'])
#compute(['6','3','7','8'])
