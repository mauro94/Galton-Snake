# Additional Compiler Functions
# Patricio Sanchez A01191893
# Mauro Amarante A01191893

# -------------------------- STACK OPERATIONS --------------------------
def stackTop(stack):
	global operands, types, operators
	if len(stack) > 0:
		x = stack[-1]
	else:
		x = None
	return x

def stackPush(stack, x):
	global operands, types, operators
	stack.append(x)

def stackPop(stack):
	global operands, types, operators
	if len(stack) > 0:
		x = stack.pop()
	else:
		x = None
	return x


# -------------------------- QUADRUPLES OPERATIONS --------------------------
def newQuadruple(list, operator, operand1, operand2, result):
	global quadruples
	list.append({'operator':operator, 'operand1':operand1, 'operand2':operand2, 'result':result})
