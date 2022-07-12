import queue


f = open('temp.txt','r')
map=[]
for line in open('temp.txt'):
    line = f.readline()
    map.append(line)


#print(map)
row=len(map)

for i in range(0,row):
    map[i]=list(map[i])
    map[i].pop(len(map[i])-1)

col=len(map[1])
#print(row,col)
col-=1

def my_print_2(map):
    for i in range(0,len(map)):
        for j in range(0,len(map[i])):
            if map[i][j]=='*':
                print("\033[1;33m"+'0'+"\033[0m",end='')
            else:
                print(map[i][j],end='')
        print()


next=[[0,1],[-1,0],[0,-1],[1,0]]#上下左右
ans=[]

#判断能不能走
def can_walk(a,b,map):
    if a>=0 and a<len(map) and b>=0 and b<len(map[0]) and (map[a][b]=='0' or map[a][b]=='E'):
        return True
    else:
        return False

#深度受限搜索
def limit_dfs(sx,sy,map,book,lim,curr_lim):
    if curr_lim>lim:#curr_lim为当前深度，lim为限制深度，但超过限制时返回False
        return False
    if(map[sx][sy]=='E'):
        return True
    for i in range(len(next)):
        if can_walk(sx+next[i][0],sy+next[i][1],map) and book[sx+next[i][0]][sy+next[i][1]]==0 :
            book[sx+next[i][0]][sy+next[i][1]]=1     
            if limit_dfs(sx+next[i][0],sy+next[i][1],map,book,lim,curr_lim+1)==True:
                ans.append([sx,sy])
                return True
    return False



#迭代加深搜索
def iteration_dfs(startx,starty,map):
    global ans
    dep=0   #dep为每次深搜的最大限制深度
    while 1:    #迭代加深直至得到答案
        ans=[]
        book=[]
        for k1 in range(0,row):
            book.append([])
            for k2 in range(0,col):
                book[k1].append(0)
    #print(startx,starty)
        tmp=limit_dfs(startx,starty, map,book,dep,0)
        if tmp==True:
            break
        else:
            dep+=1      
        #理论上，搜索的深度在数值上不超过面积，所以单深度超过面积时说明没有答案
        if dep>col*row:
            return -1
    return dep

    


startx=0
starty=0

for k1 in range(0,row):
    for k2 in range(0,col):
        if map[k1][k2]=='S':
            startx=k1
            starty=k2
            break
#print(book)
#print(startx,starty)
dep=iteration_dfs(startx,starty,map)
if dep==-1:
    print('No answer!')
    exit(0)


for i in range(len(ans)):
    if map[ans[i][0]][ans[i][1]]!='S' or map[ans[i][0]][ans[i][1]]!='E':
        map[ans[i][0]][ans[i][1]]='*'
map[startx][starty]='S'
print('最后限制深度为：',dep)
my_print_2(map)