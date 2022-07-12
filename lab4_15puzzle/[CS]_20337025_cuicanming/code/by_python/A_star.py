from queue import PriorityQueue

import time

from numpy import append

def print_in_16(g):
    print('------------------------')
    count=0
    for i in g[1:17]:
        print("%2d"%int(i),end=' ')
        count+=1
        if count%4==0:
            print()
    print('-------------------------')

def cmp_two(a,b):
    for i in range(1,17):
        if a[i]!=goat[i]:
            return False
    return True

def cmp(a):#对比是否相等
    for i in range(1,17):
        if int(a[i])!=goat[i]:
            return False
    return True

def sch_in_open2(open2,b):
    for i in range(len(open2)):
        if cmp_two(open2[i],b):
            return i
    return -1

def m_to_tuple(m,deep):#地图转元组1
    tlist=[0]
    for i in range(4):
        for j in range(4):
            tlist.append(m[i][j])

    tlist[0]=madun_dis(tlist)+deep
    
    t=tuple(tlist)

   
    return t

def move(a,direction,deep):#1上2下3左4右
    mp=[[],[],[],[]]
    for i in range(1,17):
        mp[int((i-1)/4)].append(a[i])
    x=-1
    y=-1
    for i in range(4):
        for j in range(4):
          if mp[i][j]=='0':
              x=i
              y=j
  
    if direction==1 and x-1>=0:
        mp[x][y]=mp[x-1][y]
        mp[x-1][y]='0'
        return m_to_tuple(mp,deep)
    elif direction==2 and x+1<4:
        mp[x][y]=mp[x+1][y]
        mp[x+1][y]='0'
        return m_to_tuple(mp,deep)
    elif direction==3 and y-1>=0:
        mp[x][y]=mp[x][y-1]
        mp[x][y-1]='0'
        return m_to_tuple(mp,deep)
    elif direction==4 and y+1<4:
        mp[x][y]=mp[x][y+1]
        mp[x][y+1]='0'
        return m_to_tuple(mp,deep)

    return ()


def madun_dis(a):#计算曼哈顿距离总和，a为元组
    total=0
    for i in range(1,17):
        gx=int((int(a[i])-1)/4)
        gy=int(int(a[i])-1)%4
        if a[i]=='0':
            gx=3
            gy=3
        x=int((i-1)/4)
        y=(i-1)%4
        #print(int(abs(gx-x))+int(abs(gy-y)))
        total+=int(abs(gx-x))+int(abs(gy-y))
    return total

def A_star(start):
    close=[]
    historylist=[]
    path=[]
    open=PriorityQueue()
    open2=[]
    open.put(start)
    open2.append(start)

    historylist.append(start[1:17])
    path.append(-3)

    tree_deep=0
    ans=[]
    while open!=[]:
        curr_state=open.get()
        open2.remove(curr_state)
        #print("choose:")
        #print_in_16(curr_state)
        close.append(curr_state[1:17])
        #print(curr_state[0]-madun_dis(curr_state))
        #print(curr_state)

        if cmp(curr_state):
            print('find!\nsteps=',curr_state[0]-madun_dis(curr_state))
            idx=historylist.index(curr_state[1:17])
            ni=0
            while ni!=-3:
                ans.append(historylist[idx])
                ni=path[idx]
                idx=ni

            
            break#找到了

        
        for i in range(1,5):
            tree_deep=curr_state[0]-madun_dis(curr_state)+1
            after_move=move(curr_state,i,tree_deep)
            if after_move==():
                continue
            

            index=sch_in_open2(open2,after_move)
            if index!=-1:
                if after_move[0]<open2[index][0]:
                    open2[index][0]=after_move[0]


            elif (after_move[1:17] not in historylist) and(after_move[1:17] not in close):
                open.put(after_move)
                open2.append(after_move)
                historylist.append(after_move[1:17])
                path.append(historylist.index(curr_state[1:17]))
               # print_in_16(after_move)

        #if curr_state=tar:
    ans.reverse()
    
    
    for i in ans:
        print('------------------------')
        count=0
    
        for j in range(16):
            print("%2d"%int(i[j]),end=' ')
            count+=1
            if count%4==0:
                print()
        print('-------------------------')

    print(len(ans))
    
#输入初始状态

temp=['0']
for i in range(4):
    a=input()
    t=a.split(" ")
    for j in t:
        temp.append(j)


temp[0]=madun_dis(tuple(temp))
#print(temp)
g0=tuple(temp)
#g0.print()

print(g0)

goat=(-1,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0)



tim=time.time()
A_star(g0)
tim2=time.time()
print(tim2-tim)
#print_in_16(goat)
#print(madun_dis(goat))