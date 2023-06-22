import math
import random
import numpy as np
import matplotlib.pyplot as plt
import time
import numpy as np
import copy

max_iterations = 50
k = 5
max_amount = 40020
X = range(-5000,5001)
Y = range(-5000,5001)

def generate_start(starting_points):


    for i in range(20):
        
        while(True):
            
            x = random.randrange(X[0],-(X[0]))
            y = random.randrange(Y[0],-(Y[0]))
            i = x,y

            if i not in starting_points:    
                break

        starting_points[i] = 0

    return    

def generate_other(all_points):

        while(len(all_points) < max_amount):
            
            #vyber nahodneho z prvych 20
            prev_point = random.choice(list(all_points.items()))

            #vypocet distance
            distance_x = -X[0] - abs(prev_point[0][0]) 
            distance_y = -Y[0] - abs(prev_point[0][1])
            while(True):

                #zredukovanie offsetu
                if(distance_x < 100):

                    if(prev_point[0][0] > 0):
                        x_offset = random.randrange(-100, 100 - distance_x)
                    
                    else:
                        x_offset = random.randrange(-100 + distance_x, 100)

                else:
                    x_offset = random.randrange(-100, 100)

                
                if(distance_y < 100):

                    if(prev_point[0][1] > 0):
                        y_offset = random.randrange(-100, 100 - distance_y)
                    
                    else:
                        y_offset = random.randrange(-100 + distance_y, 100)

                else:
                    y_offset = random.randrange(-100, 100)

                i = prev_point[0][0]+x_offset,prev_point[0][1]+y_offset

                #check ci je unikatny
                if i not in all_points:
                    break
            
            all_points[(prev_point[0][0]+x_offset,prev_point[0][1]+y_offset)] = 0

def init_centriod(centroids):

    for i in range(k):
        
        while(True):
            
            x = random.randrange(X[0],-(X[0]))
            y = random.randrange(Y[0],-(Y[0]))
            i = x,y

            if i not in centroids:    
                break
        
        centroids.append(i)

def distanceforcentroid(centroids, pos):

    #vypocet vzdialenosti bodu od centroidu pomocou euclivovej vety
    dist = math.dist(centroids,pos)
    return dist
    
# viem pouzit aj pri medoid aj pri centroid
def label_clusters(centroids,all_points):
    
    for k, v in all_points.items():
        index = 0
        distances = []

        for centroid in centroids:
            
            #Zistim pre kazdy bod dlzku od centroidu 
            distances.append((distanceforcentroid(centroid, k), index))
            
            index+=1

        #Zistim najmensiu cestu ku centroidu
        sorted_distances = sorted(distances, key=lambda tup: tup[0])
        #Zapisem mu jeho index (farbu)
        all_points[k] = sorted_distances[0][1]
               
def update_centroid(centroids,all_points):

    for i in range(len(centroids)):
        
        #vsetky x a y pre jeden centroid
        temp_x = []
        temp_y = []

        for k, v in all_points.items():

            if v == i:
                temp_x.append(k[0])
                temp_y.append(k[1])
        
        #vypocitam novy centroid
        x = np.mean(temp_x)
        y = np.mean(temp_y)

        new_pos = x,y

        #zapisem do pola
        centroids[i] = new_pos       
    

def k_means_centroid(centroids,all_points):

    #vytvorim pociatocne cetroids
    init_centriod(centroids)

    #zistim ktore body ku ktoremu patria a "vyfarbim ich"
    label_clusters(centroids,all_points)
    
    #prva mapa
    visual(centroids,all_points)
    for iteration in range(max_iterations):
        
        old_centroid = []
        old_centroid = copy.deepcopy(centroids)
        #vypocitam nove centroidy podla mean
        update_centroid(centroids,all_points)

        if (old_centroid == centroids):
            print("Najlepsia optimalizacia v " , iteration, "iteracii")
            break
        
        #zistim na novo ktore body patria ku ktoremu centroidu
        label_clusters(centroids,all_points)


