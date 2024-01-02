import itertools

def fill(partialTuple):
    # param partialTuple: (0, 1, 1, 0, None, None, 1)
    nones = [i for i in range(len(partialTuple)) if partialTuple[i] is None]
    for i in range(2**len(nones)):
        val = i
        fullList = list(partialTuple)
        for j in nones:
            fullList[j] = val & 1
            val = val // 2
        yield tuple(fullList)

def augment(initialTable, condProbs):
    # param initialTable: {[0, 0]: 25%, [0, 1]: 70%, [1, 0]: 4%, [1, 1]: 1%}
    # param condProbs: {[0, None]: 90%, [1, None]: 5%}
    # return newState: {[0, 0]: 10% ... /* include all eight */ ... }

    fullCondProbs = {}
    for key in condProbs:
        prob = condProbs[key]
        fullCondProbs[key + (1, )] = prob
        fullCondProbs[key + (0, )] = 1-prob
    newState = {}

    for cond in fullCondProbs:
        prob = fullCondProbs[cond]
        for filledCond in fill(cond):
            newState[filledCond] = prob * initialTable[filledCond[:-1]]
    return newState


# parse("P(C|A) = 0.6", "P(C|~A, B) = 0.2", "P(C|~A, ~B) = 0.7"], ["A", "B"])
# should return {(1, None): 0.6, (0, 1): 0.2, (0, 0): 0.7}
def parse(instructions, nodeNames):
    # param instructions: ["P(C|A) = 0.6", "P(C|~A, B) = 0.2", "P(C|~A, ~B) = 0.7"]
    condProbs = {}
    for instr in instructions:
        conditionStr, prob = instr.split("=")
        prob = float(prob)
        givenSplit = conditionStr.split("|")
        if len(givenSplit) == 2: givens = givenSplit[1].split(")")[0].split(",")
        else: givens = []
        givenSet = {i.strip() for i in givens}

        # err
        for given in givenSet:
            bareGiven = given[1:] if given[0] == "~" else given
            if bareGiven not in nodeNames and bareGiven not in nodeNames:
                errStr = str(instr) + " is invalid because P(" + bareGiven + ") has not been defined yet"
                raise ValueError(errStr)
        
        condTable = tuple((1 if name in givenSet else 0 if "~"+name in givenSet else None) for name in nodeNames)
        condProbs[condTable] = prob
    return condProbs

def bayes(instructions):
    table = {(): 1}
    nodeNames = []

    instrAcc = []
    accToken = None
    
    for instr in instructions + ["P()"]:
        conditionStr = instr.split("=")[0]
        token = conditionStr.split("|")[0].split("(")[-1].split(")")[0].strip()
        if accToken is None: accToken = token
        if token != accToken:
            table = augment(table, parse(instrAcc, nodeNames))

            # error handling
            if 2**(len(nodeNames)+1) != len(table):
                errStr = "Missing the following probabilities \n\n"
                for prod in itertools.product((0, 1), repeat=len(nodeNames)):
                    if prod + (1, ) not in table:
                        errStr += "P(" + accToken + "|"
                        for tokenIdx in range(len(nodeNames)):
                            if prod[tokenIdx] == 0:
                                errStr += "~"
                            errStr += nodeNames[tokenIdx]
                            if tokenIdx != len(nodeNames)-1:
                                errStr += ", "
                        errStr += ")\n"
                raise ValueError(errStr)

            nodeNames.append(accToken)
            instrAcc = []
            accToken = token
        instrAcc.append(instr)
    return table, nodeNames

def getProb(probToFind, givenProbs):
    table, nodeNames = bayes(givenProbs)
    givenSplit = probToFind.split("|")
    if len(givenSplit) == 2: givens = givenSplit[1].split(")")[0].split(",")
    else: givens = []
    givenSet = {i.strip() for i in givens}
    givenDict = {(i[1:] if i[0] == "~" else i) : (False if i[0] == "~" else True) for i in givenSet}
    token = givenSplit[0].split("(")[-1].split(")")[0].strip()
    tokenInd = nodeNames.index(token.replace("~",""))

    givenInd = {nodeNames.index(i) : givenDict[i] for i in givenDict}
    givenTup = tuple(givenInd[i] if i in givenInd else None for i in range(len(nodeNames)))

    favorable = 0
    total = 0
    for completion in fill(givenTup):
        prob = table[completion]
        satisfy = (completion[tokenInd] == (token[0] != "~"))
        if satisfy: favorable += prob
        total += prob
    return favorable / total

if __name__ == "__main__":
    probs = ['P(B)=0.001', 'P(E)=0.002', 'P(A|B,E)=0.95', 'P(A|B,~E)=0.94', 'P(A|~B,E)=0.29', 'P(A|~B,~E)=0.001', 'P(J|A)=0.9', 'P(J|~A)=0.05', 'P(M|A)=0.7', 'P(M|~A)=0.01']
    print(round(getProb('P(~B)', probs), 5))
    print(round(getProb('P(~A | B, ~E)', probs), 5))
    print(round(getProb('P(B | J, M)', probs), 5))
