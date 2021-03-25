import random
import math
import matplotlib.pyplot as plt
import numpy as np

def gen_graph(vertex,edge,delta):
    ans = []
    for i in range(vertex):
        ans.append(set())

    if edge > vertex * (vertex - 1) // 2:
        print('Edges too much compared to vertex!')
        return ans

    for i in range(vertex):
        while len(ans[i]) < delta:
            while True:
                end = random.randint(0,vertex-1)
                if i != end and end not in ans[i]:
                    break
            ans[i].add(end)
            ans[end].add(i)
            edge -= 1

    if edge < 0:
        print('Edges too few compared to delta!')
        
    while edge > 0:
        while True:
            start = random.randint(0,vertex-1)
            end = random.randint(0,vertex-1)
            if start != end and end not in ans[start]:
                break
        ans[start].add(end)
        ans[end].add(start)
        edge -= 1

    return ans

def dominate(G,flag):
    vertex = len(G)
    chosen = set()
    unchosen = set(range(vertex))
    dominated = set()
    undominated = set(range(vertex))

    while len(undominated) > 0:
        #print(chosen,undominated)
        max_dominate = 0
        max_index = -1
        if flag:
            candidate = unchosen
        else:
            candidate = undominated
            
        for v in candidate:
            cnt = 0
            for end in G[v]:
                if end in undominated:
                    cnt += 1
            if v in undominated:
                cnt += 1
                
            if cnt > max_dominate:
                max_index = v
                max_dominate = cnt

        chosen.add(max_index)
        unchosen.remove(max_index)
        dominated.add(max_index)
        undominated.discard(max_index)
        for end in G[max_index]:
            dominated.add(end)
            undominated.discard(end)
    return chosen

def work(G,vertex,edge,delta,verbose = False):
    ans1 = dominate(G,True)
    ans2 = dominate(G,False)
    bound = vertex * (1+math.log(delta+1)) / (delta+1)

    if verbose:
        print(G)
        print(len(ans1))
        print(ans1)
        print(len(ans2))
        print(ans2)
        print("bound:",bound)
    return [ans1,ans2,bound]

def vertex_test():
    edge = 1000
    delta = 2
    candidate = [50,100,200,300,400,500]
    zans1 = []
    zans2 = []
    zbound = []
    
    for vertex in candidate:
        G = gen_graph(vertex,edge,delta)
        ans1,ans2,bound = work(G,vertex,edge,delta,False)
        print(vertex,len(ans1),len(ans2),bound)
        zans1.append(len(ans1))
        zans2.append(len(ans2))
        zbound.append(bound)
    draw(candidate,zans1,zans2,zbound,'顶点个数','顶点数量')

def edge_test():
    vertex = 100
    delta = 2
    candidate = [200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400]
    zans1 = []
    zans2 = []
    zbound = []

    for edge in candidate:
        G = gen_graph(vertex,edge,delta)
        ans1,ans2,bound = work(G,vertex,edge,delta,False)
        print(edge,len(ans1),len(ans2),bound)
        zans1.append(len(ans1))
        zans2.append(len(ans2))
        zbound.append(bound)
    draw(candidate,zans1,zans2,zbound,'边条数','边的数量')

def delta_test():
    vertex = 100
    edge = 500
    candidate = [1,2,3,4,5,6,7]
    zans1 = []
    zans2 = []
    zbound = []

    for delta in candidate:
        G = gen_graph(vertex,edge,delta)
        ans1,ans2,bound = work(G,vertex,edge,delta,False)
        print(delta,len(ans1),len(ans2),bound)
        zans1.append(len(ans1))
        zans2.append(len(ans2))
        zbound.append(bound)
    draw(candidate,zans1,zans2,zbound,'δ','δ')

def draw(x,y1,y2,y3,xname,tname):
    font1 = {'size': 23}
    plt.figure(figsize=(10,7))
    plt.tick_params(labelsize=23)
    plt.title(tname+'与支配集顶点数量的关系',fontsize=23)
    plt.xlabel(xname,font1)
    plt.ylabel("支配集顶点的个数",font1)
    #plt.plot(x,y,color='green',linewidth = 3)
    plt.plot(x,y1,marker='o',label='贪心算法1',linestyle='-.')
    plt.plot(x,y2,marker='o',label='贪心算法2',linestyle=':')
    plt.plot(x,y3,marker='o',label='上界')
    plt.legend(loc = 'upper right',prop=font1)
    plt.show()

def main():
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus']=False
    random.seed(0)
    edge_test()
    delta_test()
    vertex_test()

main()
