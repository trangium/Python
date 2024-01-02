import torch
import torch.nn as nn

def calc(sample):
    dist = ((sample[2]-sample[0])**2 + (sample[3] - sample[1])**2)**0.5
    return torch.tensor([dist, 1 if dist < sample[4] else 0])

model = nn.Sequential(
    nn.Linear(5, 128),  # Input size 5, output size 128
    nn.SiLU(),          # ReLU activation function
    nn.Linear(128, 64),  # Input size 128, output size 64
    nn.SiLU(),          # ReLU activation function
    nn.Linear(64, 2)    # Input size 64, output size 2
)

learning_rate = 0.05
batch_size = 1
loss_fn = torch.nn.MSELoss(reduction='sum')

def test(model, samples=1000):
    loss = 0
    for i in range(samples):
        sample = torch.rand(5)*2-1
        sample[4] += 1
        loss += loss_fn(model(sample), calc(sample))
    return loss / samples

for i in range(2000001):
    sample = torch.rand(5)*2-1
    sample[4] += 1
    loss = loss_fn(model(sample), calc(sample))
    loss.backward()

    if i % batch_size == 0:
        with torch.no_grad():
            for param in model.parameters():
                param -= learning_rate * param.grad
        model.zero_grad()
    
    if i%1000 == 0:
        test_loss = test(model)
        print(i, "\tLoss: ", test_loss)
        if test_loss < 0.027:
            learning_rate = 0.01
        if test_loss < 0.020:
            learning_rate = 0.002
        if test_loss < 0.016:
            learning_rate = 0.0004

print(model(torch.tensor([-0.4, 0.6, 0.9, -0.1, 1.57])))