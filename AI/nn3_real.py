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

def lazy_bp(weights, input_vals, target=1, alpha=0.1, epsilon=1e-6):
   new_weights = [list(layer) for layer in weights]
   old_eval = (target - evaluate(weights, input_vals)[0])**2/2
   for layer_ind, layer in enumerate(weights):
      for weight_ind, weight in enumerate(layer):
         weights[layer_ind][weight_ind] += epsilon
         new_eval = (target - evaluate(weights, input_vals)[0])**2/2
         derivative = (new_eval - old_eval) / epsilon
         # print(layer_ind, weight_ind, derivative, sep="\t")
         new_weights[layer_ind][weight_ind] = weight - alpha * derivative
         weights[layer_ind][weight_ind] -= epsilon
   return new_weights

def smart_bp(weights, input_vals, target=1, alpha=0.1):
   layer_ct = len(weights)
   
   new_weights = [list(layer) for layer in weights]
   all_eval = list(all_evaluate(weights, input_vals))

   node_derivs = []

   for layer_ind in range(layer_ct-1, -1, -1):
      next_nodes = all_eval[layer_ind+1]
      prev_nodes = all_eval[layer_ind]
      
      if layer_ind == layer_ct - 1:
         next_node_derivs = [implicit(x) * (x-target) for x in next_nodes]
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

def stress_test(weights):
   goofs = 0
   for i in range(100000):
      x = random.uniform(-1.5, 1.5)
      y = random.uniform(-1.5, 1.5)
      expect = 1 if x**2+y**2 < 1 else 0
      res = evaluate(weights, [x, y, 1])[0]
      if abs(expect-res) >= 0.5:
         goofs += 1
         if goofs < 5:
            print("Mistake:", "("+str(x)+", "+str(y)+")")
   print("Goof count:", goofs)

def quick_test(weights):
   goofs = 0
   for xi in range(-24, 24):
      for yi in range(-24, 24):
         x = (xi + 0.383) / 16.553
         y = (yi + 0.476) / 16.438
         expect = 1 if x**2+y**2 < 1 else 0
         res = evaluate(weights, [x, y, 1])[0]
         if abs(expect-res) >= 0.5:
            goofs += 1
   print("Goofs per 100k:", round(goofs / 2304 * 100000))
   return goofs / 2304

def randweights():
   layer1 = [random.uniform(-0.5, 0.5) for i in range(3*250)] 
   layer2 = [random.uniform(-0.5, 0.5) for i in range(250*20)] 
   layer3 = [random.uniform(-0.5, 0.5) for i in range(20*20)]
   layer4 = [random.uniform(-0.5, 0.5) for i in range(20*1)]
   return [layer1, layer2, layer3, layer4]
   
def main():
   global classifier
   classifier = randweights()

   for i in range(1000000):
      if i % 1000 == 0:
         print(i)
         lr = quick_test(classifier)
         print(max(i for j in classifier for i in j))
      x = 0
      y = 0
      for i in range(13):
         if 0.94 < x**2 + y**2 < 1.06: break
         x = random.uniform(-1.5, 1.5)
         y = random.uniform(-1.5, 1.5)
      res = 1 if x**2+y**2 < 1 else 0
      classifier = smart_bp(classifier, [x, y, 1], target=res, alpha=lr*0.4)



   
      
if __name__ == '__main__':
    main()

# Vincent Trang, Period 4, 2023
