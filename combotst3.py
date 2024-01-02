import random


def run():
    money = 500
    steps = 0
    machinesBroken = 0

    while money > 0:
        steps += 1
        if random.random() < 0.5:
            money += 20
        elif random.random() < (0.5) ** (machinesBroken + 1):
            money -= 120
            machinesBroken += 1
        else:
            money -= 20

    return steps

steps = []
for i in range(1000):
    steps.append(run())

steps.sort(reverse=True)

print(steps)
