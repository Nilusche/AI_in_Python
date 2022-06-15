import numpy as np
import random
from threading import Thread
import concurrent.futures
class SimulatedGeneticAlgorithm:
    
    def __init__(self,state):
        self.state = state
        self.crossoverpoint = -1
        self.generation = 0

    def get_gene_from_state(self):
        gene = []
        for i in range(8):
            found = False
            for j in range(7, -1,-1):
                if self.state[j][i] == "♛":
                    gene.append(8-j-1)
                    found = True
            if not found:
                gene.append("*")
        
        return gene

    def set_state_with_gene(self, gene):
        if gene is None:
            return
        for i in range(8):
            for j in range(7, -1,-1):
                if gene[i]!= "*" and 8-j-1 == gene[i]:
                    self.state[j][i] = "♛"
                else:
                    self.state[j][i] = "□"
                
        pass

    def __generate_gene(self):
        gene = np.random.randint(low=0, high=7, size=8)
        return gene
    
    def generate_Population(self, size= 10):
        population = []
        for i in range(size):
            population.append(self.__generate_gene())

        return np.array(population)

    def fitness_function(self,genearray):
        gene = np.array(genearray)
        attacks = 0
        row_col_attacks = abs(len(gene)-len(np.unique(gene)))
        attacks += row_col_attacks
        for i in range(len(gene)):
            for j in range(i,len(gene)):
                if i!=j:
                    dx = abs(i-j)
                    dy = abs(gene[i]-gene[j])
                    if dx == dy:
                        attacks+=1
        return 28 - attacks  

    def is_population_fit(self, population):
        for x in population:
            if self.fitness_function(x) == 28:
                return x

    def small_random_probability(self, num):
        rand = random.SystemRandom().random()
        #print("mutation", rand)
        return rand <=num
    
    def reproduce(self, x, y):
        crossover_point = np.random.choice(x.shape[0], 1, replace=False)[0]
        x1 = x[:crossover_point]
        x2 = x[crossover_point:]
        y1 = y[:crossover_point]
        y2 = y[crossover_point:]        
        child1 = np.concatenate([x1, y2])
        child2 = np.concatenate([y1, x2])
        
        #Major Performance Optimization
        #Child 1 is not fitter than their parents
        if self.fitness_function(x)> self.fitness_function(child1) or self.fitness_function(y)> self.fitness_function(child1):
            if self.fitness_function(x)>self.fitness_function(y):
                child1 = x
            else:
                child1 = y         
        #Child 2 is not fitter than their parents
        if self.fitness_function(x)> self.fitness_function(child2) or self.fitness_function(y)> self.fitness_function(child2):
            if self.fitness_function(x)>self.fitness_function(y):
                child2 = x
            else:
                child2 = y         
        
        #if both children were dismissed  
               
        if (child1 == x).all() and (child2 == x).all():
            child1 = y
        elif (child1 == y).all() and (child2 == y).all():
            child1 = x 
           

        return child1, child2, crossover_point

    def parentselection(self, population):

        #Get Random parent
        '''
        return np.array(population[np.random.choice(population.shape[0],size=1, replace = False),:][0]), np.array(population[np.random.choice(population.shape[0],size=1, replace = False),:][0])
        '''
        
        #Stochastic Unviversal Sampling
        #Get fitness levels of population and choose offspring based on distributed probability
        '''
        fitness = []
        for x in population:
            fitness.append(self.fitness_function(x))
        return random.choices(population, weights=fitness,k=1)[0], random.choices(population, weights=fitness, k=1)[0]
        '''

        #Rank Selection
        '''
        population = np.ndarray.tolist(population)
        population.sort(key=self.fitness_function, reverse=True)
        parent1 = np.array(population[0])
        parent2 = np.array(population[1])
        population = np.array(population)
        return parent1, parent2
        '''
        
        #Tournament Selection
        
        #First parent selection
        k = random.randrange(1, len(population))
        p_list = np.ndarray.tolist(population)
        candidates = random.choices(p_list, k=k)
        candidates.sort(key=self.fitness_function, reverse=True)
        parent1 = candidates[0]

        #Second parent selection
        k = random.randrange(1, len(population))
        p_list = np.ndarray.tolist(population)
        candidates = random.choices(p_list, k=k)
        candidates.sort(key=self.fitness_function, reverse=True)
        population = np.array(population)
        parent2 = candidates[0]
        return np.array(parent1), np.array(parent2)
        


    def mutate(self, subject):
        index = np.random.choice(subject.shape[0], 1, replace=False)
        subject[index] = random.randint(0,7)
        return subject
    
    def get_current_max_fitness(self, population):
        max = -1
        for x in population:
            fitness = self.fitness_function(x)
            if max < fitness:
                max = fitness
        
        return max

    def kill_weak_individuals(self, population, number):
        p = np.ndarray.tolist(population)
        p.sort(key=self.fitness_function, reverse=False)
        return np.array(p[number:])

    def genetic_algorithm(self,population):
        #print("===================================")
        population =self.kill_weak_individuals(population,60)
        while self.is_population_fit(population) is None and self.generation<100:
            #print("Generation: ", self.generation)
            new_population = []
            population = self.kill_weak_individuals(population, 20);
            for _ in range(len(population)+20):
                x,y= self.parentselection(population)
                while (x == y).all():
                    x, y = self.parentselection(population)
                 
                child1, child2,  crossoverpoint = self.reproduce(x,y)
                if self.small_random_probability(0.8):
                    child1 = self.mutate(child1)
                if self.small_random_probability(0.8):
                    child2 = self.mutate(child2)
                chosenchild = random.choice([child1, child2])
                new_population.append(chosenchild)

            self.set_state_with_gene(chosenchild)

            self.generation+=1

            population = np.array(new_population)

        if self.is_population_fit(population) is not None:
            return self.generation
        return -1




BOARD = np.array([
    ["□", "□", "□", "□", "□", "□", "□", "□"],
    ["□", "□", "□", "□", "□", "□", "□", "□"],
    ["□", "□", "□", "□", "□", "□", "□", "□"],
    ["□", "□", "□", "□", "□", "□", "□", "□"],
    ["□", "□", "□", "□", "□", "□", "□", "□"],
    ["□", "□", "□", "□", "□", "□", "□", "□"],
    ["□", "□", "□", "□", "□", "□", "□", "□"],
    ["□", "□", "□", "□", "□", "□", "□", "□"], 
])

def simulation():
    
    n = 100
    sum = 0
    unsolved = 0
    total = n 
    for _ in range(n):
        s = SimulatedGeneticAlgorithm(BOARD)
        gens = s.genetic_algorithm(s.generate_Population(100))
        if gens ==-1:
            unsolved+=1
            total-=1
        sum+=gens
        s.generation = 0
    return sum/total, unsolved
    print(sum/n)
    print("Unsolved under 100 generations: ", unsolved)

if __name__ == '__main__':
    print("Number of simulations: 100 (3x)")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(simulation) for _ in range(3)]
        results = [f.result() for f in futures]
        for x in results:
            print(x[0])
            print("Unsolved under 100 generations: ", x[1])

    
