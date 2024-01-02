import sys; args = sys.argv[1:]
file = open(args[0])
import math

def transfer(t_funct, value):
   return t_funct(value)

def dot_product(list1, list2):
   return sum(i*j for i,j in zip(list1, list2))

def evaluate(file, input_vals, t_funct):
   vals = input_vals
   lines = file.readlines()
   for line in lines[:-1]:
      weightList = list(map(float, line.split())) # order: w14, w24, w34, w15, w25, w35
      newVals = []
      for i in range(0, len(weightList), len(vals)):
         newVals.append(transfer(t_funct, dot_product(vals, weightList[i:(i+len(vals))])))
      vals = newVals
   return [i*j for i,j in zip(vals, map(float, lines[-1].split()))]
     
def main():
    inputs, t_funct, transfer_found = [], 'T1', False
    for arg in args[1:]:
       if not transfer_found:
           t_funct, transfer_found = arg, True
       else:
          inputs.append(float(arg))
    t_funct = {'T1': (lambda x: x),
               'T2': (lambda x: max(0, x)),
               'T3': (lambda x: 1/(1+math.e**(-x))),
               'T4': (lambda x: -1+2/(1+math.e**(-x)))}[t_funct]
    li =(evaluate(file, inputs, t_funct)) #ff
    for x in li:
       print (x, end=' ') # final outputs
      
if __name__ == '__main__':
    main()

# Vincent Trang, Period 4, 2023
