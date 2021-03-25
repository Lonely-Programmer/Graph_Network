import matplotlib.pyplot as plt
import networkx as nx
import random

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

random.seed(0)
data = [(100,200,2),(100,800,2),(100,1400,2),(100,500,1),(100,500,4),(100,500,7),(100,1000,2),(300,1000,2),(500,1000,2)]
for obj in data:
    vertex,edge,delta = obj
    zG = gen_graph(vertex,edge,delta)
    G = nx.Graph()
    for i in range(len(zG)):
        G.add_node(i)
    for i in range(len(zG)):
        for end in range(len(zG[i])):
            G.add_edge(i,end)

    options = {
        "node_color": "black",
        "node_size": 50,
        "linewidths": 0,
        #"edge_color": (0.5,0.5,0.5),
        "width": 0.1,
    }
    nx.draw(G, **options)
    plt.show()
