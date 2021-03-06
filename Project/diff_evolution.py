import numpy as np
import sys
from time import time
from function_list import *

NFC = 5000
P_MAX = 100
CR = 0.9
F = 0.8
D = int(sys.argv[1])
prefix = ""


def eval(xinputs, E):
    global prefix
    if(E == 0):
        prefix = "elliptic"
        return high_conditioned_elliptic(xinputs)
    elif(E == 1):
        prefix = "cigar"
        return bent_cigar(xinputs)
    elif(E == 2):
        prefix = "discus"
        return discus(xinputs)
    elif(E == 3):
        prefix = "rosen"
        return rosenbrock(xinputs)
    elif(E == 4):
        prefix = "ackley"
        return ackley(xinputs)
    elif(E == 5):
        prefix = "weier"
        return weierstrass(xinputs)
    elif(E == 6):
        prefix = "grie"
        return griewank(xinputs)
    elif(E == 7):
        prefix = "rast"
        return rastrigin(xinputs)
    else:
        prefix = "katsuura"
        return katsuura(xinputs)
print "Init..."
start = time()
end = time() - start
for e in range(0, 9):
    avg = np.random.uniform(0.0,0.0,(NFC/P_MAX*D))
    runs = np.random.uniform(0.0,0.0,(P_MAX * 51, D))
    for r in range(1, 52):
        pop = np.random.uniform(-10.0, 10.0, (P_MAX, D))
        fness = [eval(pop[x],e) for x in range(P_MAX)]
        fgBest = fness[0]
        prev = fgBest
        for j in range(P_MAX):
            if(fness[j] < fgBest):
                fgBest = fness[j]

        end = time() - start
        print("iteration: %3d  function: %s    time: %10.4f s" % (r, prefix, end))

        for x in range(0, NFC/P_MAX * D):
            prev = fgBest
            pop_new = [[0.0 for i in range(D)] for k in range(P_MAX)]
            for j in range(P_MAX):
                a = 0
                b = 0
                c = 0
                mutated_v = [0.0 for i in range(D)]
                diff_v = [0.0 for i in range(D)]
                new_v = [0.0 for i in range(D)]
                while True:
                    a = np.random.randint(0, P_MAX)
                    if j != a:
                        break
                while True:
                    b = np.random.randint(0, P_MAX)
                    if b != a and b != j:
                        break
                while True:
                    c = np.random.randint(0, P_MAX)
                    if c != b and c != a and c != j:
                        break

                for i in range(D):
                    diff_v[i] = (pop[a][i] - pop[b][i]) * F
                    mutated_v[i] = diff_v[i] + pop[c][i]

                for i in range(D):
                    if (np.random.random() < CR) and (mutated_v[i] <= 10) and (mutated_v[i] >= -10):
                        new_v[i] = mutated_v[i]
                    else:
                        new_v[i] = pop[j][i]

                newfness = eval(new_v,e)

                if(newfness < fness[j]):
                    pop_new[j] = new_v
                    fness[j] = newfness
                else:
                    pop_new[j] = pop[j]

                if(fness[j] < fgBest):
                    fgBest = fness[j] 

            avg[x] += fgBest
            
            for j in range(P_MAX):
                pop[j] = pop_new[j]

        for x in range(P_MAX):
            runs[x+(P_MAX * (r-1))] = pop[x]
            #print str(e) +" " +  str(r) + " " + prefix

    for x in range (NFC/P_MAX*D):
        avg[x] /= 51
    
    out_file = open("data/" + str(D) + "_" + prefix + "_de_points" + ".csv","w")
    full_output = runs.tolist()
    for line in full_output:
        out_file.write(str(line)[1:-1] + ', ' + str(eval(line,e)) + "\n")
    out_file.close()

    plot_file = open("plots/" + str(D) + "_" + prefix + "_de_plot" + ".csv","w")
    for x in range(NFC/P_MAX*D):
        plot_file.write(str(avg[x]) + "\n")
    plot_file.close()
    