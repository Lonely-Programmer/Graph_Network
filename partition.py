import random
import time
from itertools import combinations

def gen_graph(n):
    random.seed(2)
    ans = []
    for i in range(2 * n):
        tmp = []
        for j in range(2 * n):
            tmp.append(0)
        ans.append(tmp)
        
    for i in range(2 * n):
        for j in range(i + 1, 2 * n):
            r = random.randint(1,10)
            ans[i][j] = r
            ans[j][i] = r
            
    return ans

def calc_cost(G,X,Y):
    cost = 0
    for u in X:
        for v in Y:
            cost += G[u][v]
    return cost

def violence(G,n):
    min_cost = 9999999999
    min_X = None
    min_Y = None
    
    x_list = list(combinations(range(2 * n),n))
    for obj in x_list:
        X = set(obj)
        Y = set(list(range(2 * n))) - X
        c = calc_cost(G,X,Y)
        if c < min_cost:
            min_cost = c
            min_X = X
            min_Y = Y
    return (min_cost,min_X,min_Y)

def get_delta(G,X,Y,a,b):
    ans = 0
    for obj in X:
        if obj != a and obj != b:
            ans += G[a][obj]
            ans -= G[b][obj]
    for obj in Y:
        if obj != a and obj != b:
            ans += G[b][obj]
            ans -= G[a][obj]
    return ans

def tabu(G,n,trials,tabu_size):
    X = set()
    Y = set()
    min_X = set()
    min_Y = set()
    tabu_list = []
    
    for i in range(n):
        X.add(i)
        Y.add(i + n)
    cost = calc_cost(G,X,Y)
    min_cost = cost
    
    for i in range(trials):
        min_delta = 99999999999
        min_ab = None
        for a in X:
            for b in Y:
                if (a,b) in tabu_list or (b,a) in tabu_list:
                    continue
                delta = get_delta(G,X,Y,a,b)
                if delta < min_delta:
                    min_delta = delta
                    min_ab = (a,b)

        if min_ab == None:
            break

        a = min_ab[0]
        b = min_ab[1]
        X.remove(a)
        X.add(b)
        Y.remove(b)
        Y.add(a)
        cost += min_delta

        if cost < min_cost:
            min_cost = cost
            min_X = set(X)
            min_Y = set(Y)
            
        tabu_list.append(min_ab)
        while len(tabu_list) > tabu_size:
            del tabu_list[0]
    print(calc_cost(G,min_X,min_Y))
    return (min_cost,min_X,min_Y)

def work(n):
    G = gen_graph(n)
    print("n = ",n)
    t = time.time()
    print("Best solution:",violence(G,n))
    print(time.time() - t,"s")
    t = time.time()
    print("tabu:",tabu(G,n,1000,50))
    print(time.time() - t,"s")
    print()

def main():
    z = [5,6,7,8,9,10,11,12,13,14,15]
    for obj in z:
        work(obj)

main()

