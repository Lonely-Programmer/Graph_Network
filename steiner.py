import random

rx = dict()
live_point = set()
live_pair = set()

def initialize(n):
    for i in range(n):
        rx[i] = 0
        live_point.add(i)
        for j in range(i + 1, n):
            live_pair.add((i,j))

def get_all_x():
    return list(live_point)

def get_all_yz(x):
    ans = set()
    for obj in live_pair:
        if x in obj:
            ans.add(list(set(obj) - set([x]))[0])
    
    return list(ans)

def switch(state,n,x,y,z):
    goal = (n - 1) // 2
    if (y,z) in live_pair or (z,y) in live_pair:
        state.append((x,y,z))
        for obj in [x,y,z]:
            rx[obj] += 1
            if rx[obj] == goal:
                live_point.remove(obj)

        live_pair.discard((x,y))
        live_pair.discard((y,x))
        live_pair.discard((y,z))
        live_pair.discard((z,y))
        live_pair.discard((z,x))
        live_pair.discard((x,z))
                    
    else:
        for i in range(len(state)):
            obj = state[i]
            
            if y in obj and z in obj:
                w = list(set(state[i]) - set((y,z)))[0]
                del state[i]
                state.append((x,y,z))

                live_point.add(w)
                rx[w] -= 1
                rx[x] += 1
                if rx[x] == goal:
                    live_point.remove(x)

                live_pair.add((w,y))
                live_pair.add((y,w))
                live_pair.add((w,z))
                live_pair.add((z,w))
                live_pair.discard((x,y))
                live_pair.discard((y,x))
                live_pair.discard((x,z))
                live_pair.discard((z,x))
                return
        print("ERROR")

def steiner(n):
    state = []
    goal = n * (n - 1) // 6
    while len(state) < goal:
        x = random.choice(get_all_x())
        y, z = random.sample(get_all_yz(x),2)
        switch(state,n,x,y,z)

    for i in range(len(state)):
        state[i] = sorted(list(state[i]))
        for j in range(len(state[i])):
            state[i][j] += 1
        state[i] = tuple(state[i])
    state.sort()
        
    return state

def check(state,n):
    flag = True
    cnt_dict = dict()
    for i in range(1,n + 1):
        for j in range(i + 1, n + 1):
            cnt_dict[(i,j)] = 0
            cnt_dict[(j,i)] = 0
    for obj in state:
        for i in range(len(obj)):
            for j in range(i + 1,len(obj)):
                cnt_dict[(obj[i],obj[j])] += 1
                cnt_dict[(obj[j],obj[i])] += 1
    for i in range(1,n + 1):
        for j in range(i + 1, n + 1):
            if cnt_dict[(i,j)] != 1:
                print(i,j,cnt_dict[(i,j)])
                flag = False
    return flag

def work(n):
    random.seed(0)
    initialize(n)
    state = steiner(n)
    print("n =",n)
    print(state)
    print(check(state,n))
    print()

def main():
    test = [1, 2]
    for obj in test:
        work(6 * obj + 1)
        work(6 * obj + 3)
        
main()
