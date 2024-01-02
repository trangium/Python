import sys; args = sys.argv[1:]
file = open(args[0])
import math, random

def transfer(t_funct, value):
   return t_funct(value)

def dot_product(list1, list2):
   return sum(i*j for i,j in zip(list1, list2))

def evaluate(weights, input_vals, t_funct):
   vals = input_vals
   for weightList in weights[:-1]: # order: w14, w24, w34, w15, w25, w35
      newVals = []
      for i in range(0, len(weightList), len(vals)):
         newVals.append(transfer(t_funct, dot_product(vals, weightList[i:(i+len(vals))])))
      vals = newVals
   return [i*j for i,j in zip(vals, weights[-1])]
     
def nn(inputs, t_funct, weights):
    t_funct = {'T1': (lambda x: x),
               'T2': (lambda x: max(0, x)),
               'T3': (lambda x: 1/(1+math.e**(-x))),
               'T4': (lambda x: -1+2/(1+math.e**(-x)))}[t_funct]
    li =(evaluate(weights, inputs, t_funct)) 
    return li

def nnErrors(layers, targetDict):
   errors = []
   for inputs in targetDict:
      outputs = targetDict[inputs]
      actual = (nn(list(inputs) + [1], "T3", layers))[0]
      errors.append(0.5*(outputs-actual)**2)
   return errors

def main():
   targetDict = {}
   for line in file.readlines():
      inputStr, outputStr = line.split("=>")
      t_inputs = tuple(map(float, inputStr.split()))
      t_output = float(outputStr.strip())
      targetDict[t_inputs] = t_output
      inputCount = len(t_inputs)
   
   layer1 = [(random.random()-0.5)*2 for i in range(2*inputCount+2)]
   layer2 = [30, -30]
   layer3 = [1]
   best = float("inf")

   for i in range(70000):
      newLayer1 = layer1[:]
      newLayer1[random.randint(0, len(layer1)-1)] = (random.random()-0.5)*2
      errors = nnErrors([newLayer1, layer2, layer3], targetDict)
      error = sum(errors)
      if error < best:
         layer1 = newLayer1
         best = error
      if i%7000 == 0: best = float("inf")
      if error < 0.01: break

   print("Errors:", errors)
   print("Error:", sum(errors))
   print("Layer cts:", [inputCount+1, 2, 1, 1])
   print("Weights:")
   print(layer1)
   print(layer2)
   print(layer3)
      
if __name__ == '__main__':
    main()

# Vincent Trang, Period 4, 2023
