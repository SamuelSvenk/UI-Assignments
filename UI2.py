import random
from operator import itemgetter
import time

import numpy as np

X = 12
Y = 10

print_solution = False
stones = 6
max_generation = 20000
max_population = 100
solution_blocks = X * Y - 6
max_genes = (X + Y)  + stones
circuit = 2 * (X + Y) - 4

class garden:
    #garden
    blocks = []     
    population = []       
    startpoints = []
    stones = 6
    max_genes = (X + Y) + stones       
    circuit = 2 * (X + Y) - 4
    HELPER = True


def init_board():

    board = [[0 for i in range(X)]for i in range(Y)]
    stone = -1

          #Y,X
    board[4][2] = stone
    board[2][1] = stone
    board[3][4] = stone
    board[1][5] = stone
    board[6][8] = stone
    board[6][9] = stone

    return board

def print_board(board):

    print(np.matrix(board))


#Najde na obvode startovne pozicie pre mnicha
def get_startingpoints():
    for i in range(0, Y):
        for j in range(0, X):

            if (i == 0 or i == Y-1) and (garden.blocks[i][j] != -1):
                garden.startpoints.append([i, j], )
            elif (j == 0 or j == X-1) and (garden.blocks[i][j] != -1):
                garden.startpoints.append([i, j], )
        
    return

#Zistujem ci sa dostal mnich na spodok
def check_floor(monky):
    if monky == Y - 1:
        return 1

    return 0

def check_down(monkx, monky, monks_garden):
    if monky + 1 < Y and monks_garden[monky+1][monkx] == 0:
        return 1

    return 0


def check_left(monkx, monky, monks_garden):
    if monkx > 0 and monks_garden[monky][monkx-1] == 0:
        return 1

    return 0
    
def check_leftwall(monkx):
    if monkx == 0:
        return 1

    return 0

def check_up(monkx, monky, monks_garden):

    if monky > 0 and monks_garden[monky-1][monkx] == 0:
        return 1

    return 0


def check_ceiling(monky):
    if monky == 0:
        return 1

    return 0

def check_right(monkx, monky, monks_garden):
    if monkx + 1 < X and monks_garden[monky][monkx+1] == 0:
        return 1

    return 0

def check_rightwall(monkx):
    if monkx == X - 1:
        return 1

    return 0

            
def go_rake(monkx, monky, monks_garden, counter, move):
    check = 0
    fitness = 1


    if ((monks_garden[monky][monkx]) != 0):
        return 0   

    while 1:

        #Nastav pohyb
        monks_garden[monky][monkx] = counter

        #Pohyb dole
        if move == "S":

            if check_down(monkx, monky, monks_garden):            
                monky = monky + 1
                fitness += 1
                continue


            elif check_floor(monky):            
                return fitness
            
            #Alternativne pohyby
            elif check_right(monkx, monky, monks_garden):          
                move = "D"                                 
                continue
            
            elif check_left(monkx, monky, monks_garden):
                move = "A"
                continue
            
            #Mnich sa zasekol
            else:                                              
                return 0

        elif move == "W":

                if check_up(monkx, monky, monks_garden):            
                    monky = monky - 1
                    fitness += 1
                    continue


                elif check_ceiling(monky):            
                    return fitness
                    
                    #Alternativne pohyby
                elif check_right(monkx, monky, monks_garden):          
                    move = "D"                                 
                    continue
                    
                elif check_left(monkx, monky, monks_garden):
                    move = "A"
                    continue
                    
                    #Mnich sa zasekol
                else:                                              
                    return 0

        elif move == "A":

                if check_left(monkx, monky, monks_garden):            
                    monkx = monkx - 1
                    fitness += 1
                    continue


                elif check_leftwall(monkx):            
                    return fitness
                    
                    #Alternativne pohyby
                elif check_up(monkx, monky, monks_garden):          
                    move = "W"                                 
                    continue
                    
                elif check_down(monkx, monky, monks_garden):
                    move = "S"
                    continue
                    
                    #Mnich sa zasekol
                else:                                              
                    return 0

        elif move == "D":
                

                if check_right(monkx, monky, monks_garden):            
                    monkx = monkx + 1
                    fitness += 1
                    continue


                elif check_rightwall(monkx):            
                    return fitness
                    
                    #Alternativne pohyby
                elif check_up(monkx, monky, monks_garden):          
                    move = "W"                                 
                    continue
                    
                elif check_down(monkx, monky, monks_garden):
                    move = "S"
                    continue
                    
                    #Mnich sa zasekol
                else:                                              
                    return 0

    
    return 0


def delete_path(monks_garden, counter):

    for i in range(0, Y):
        for j in range(0, X):

            if monks_garden[i][j] == counter:
                monks_garden[i][j] = 0
             
    return

