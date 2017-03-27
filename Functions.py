# Additional Compiler Functions
# Patricio Sanchez A01191893
# Mauro Amarante A01191893

# -------------------------- STACK OPERATIONS --------------------------
def stackTop(stack):
	global stackOperands, stackType, stackOperators
	x = stack.pop()
	stack.append(x)
	return x

def stackPush(stack, x):
	global stackOperands, stackType, stackOperators
	stack.append(x)

def stackPop(stack):
	global stackOperands, stackType, stackOperators
	x = stack.pop()
	return x



# -------------------------- QUEUE OPERATIONS --------------------------
def queuePush(queue, x):
	global quadruples
	queue.append(x)

def queuePop(queue):
	global quadruples
	x = queue.popleft()
	return x



# -------------------------- SEMANTIC OPERATIONS --------------------------
def newFunction(dirFunc, scope, t):
	dirFunc[scope] = [t, [], 0, 0, 0, {}]

def varTable(dirFunc, scope):
	return dirFunc[scope][5]

def funcSignature(dirFunc, scope):
	return dirFunc[scope][1]


# -------------------------- DATAFRAME OPERATIONS --------------------------
def dataframeTags(dirFunc, scope, p):
	return dirFunc[scope][5][p[-5]][1]


# -------------------------- QUADRUPLES OPERATIONS --------------------------
def createQuadruple(operator, operand1, operand2, result):
	queuePush(quadruples, {'operator':operator, 'operand1':operand1, 'operand2':operand2, 'result':result})
