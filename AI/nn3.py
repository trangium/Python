import sys; args = sys.argv[1:]
import math, random

def sigmoid(x):
   return 1/(1+math.e**(-x))

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
               'T3': sigmoid,
               'T4': (lambda x: -1+2/(1+math.e**(-x)))}[t_funct]
    li =(evaluate(weights, inputs, t_funct)) 
    return li

def main():
   R = float(args[0].replace("=","").replace("<",">").split(">")[1])**0.5
   direction = ("<" in args[0])*2-1
   a = 0.005 # epsilon > 0
   
   layer1 = [a, 0, 0, 0, a, 0, 0, 0, 0] # 3*3
   layer2 = [4, 0, -2, 4, 0, -6, 0, 4, -2, 0, 4, -6, 0, 0, 0] # 3*5
   layer3 = [1, -1, 1, -1, 0, 0, 0, 0, 0, 2*(sigmoid(4*sigmoid(a*R)-1)-sigmoid(4*sigmoid(a*R)-3)+2*sigmoid(1)-1)] # 5*2
   layer4 = [direction, -direction] # 2*1
   layer5 = [1]

   layers = [layer1, layer2, layer3, layer4, layer5]
   best = float("inf")

   print("Layer cts:", [3, 3, 5, 2, 1, 1])
   print("Weights:")
   print(*layers, sep="\n")
      
if __name__ == '__main__':
    main()

# Vincent Trang, Period 4, 2023
