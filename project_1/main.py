import random

POP_SIZE = 500
MUT_RATE = 0.1
TARGET = 'rayan ali'
GENES = ' abcdefghijklmnopqrstuvwxyz'

def initializePop(TARGET):
    population = list()
    tar_len = len(TARGET)

    for i in range(POP_SIZE):
        temp = list()
        for j in range(tar_len):
            temp.append(random.choice(GENES))
        population.append(''.join(temp))

    return population

# print(list( zip( TARGET, initializePop(TARGET)[0] ) ))

def fitnessCalc(TARGET, chromoFromPop):
    diff = 0
    for tarChar, chrChar in zip(TARGET, chromoFromPop):
        if tarChar != chrChar: diff += 1
    return [chromoFromPop, diff]

# A população vem junto com o resultado do fitness
def selection(population, TARGET):
    sorted_chromo_pop = sorted(population, key= lambda x: x[1])
    return sorted_chromo_pop[:int(0.5*POP_SIZE)] # melhores 50%

# def crossover(selecteChromo, chromoLen, population):
#     off

print(len(initializePop(TARGET)[:int(POP_SIZE*0.5)]))
    