import copy
import random
import numpy as np

tuple_cnt = dict()

def initialize(days,group_num,girls_per_group):
    state = []
    random.seed(4)
    for i in range(days):
        r = np.array(list(range(1,group_num*girls_per_group+1)))
        random.shuffle(r)
        tmp1 = []
        for j in range(group_num):
            tmp2 = []
            for k in range(girls_per_group):
                tmp2.append(r[j*girls_per_group+k])
            tmp1.append(tmp2)
        state.append(tmp1)
    
    for i in range(group_num * girls_per_group):
        for j in range(group_num * girls_per_group):
            tuple_cnt[(i+1,j+1)] = 0

    for i in range(days):
        for j in range(group_num):
            for k in range(girls_per_group):
                for m in range(k+1,girls_per_group):
                    tuple_cnt[(state[i][j][k],state[i][j][m])] += 1
                    tuple_cnt[(state[i][j][m],state[i][j][k])] += 1

    return state

def score_function(cnt):
    if cnt < 0:
        print("Error!")
        pass
    return abs(cnt - 1)

def get_delta(state,days,group_num,girls_per_group,zday,zgroup1,zgroup2,zx,zy):
    delta = 0
    for i in range(girls_per_group):
        girl = state[zday][zgroup1][zx]
        girl1 = state[zday][zgroup1][i]
        girl2 = state[zday][zgroup2][i]
        cnt1 = tuple_cnt[(girl,girl1)]
        cnt2 = tuple_cnt[(girl,girl2)]
        if zy != i:
            delta += score_function(cnt2 + 1) - score_function(cnt2)
        if zx != i:
            delta += score_function(cnt1 - 1) - score_function(cnt1)
            
    for i in range(girls_per_group):
        girl = state[zday][zgroup2][zy]
        girl1 = state[zday][zgroup2][i]
        girl2 = state[zday][zgroup1][i]
        cnt1 = tuple_cnt[(girl,girl1)]
        cnt2 = tuple_cnt[(girl,girl2)]
        if zx != i:
            delta += score_function(cnt2 + 1) - score_function(cnt2)
        if zy != i:
            delta += score_function(cnt1 - 1) - score_function(cnt1)

    return delta

def update_ans(state,days,group_num,girls_per_group,neighbor):
    zday,zgroup1,zgroup2,zx,zy = neighbor
    state[zday][zgroup1][zx], state[zday][zgroup2][zy] = state[zday][zgroup2][zy], state[zday][zgroup1][zx]
    return state

def update_cnt(state,days,group_num,girls_per_group,neighbor):
    zday,zgroup1,zgroup2,zx,zy = neighbor
    for i in range(girls_per_group):
        girl = state[zday][zgroup1][zx]
        girl1 = state[zday][zgroup1][i]
        girl2 = state[zday][zgroup2][i]
        if zy != i:
            tuple_cnt[(girl,girl2)] += 1
            tuple_cnt[(girl2,girl)] += 1
        if zx != i:
            tuple_cnt[(girl,girl1)] -= 1
            tuple_cnt[(girl1,girl)] -= 1
            
    for i in range(girls_per_group):
        girl = state[zday][zgroup2][zy]
        girl1 = state[zday][zgroup2][i]
        girl2 = state[zday][zgroup1][i]
        if zx != i:
            tuple_cnt[(girl,girl2)] += 1
            tuple_cnt[(girl2,girl)] += 1
        if zy != i:
            tuple_cnt[(girl,girl1)] -= 1
            tuple_cnt[(girl1,girl)] -= 1

def get_best_neighbor(state,days,group_num,girls_per_group,tabu_list):
    min_delta = 1000000000
    min_neighbor = None
    
    for i in range(days):
        for j in range(group_num):
            for k in range(j+1,group_num):
                for x in range(girls_per_group):
                    for y in range(girls_per_group):
                        if (i,state[i][j][x],state[i][k][y]) in tabu_list or (i,state[i][k][y],state[i][j][x]) in tabu_list:
                            continue
                        delta = get_delta(state,days,group_num,girls_per_group,i,j,k,x,y)
                        if delta < min_delta:
                            min_delta = delta
                            min_neighbor = (i,j,k,x,y)
                            
    return (min_delta,min_neighbor)

def sanpo(k,trials,tabu_size):
    n = 6 * k + 3
    days = (n - 1) // 2
    girls_per_group = 3
    group_num = n // girls_per_group

    state = initialize(days,group_num,girls_per_group)
    prev_score = calc_score(state)
    global_min = 1000000000
    global_ans = None
    tabu_list = []
    
    for i in range(trials):
        min_delta,min_neighbor = get_best_neighbor(state,days,group_num,girls_per_group,tabu_list)
        if min_neighbor == None:
            break
        min_score = prev_score + min_delta

        neighbor_i,neighbor_j,neighbor_k,neighbor_x,neighbor_y = min_neighbor
        tabu_list.append((neighbor_i,state[neighbor_i][neighbor_j][neighbor_x],state[neighbor_i][neighbor_k][neighbor_y]))
        while len(tabu_list) > tabu_size:
            del tabu_list[0]
            
        prev_score = min_score
        update_cnt(state,days,group_num,girls_per_group,min_neighbor)
        update_ans(state,days,group_num,girls_per_group,min_neighbor)

        if min_score < global_min:
            global_min = min_score
            global_ans = copy.deepcopy(state)

        if global_min == 0:
            break

    print(global_min)
    return global_ans

def calc_score(state):
    zdict = dict()
    days = len(state)
    group_num = len(state[0])
    girls_per_group = len(state[0][0])
    score = 0
    
    for i in range(group_num * girls_per_group):
        for j in range(group_num * girls_per_group):
            zdict[(i+1,j+1)] = 0

    for i in range(days):
        for j in range(group_num):
            for k in range(girls_per_group):
                for m in range(k+1,girls_per_group):
                    zdict[(state[i][j][k],state[i][j][m])] += 1
                    zdict[(state[i][j][m],state[i][j][k])] += 1

    for i in range(group_num * girls_per_group):
        for j in range(i+1,group_num * girls_per_group):
            score += score_function(zdict[(i+1,j+1)])

    return score

def main():
    ans = sanpo(2,2000,30)
    calc_score(ans)

    for obj in ans:
        print(obj)

main()