def test_monk(monk):

    monks_garden = init_board()
    fitness = 0   
    counter = 1

   
    # Hore "W", Dole "S", Doprava "D", Dolava "A" = WASD pohyb
    for startingpoint in monk[0]:

        # Ak je X 12 pojdeme dole od 0-11                                        
        if startingpoint < X:                                 
            fitness = go_rake(startingpoint, 0, monks_garden, counter, "S")

            #Ked nasiel cestu pripocitaj ju
            if(fitness != 0):
                monk[1]+= fitness

            #Musime zmazat cestu a ist na dalsieho monka s novou garden
            else:
                if(print_solution == True):
                    print_board(monks_garden)
                    break
                delete_path(monks_garden, counter)
                counter -= 1
                return fitness    


        #Ak je X=12 Y= 10 tak chceme ist dolava od 12-19
        elif startingpoint < X + Y - 2:
            fitness = go_rake(X - 1, startingpoint - X + 1, monks_garden, counter, "A")

            if(fitness != 0):
                monk[1]+= fitness
            
            else:
                if(print_solution == True):
                    print_board(monks_garden)
                    break
                delete_path(monks_garden, counter)
                counter -= 1
                return fitness    

        #Ak je X=12 Y= 10 tak chceme ist hore od 20-31
        elif startingpoint < 2 * X + Y - 2:
            fitness = go_rake((2 * X + Y - 3) - startingpoint,Y - 1,  monks_garden, counter, "W")

            if(fitness != 0):
                monk[1]+= fitness
            
            else:
                if(print_solution == True):
                    print_board(monks_garden)
                    break
                delete_path(monks_garden, counter)
                counter -= 1
                return fitness
                

        #31 - 39 doprava
        else:
            fitness = go_rake(0, 2 * X + 2 * Y - 4 - startingpoint,  monks_garden, counter, "D")

            if(fitness != 0):
                monk[1]+= fitness

            else:
                if(print_solution == True):
                    print_board(monks_garden)
                    break

                delete_path(monks_garden, counter)
                counter -= 1
                return fitness    

        counter+=1


                   
                   
    return fitness


def get_random(monk):

    rand = random.randint(0, circuit-1)

    #check na duplikaty
    while rand in monk[0]:                
        rand = random.randint(0, circuit - 1)


    return rand


def generate_monk(population):

    #For na vytvaranie monkov po max populaciu v generacii
    for i in range(max_population):
        #Novy monk s genom(startovne policko), fitness, poradie
        monk = [[], 0]       

        #Vytvaranie nahodnych monkov
        for j in range(max_genes):         
            monk[0].append(get_random(monk))

        #Testovanie monka
        test_monk(monk)
        #Pridanie monka do generacie
        population.append(monk)

def mutation(first_parent, second_parent):
    child = [[], 0]

    # Miesto od ktoreho sa vykona N-point crossover 3/4 z prveho rodica 1/4 z druheho
    ratio = max_genes/4 * 3
    ratio = int(round(ratio))

    #Uchovame geny z prveho rodica
    for i in range(0, ratio):                                  
        child[0].append(first_parent[0][i])

    for i in range(ratio, max_genes):
        child[0].append(second_parent[0][i])

    #Mutacia
    for gen in range(max_genes):                         
        if random.randint(0,1) <= 0.25:
            
            child[0][gen] = get_random(child)

    return child

def tournament(population):
    first_parent = random.randint(0, max_population - 1)
    second_parent = random.randint(0, max_population - 1)

    #Ak su rovnake zmenim parenta
    if(second_parent == first_parent):
        second_parent = random.randint(0, max_population - 1)

    #Vyberam lepsieho
    if population[first_parent][1] > population[second_parent][1]:
        return population[first_parent]
    else:
        return population[second_parent]


def roulette(fitness,population):

    rand = random.randint(0, fitness)

    for monk in reversed(population):
        rand -= monk[1]
        if rand < 1:
            return monk



def fitness(population):
    
    #Ak je solution vrat monka
    for monk in population:     
        if monk[1] == solution_blocks:
            return monk
    
    temp_population = []

    #Sort podla fitness prvy v poli bude najlepsi
    population.sort(key=itemgetter(1), reverse=True)

    #print("Fitness najlepsieho:", population[0][1])
    #print("Fitness najhorsieho:", population[max_population-1][1])

    #Elitizmus necham si top 2
    for i in range(2):
        temp_population.append(population[i])


    #Zistujem celkove fitness pre ruletovi vyber
    total_fitness = 0                                         
    for monk in population:
        total_fitness += monk[1]

    #Tournament vyber
    while len(temp_population) < max_population:
        first_parent = tournament(population)                             
        second_parent = tournament(population)
        if first_parent[1] > second_parent[1]:
            temp_population.append(mutation(first_parent, second_parent))
        else:
            temp_population.append(mutation(second_parent, first_parent))
    

        #Vyber ruletov
        first_parent = roulette(total_fitness,population)                 
        second_parent = roulette(total_fitness,population)
        if first_parent[1] > second_parent[1]:
            temp_population.append(mutation(first_parent, second_parent))
        else:
            temp_population.append(mutation(second_parent, first_parent))

    population.clear()
    

    #Zistenie novej fitness s novymi monkami
    for monk in temp_population:                               
        if monk[1] == 0:                                        
            test_monk(monk)
        population.append(monk)

    population.sort(key=itemgetter(1), reverse=True)
    

def main():

    #Nacitam si hraciu plochu
    #get_startingpoints()
    start = time.time()
    population = []
    generations = 1
    #Prva populacia vyriesenie hry
    generate_monk(population)
    global print_solution

    #Prechadzame generacie
    while generations < max_generation:
        
        fitness(population)

        if(population[0][1] == solution_blocks):
            print_solution = True
            print("Nasla sa najlepsia solution")
            print("Fitness najlepsieho jedinca je: ", population[0][1], "\n")
            test_monk(population[0])
            done = time.time()
            elapsed = done - start
            print(elapsed, "sekund")
            break

            
        elif(generations == max_generation-1):
            print_solution = True
            print("Nenasla sa najlepsia solution")
            print("Vysledok sa nasiel v generacii: ", generations)
            print("Fitness najlepsieho jedinca je: ", population[0][1], "\n")
            test_monk(population[0])
            done = time.time()
            elapsed = done - start
            print(elapsed, "sekund")
            break

        generations+=1


if __name__ == "__main__":
    main()

