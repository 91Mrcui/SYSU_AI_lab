
#地图类
class roman_map():
    def __init__(self):#初始化
        self.book={}    #城市名字到编号的映射
        self.book2={}   #编号到城市名字的映射
        self.book3={}   #城市名与缩写的映射
        self.index=0
        self.m=20      #城市的数量
        self.n=23      #城市间道路的数量
        self.grp=[]     #用邻接矩阵存图
        for s1 in range(0,self.m):
            self.grp.append([])
            for s2 in range(0,self.m):
                if(s1==s2):
                    self.grp[s1].append(0)
                else:
                    self.grp[s1].append(float("inf"))#将边初始化为最大值


    def read_message(self,file_name):#读取文件信息以建立图
        file_object=open(file_name)
        i=0

        for line in file_object.readlines():
            if i!=0:
                v1,v2,w=line.split()
                w=int(w)
                v1=v1.lower()
                v2=v2.lower()


                self.book3[v1[0]]=v1
                self.book3[v2[0]]=v2

                if v1 in self.book.keys():  #输入时采用字典将城市名字转变为数字表示顶点编号
                    v1=self.book[v1]
       
                else:
                    self.book[v1]=self.index
                    self.book2[self.index]=v1
                    v1=self.index
                    self.index+=1

                if v2 in self.book.keys():
                    v2=self.book[v2]
                else:
                    self.book[v2]=self.index
                    self.book2[self.index]=v2
                    v2=self.index
                    self.index+=1

                self.grp[v1][v2]=w
                self.grp[v2][v1]=w
        #-------------------
            else:
                i+=1
        file_object.close()




