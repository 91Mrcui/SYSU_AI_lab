

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


book=[]
next=[[0,1],[-1,0],[0,-1],[1,0]]#上下左右
ans=[]

#判断能不能走
def can_walk(a,b,map):
    if a>=0 and a<len(map) and b>=0 and b<len(map[0]) and (map[a][b]=='0' or map[a][b]=='E'):
        return True
    else:
        return False
#用深搜的方法
def dfs(sx,sy,map,book):
    if(map[sx][sy]=='E'):
        return True
    for i in range(len(next)):
        if can_walk(sx+next[i][0],sy+next[i][1],map) and book[sx+next[i][0]][sy+next[i][1]]==0 :
            book[sx+next[i][0]][sy+next[i][1]]=1     
            if dfs(sx+next[i][0],sy+next[i][1],map,book)==True:
                ans.append([sx,sy])
                return True
    return False

startx=0
starty=0
for i in range(0,row):
    book.append([])
    for j in range(0,col):
        book[i].append(0)
        if map[i][j]=='S':
            startx=i
            starty=j
#print(book)
#print(startx,starty)
dfs(startx,starty,map,book)
for i in range(len(ans)):
    if map[ans[i][0]][ans[i][1]]!='S' or map[ans[i][0]][ans[i][1]]!='E':
        map[ans[i][0]][ans[i][1]]='*'
map[startx][starty]='S'
print('路径长度为：',len(ans))
my_print_2(map)
print('------------------')
#my_print(map)