def init_medoid(medoids,all_points):

    for medoid in range(0,k):
        while(True):

            #vyberem random medoid
            medoid = random.choice(list(all_points.keys()))

            
            #unikatny medoid
            if medoid not in medoids:    
                break

        #vlozim ho do pola
        medoids.append(medoid)

def update_medoids(medoids,all_points):
    
    for medoid in range(len(medoids)):
        
        distances = []
        all_distances = []
        #vsetky x a y pre jeden centroid
        temp_x = []
        temp_y = []

        for k, v in all_points.items():

            if v == medoid:
                temp_x.append(k[0])
                temp_y.append(k[1])
        
        #vypocitam novy centroid
        x = np.mean(temp_x)
        y = np.mean(temp_y)

        x = round(x)
        y = round(y)
        #pozicia noveho centroidu
        new_pos = x,y
    
        #zistim dlzku vsetkych od noveho centroidu
        for k, v in all_points.items():
            if v == medoid:
                
                #dlzky od kazdeho bodu
                distances.append(distanceforcentroid(new_pos, k))
                #pole bodov
                all_distances.append(k)
                
        #Zistim namensiu vzdialenost od noveho centroidu
        min_distance = min(distances)
        #index najlepsieho medoidu
        min_index = distances.index(min_distance)
        
        #novy medoid
        new_medoid = all_distances[min_index]
        
        #zapisem
        medoids[medoid] = new_medoid  

        
def k_means_medoid(medoids,all_points):
    
    init_medoid(medoids,all_points)
    
    label_clusters(medoids,all_points)

    visual(medoids, all_points)
    for iteration in range(max_iterations):
        
        old_medoid = []
        old_medoid = copy.deepcopy(medoids)
        #vypocitam nove centroidy podla mean
        update_medoids(medoids,all_points)
        
        if (old_medoid == medoids):
            print("Najlepsia optimalizacia v " , iteration, "iteratacii")
            break
        
        #zistim na novo ktore body patria ku ktoremu medoidu
        label_clusters(medoids,all_points)
       
        
def visual(centroids,starting_points):

        x_c = []
        y_c = []
        for k in centroids:
            x_c.append(k[0])
            y_c.append(k[1])
        
        x = []
        y = []
        colors = []
        for k, v in starting_points.items():
            x.append(k[0])
            y.append(k[1])

            if(v == 0):
                colors.append('#fccf03')
            elif(v == 1):
                colors.append('#2b2b2b')
            elif(v == 2):
                colors.append('#24fc03')
            elif(v == 3):
                colors.append('#03fcca')
            elif(v == 4):
                colors.append('#40dcff')
            elif(v == 5):
                colors.append('#40ff80')
            elif(v == 6):
                colors.append('#e35d5d')
            elif(v == 7):
                colors.append('#f2903a')
            elif(v == 8):
                colors.append('#670fff')
            elif(v == 9):
                colors.append('#ff0f8b')

        plt.scatter(x,y,c=colors)
        plt.scatter(x_c,y_c, marker="x", c="#000000")
        
        plt.xlim(-5000, 5000)
        plt.ylim(-5000, 5000)
        plt.show()  

def main():

    print("Ked chceme spustit k means s centroidom stacte: 1")
    print("Ked chceme spustit k means s medoidom stacte: 2")
    algo = input()
    starting_points = {}

    centroids = []
    medoids = []
    
    start = time.time()
    #Vygenerejuem prvych 20 bodov
    generate_start(starting_points)

    #Vygenerujem ostatne body podla max_amount
    generate_other(starting_points)

    if(algo == str(1)):
        # k means centroid
        k_means_centroid(centroids,starting_points)
        done = time.time()
        elapsed = done - start
        print(elapsed, "sekund")
        #pre centroid
        visual(centroids,starting_points)

    elif(algo == str(2)):
        k_means_medoid(medoids, starting_points)
        done = time.time()
        elapsed = done - start
        print(elapsed, "sekund")
    
        visual(medoids,starting_points)

 
if __name__ == "__main__":
    main()