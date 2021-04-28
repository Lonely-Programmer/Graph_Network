import random
from itertools import combinations

n = 15
P = [135,139,149,150,156,163,173,184,192,201,210,214,221,229,240]
W = [70,73,77,80,82,87,90,94,98,106,110,113,115,118,120]
C = 750
e = 2.7182818284590452

def violence():
    zp = 0
    zw = 0
    ans = -1
    for i in range(2**n):
        w = 0
        p = 0
        for j in range(n):
            t = (i & (1<<j)) >> j
            w += W[-j] * t
            p += P[-j] * t
        if w <= C and p >= zp:
            ans = i
            zp = p
            zw = w
    ans = bin(ans)[2:]
    ans = [int(s) for s in ans]
    return (ans,zp,zw)

def dp():
    ans = [0] * (C + 1)
    for i in range(n):
        for j in range(C,-1,-1):
            if j >= W[i]:
                ans[j] = max(ans[j],ans[j-W[i]] + P[i])
    return ans[-1]

def gen_neighbor(n,d):
    ans = []
    for i in range(1,d+1):
        ans += list(combinations(range(n),i))
    return ans

def sa(T,alpha,neighbor_size):
    random.seed(0)
    ans = [0] * n
    weight = 0
    price = 0
    max_ans = None
    max_price = 0
    max_weight = 0
    max_T = None
    while T > 1:
        neighbor = gen_neighbor(n,neighbor_size)
        flag = False
        for i in range(100):
            obj = random.choice(neighbor)
            new_weight = weight
            new_price = price
            for item in obj:
                if ans[item] == 0:
                    new_weight += W[item]
                    new_price += P[item]
                elif ans[item] == 1:
                    new_weight -= W[item]
                    new_price -= P[item]
                else:
                    print("Error!")
            if new_weight > C:
                continue
            if new_price > price or random.random() < e ** ((new_weight - weight) / T):
                price = new_price
                weight = new_weight
                for item in obj:
                    ans[item] = 1 - ans[item]
                flag = True
            if price > max_price:
                max_price = price
                max_weight = weight
                max_ans = ans[:]
                max_T = T
            if flag:
                break
            
        if not(flag):
            break      
        T *= alpha
    return (max_ans,max_price,max_weight,max_T)

def tabu(neighbor_size,trials,tabu_size):
    global_ans = None
    global_price = 0
    global_weight = 0
    tabu_list = []

    prev_ans = [0] * n
    prev_price = 0
    prev_weight = 0
    
    for i in range(trials):
        neighbor = gen_neighbor(n,neighbor_size)
        max_ans = None
        max_price = 0
        max_weight = 0
        max_neighbor = None
        for obj in neighbor:
            if obj in tabu_list:
                continue
            new_price = prev_price
            new_weight = prev_weight
            for item in obj:
                if prev_ans[item] == 0:
                    new_weight += W[item]
                    new_price += P[item]
                elif prev_ans[item] == 1:
                    new_weight -= W[item]
                    new_price -= P[item]
                else:
                    print("Error!")
            if new_weight > C:
                continue
            if new_price > max_price:
                max_price = new_price
                max_weight = new_weight
                max_ans = prev_ans[:]
                max_neighbor = obj
                for item in obj:
                    max_ans[item] = 1 - prev_ans[item]
                    
        if max_ans == None:
            break
        if max_price > global_price:
            global_price = max_price
            global_weight = max_weight
            global_ans = max_ans[:]
            
        tabu_list.append(max_neighbor)
        while len(tabu_list) > tabu_size:
            del tabu_list[0]

        prev_price = max_price
        prev_weight = max_weight
        prev_ans = max_ans[:]

    return (global_ans,global_price,global_weight)

def work1():
    print("Algorithm 1")
    print("[T]")
    T_list = [1000,1200,1400,1600,1800,2000]
    for obj in T_list:
        print("T =",obj)
        print(sa(obj,0.999,1))
        print()
    print("[alpha]")
    alpha_list = [0.999,0.99,0.95,0.9,0.8,0.7]
    for obj in alpha_list:
        print("alpha =",obj)
        print(sa(2000,obj,1))
        print()
    print("[d]")
    d_list = [1,2,3,4,5,6,7]
    for obj in d_list:
        print("d =",obj)
        print(sa(2000,0.99,obj))
        print()

def work2():
    print("Algorithm 2")
    print("[d]")
    d_list = [1,2,3,4,5,6,7]
    for obj in d_list:
        print("d =",obj)
        print(tabu(obj,200,20))
        print()
    print("[trials]")
    trials_list = [1,2,3,4,5]
    for obj in trials_list:
        print("trials =",obj)
        print(tabu(5,obj,20))
        print()
    print("[size]")
    tabu_list = [1,2,3,5,10,15,20,50,100]
    for obj in tabu_list:
        print("size =",obj)
        print(tabu(3,200,obj))
        print()
                
def main():
    work1()
    work2()
    print(dp())
    print(sa(2000,0.999,1))
    print(tabu(5,20,20))

main()
