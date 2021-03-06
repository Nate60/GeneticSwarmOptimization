import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib, time
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter
from function_list import *
from matplotlib import cm

P_MAX = 100
NFC = 5000
CR = 0.9
F = 0.8
D = 2
e = int(sys.argv[1])
prefix = ""

# def graph(pop, fcn):
#     fig = plt.figure()
#     ax = fig.add_subplot(111,projection='3d')
#     x1 = y1 = np.arange(-10, 10, 0.05)
#     X, Y = np.meshgrid(x1,y1)
#     zs = np.array([eval([x1,y1],fcn) for x1,y1 in zip(np.ravel(X), np.ravel(Y))])
#     Z = zs.reshape(X.shape)

#     ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, alpha=0.5)
#     ax.set_xlabel('X Label')
#     ax.set_ylabel('Y Label')
#     ax.set_zlabel('Z Label')

#     for x in range(P_MAX):
#         ax.scatter(pop[x][0], pop[x][1], eval(pop[x],e), lw=5, color='green')
#     plt.show()

class plot3dClass( object ):

    def __init__( self,x1, y1, X, Y, zs, Z):
        self.x1 = x1
        self.y1 = y1
        self.X = X
        self.Y = Y
        self.zs = zs
        self.Z = Z
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot( 111, projection='3d' )

        self.ax.w_zaxis.set_major_locator( LinearLocator( 10 ) )
        self.ax.w_zaxis.set_major_formatter( FormatStrFormatter( '%.03f' ) )
        self.surf = self.ax.plot_surface( 
            self.X, self.Y, self.Z, cmap=cm.coolwarm, alpha=0.5 )
        # plt.draw() maybe you want to see this frame?

    def drawNow( self, pop, h, pnum):
        plt.cla()
        self.surf = self.ax.plot_surface( 
            self.X, self.Y, self.Z, cmap=cm.coolwarm, alpha=0.5 )
        for x in range(pnum):
            self.ax.scatter(pop[x][0], pop[x][1], h[x], lw=5, color='green')
        plt.draw()
        self.fig.canvas.flush_events()                      # redraw the canvas

matplotlib.interactive(True)

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
    elif(E == 8):
        prefix = "katsuura"
        return katsuura(xinputs)

x1 = y1 = np.arange(-10, 10, 0.05)
X, Y = np.meshgrid(x1,y1)
zs = np.array([eval([x1,y1],e) for x1,y1 in zip(np.ravel(X), np.ravel(Y))])
Z = zs.reshape(X.shape)
p = plot3dClass(x1,y1,X,Y,zs,Z)


print "Init..."

#for r in range(1, 52):
pop = np.random.uniform(-10.0, 10.0, (P_MAX, D))
fness = [eval(pop[x],e) for x in range(P_MAX)]
start = time.time()
end = time.time() - start
for x in range(0, NFC/P_MAX * D):
    best = fness[0]
    end = time.time() - start
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
        
        if(fness[j] < best):
            best = fness[j]

    print("%3d  function: %s    time: %10.4f s %10.10f" % ((x * 1.0)/(NFC/P_MAX * D) * 100, prefix, end, best))

    for j in range(P_MAX):
        pop[j] = pop_new[j]
        
    
    #graph(pop, e)
    if(x % 6 == 0):
        p.drawNow(pop,fness,P_MAX)
    if(x == 0):
        time.sleep(1)


