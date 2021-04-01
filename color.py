import numpy as np
import time

def gen_K4(N,x,y):
    ans = []
    for i in range(N):
        for j in range(i+1,N):
            if i != x and i != y and j != x and j != y:
                t = [i,j,x,y]
                t.sort()
                ans.append(tuple(t))
    return ans

def judge_color(K,N,i,j):
    black = 0
    white = 0
    K4 = gen_K4(N,i,j)
    for obj in K4:
        i,j,k,l = obj
        dat = K[i][j][k][l]
        if dat > 0 and dat != 10:
            black += 2 ** (dat-1)
            white -= 2 ** (dat-1)
        elif dat < 0:
            black -= 2 ** (-dat-1)
            white += 2 ** (-dat-1)
    return (black,white)

def paint_color(K,N,i,j,black,white):
    ans = 1 if black <= white else -1
    K4 = gen_K4(N,i,j)
    for obj in K4:
        i,j,k,l = obj
        dat = K[i][j][k][l]
        if dat == 0:
            K[i][j][k][l] = ans
        elif dat > 0 and dat != 10:
            K[i][j][k][l] = (dat + 1 if ans == 1 else 10)
        elif dat < 0:
            K[i][j][k][l] = (10 if ans == 1 else dat - 1)
    return ans

def count_K4(K,N):
    black = 0
    white = 0
    for i in range(N):
        for j in range(i+1,N):
            for k in range(j+1,N):
                for l in range(k+1,N):
                    if K[i][j][k][l] == 6:
                        black += 1
                    elif K[i][j][k][l] == -6:
                        white += 1
    return black,white

def work(N):
    t = time.time()
    K = np.zeros((N,N,N,N),dtype=np.int8)
    black_edge = 0
    white_edge = 0
    
    for i in range(N):
        for j in range(i+1,N):
            black,white = judge_color(K,N,i,j)
            color = paint_color(K,N,i,j,black,white)
            if color == 1:
                black_edge += 1
            else:
                white_edge += 1

    black_K4,white_K4 = count_K4(K,N)
    bound = N * (N-1) * (N-2) * (N-3) // 32
    
    print("N=",N)
    print("Edges: Black =",black_edge,", White =",white_edge)
    print("K4: Black =",black_K4,", White =",white_K4)
    print("Pure K4 =",black_K4 + white_K4,", Bound =",bound)
    print("Time:",time.time() - t,"s")
    print()

def main():
    dat = [4,5,10,15,20,25,50,75,100,125,150,175,200]
    for obj in dat:
        work(obj)

main()

