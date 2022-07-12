

Maxnum=float("inf") #定义一个最大值


#dijktra算法执行过程
def dj(a,sta,end):
    num=a.m
    dis=[Maxnum]*num    
    dis[sta]=0         #dis[]存储距离
    qianzui=[-1]*num  #为输出路径，记录前缀
    vis=[0]*num
    u=0
    for i in range(num):
        min=Maxnum
        for j in range(num):
            if not vis[j] and dis[j]<min:
                min=dis[j]
                u=j
        #u为可到达的顶点中距离最小的
        vis[u]=True
        for k in range(num):
            if a.grp[u][k]<Maxnum:
                if dis[u]+a.grp[u][k]<dis[k]:
                    dis[k]=dis[u]+a.grp[u][k]
                    qianzui[k]=u    #记录前驱以输出路径
    #输出最短路程
    print(dis[end])    
    #输出路径信息
    l=end
    lujin=a.book2[sta].title()+"-->"
    ans=[]
    city=0
    while l !=sta:
        ans.append(a.book2[l])
        city+=1
        l=qianzui[l]
    for i in range(city-1,-1,-1):
        lujin+=ans[i].title()
        if i!=0:
            lujin+='-->'
    print(lujin)
    #将输出信息输入记录文件中
    filename = 'record.txt'
    with open(filename, 'a') as file_object2:
        file_object2.write(lujin+":")
        file_object2.write(str(dis[end])+"\n")
    return dis[end],lujin