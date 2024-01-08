import sys; args = sys.argv[1:]
import math, random

def implicit(x):
   if x > 0: return 1
   return 0.1

def transfer(x):
   if x > 0: return x
   return 0.1*x

def dot_product(list1, list2):
   return sum(i*j for i,j in zip(list1, list2))

def evaluate(weights, input_vals):
   vals = input_vals
   for weightList in weights: # order: w14, w24, w34, w15, w25, w35
      newVals = []
      for i in range(0, len(weightList), len(vals)):
         newVals.append(transfer(dot_product(vals, weightList[i:(i+len(vals))])))
      vals = newVals
   return vals

def all_evaluate(weights, input_vals):
   vals = input_vals
   yield vals
   for weightList in weights: # order: w14, w24, w34, w15, w25, w35
      newVals = []
      for i in range(0, len(weightList), len(vals)):
         newVals.append(transfer(dot_product(vals, weightList[i:(i+len(vals))])))
      yield newVals
      vals = newVals

def lazy_bp(weights, input_vals, target, alpha=0.1, epsilon=1e-6):
   new_weights = [list(layer) for layer in weights]
   old_eval = sum((target[i] - evaluate(weights, input_vals)[i])**2/2 for i in range(len(target)))
   for layer_ind, layer in enumerate(weights):
      for weight_ind, weight in enumerate(layer):
         weights[layer_ind][weight_ind] += epsilon
         new_eval = sum((target[i] - evaluate(weights, input_vals)[i])**2/2 for i in range(len(target)))
         derivative = (new_eval - old_eval) / epsilon
         # print(layer_ind, weight_ind, derivative, sep="\t")
         new_weights[layer_ind][weight_ind] = weight - alpha * derivative
         weights[layer_ind][weight_ind] -= epsilon
   return new_weights

def smart_bp(weights, input_vals, target, alpha=0.1):
   layer_ct = len(weights)
   
   new_weights = [list(layer) for layer in weights]
   all_eval = list(all_evaluate(weights, input_vals))

   node_derivs = []

   for layer_ind in range(layer_ct-1, -1, -1):
      next_nodes = all_eval[layer_ind+1]
      prev_nodes = all_eval[layer_ind]
      
      if layer_ind == layer_ct - 1:
         next_node_derivs = [implicit(x) * (x-t) for x, t in zip(next_nodes, target)]
      else:
         next_node_derivs = [implicit(x) * sum(weights[layer_ind+1][next_idx*len(next_nodes)+curr_idx]*deriv
                                               for next_idx, deriv in enumerate(node_derivs[0])) for curr_idx, x in enumerate(next_nodes)]
         
      node_derivs.insert(0, next_node_derivs)

      for prev_idx, prev_val in enumerate(prev_nodes):
         for next_idx, next_deriv in enumerate(node_derivs[0]):
            deriv = prev_val * next_deriv
            # print(layer_ind, next_idx*len(prev_nodes)+prev_idx, deriv, sep="\t")
            new_weights[layer_ind][next_idx*len(prev_nodes)+prev_idx] -= alpha * deriv

   return new_weights

      

   # last node derivs = x(1-x)(x-target), where x is the sigmoidified node value
   # weight derivs = (prev node value)(next node deriv)
   # non-last node derivs = x(1-x) * (sum over weights) (weight)(next node deriv)

def quick_test(weights):
   f = open("mnist_test.csv")
   data = [(int((a:=(csv[:-1].split(",")))[0]), list(map(lambda x: int(x) / 255, a[1:]))) for csv in f.readlines()]
   corr = 0
   for target, pixels in data:
      outs = evaluate(classifier, pixels)
      out = outs.index(max(outs))
      if target == out:
        corr += 1
   print("Accuracy: "+str(corr/100)+"%")

def randweights():
   layer1 = [random.uniform(-1/28, 1/28) for i in range(784*800)] 
   layer2 = [random.uniform(-1/28, 1/28) for i in range(800*10)] 
   return [layer1, layer2]
   
def main():
   global classifier, data
   classifier = randweights()

   f = open("mnist_train.csv")
   data = [(int((a:=(csv[:-1].split(",")))[0]), list(map(lambda x: int(x) / 255, a[1:]))) for csv in f.readlines()]

   ct = 0

   for i in range(10):
      for target, mapixels in data:
         pixels = list(mapixels)
         classifier = smart_bp(classifier, pixels, target=[int(a == target) for a in range(10)], alpha=0.005)
         ct += 1
         if ct % 15 == 0:
            print(ct)
            print(evaluate(classifier, data[59999][1]))

      quick_test(classifier)
      
if __name__ == '__main__':
    main()
