from math import log2

def show(genchain):
    for i in genchain:
        print(round(i*1200, 2), sep=",\t", end="\t")
    print()

def get_errors(genchain, intervals, periods):
    return [0] + [min((min(interval-i, -(1/periods)+(interval-i), key=lambda x: abs(x)) for i in genchain), key=lambda x: abs(x)) for interval in intervals]

def error(genchain, intervals, periods):
    errs = get_errors(genchain, intervals, periods)
    return (max(errs) - min(errs))*1200

def get_mapping(genchain, intervals, periods):
    root = genchain.index(0)
    return tuple(min(range(len(genchain)), key=(lambda idx: min(abs(genchain[idx]-interval), abs(-(1/periods)+(interval-genchain[idx])))))-root for interval in intervals)

complexity = 32
max_error = 65 # cents
ratios = [3, 5, 7, 9, 11, 13]

all_solutions = {}
for complexi in [complexity>>i for i in range(int(log2(complexity)))]:
    for periods in range(1, complexi+1):
        solutions = {}
        generators = (complexi+periods) // periods

        intervals = [log2(i)%(1/periods) for i in ratios]
        helds = {(i-j)%(1/periods) for i in intervals for j in (intervals + [0])} - {0}

        for held in helds:
            for comp in range(generators):
                for branch in range(comp):
                    for end in range(generators):
                        genchain = [((held+branch)/comp*i)%(1/periods) for i in range(end-generators+1, end+1)]
                        err = round(error(genchain, intervals, periods), 5)
                        if err < max_error:
                            mapping = get_mapping(genchain, intervals, periods)
                            generator = ((held+branch)/comp)%(1/periods)
                            errors = get_errors(genchain, intervals, periods)
                            if generator > (0.5/periods):
                                mapping = tuple(-i for i in mapping)
                                generator = (1/periods) - generator
                            mapping += (periods,)
                            if (mapping not in solutions or solutions[mapping][0] > err or (solutions[mapping][0] == err and abs(solutions[mapping][3][1]) >= abs(errors[1]))):
                                solutions[mapping] = (err, periods, generator, errors)
        all_solutions.update(solutions)
        solutions = {}

print("----------------------------------------------------------------------------------------", "", sep="--------"*(len(ratios)-1))
print("           Cents", "    Error     Complexity   Generator     Period      Mapping", sep="\t"*(len(ratios)-1))
print("----------------------------------------------------------------------------------------", "", sep="--------"*(len(ratios)-1))
compl_best = float("inf")
for i in sorted(list(all_solutions), key=lambda mapping: all_solutions[mapping][0]):
    j = all_solutions[i]
    compl = j[1]*(max(i[:-1]+(0, ))-min(i[:-1]+(0, )))
    if compl < compl_best and compl:
        compl_best = min(compl_best, compl)
        print(" ["+", ".join(f'{((log2(ratios[idx])-m)%1*1200):.3f}'for idx, m in enumerate(j[3][1:]))+"]", f'{j[0]:.5f}'+" "*(5-len(str(int(j[0]))))+"|    "+str(compl), round(j[2]*1200, 3), sep="\t|   ", end="")
        print("   ", "  "+str(j[1]) + ((4-len(str(j[1])))*" ") + "|    "+str(i[:-1]), sep="\t|")
    