#include<iostream>
#include<string>  
#include<cmath> 
#include<algorithm>
#include<vector>
#include<map>
#include<time.h> 
using namespace std;
 
int moves[4][2]={{-1,0},{0,-1},{0,1},{1,0}};//�ƶ����飬��������
vector<int> ans; //����ƶ����� 
int goal[16][2]= {{3,3},{0,0},{0,1},{0,2},{0,3},{1,0},{1,1},{1,2},{1,3},{2,0},{2,1},{2,2},{2,3},{3,0},{3,1},{3,2}};
int maze[4][4];
int maze2[16];
int bound;//������ֵ  
int flag,lens;				  

int h_manhadun(int a[4][4])//��������h1(x)ȡ15���������Ŀ��λ�õ������پ���
{
    int cost=0;
    for(int i=0;i<4;i++)
    {
        for(int j=0;j<4;j++)  
        {
            int w=maze[i][j];
            if(w!=0) 
			cost+=abs(i-goal[w][0])+abs(j-goal[w][1]);
        }
    }
    return cost;
}


//��������h2(x) 
/*int h_manhadun(int a[4][4])//
{
    int cost=0;
    for(int i=0;i<4;i++)
    {
        for(int j=0;j<4;j++)  
        {
            if(a[i][j]!=i*4+j+1&&a[i][j]!=0)
            cost+=1;
        }
    }
    return cost;
}
 */

//��������h3(x) 
/*int h_manhadun(int a[4][4])//
{
    int cost=0;
    int cot=0;
    for(int i=0;i<4;i++)
    {
        for(int j=0;j<4;j++)  
        {
            int w=maze[i][j];
            if(w!=0) 
			cost+=abs(i-goal[w][0])+abs(j-goal[w][1]);
            if(a[i][j]!=i*4+j+1&&a[i][j]!=0)
            cot+=1;
        }
    }
    return 0.5*cost+0.5*cot;
}
*/

int h_new(int a[4][4]);//��������h2(x) 
 
void dfs(int x,int y,int len,int pre_move)
{
    if(flag) return;
    int dist=h_manhadun(maze);
    if(len==bound)
    {
        if(dist==0)  //�ɹ� �˳�
        {
            flag=1;
            lens=len;
            return;
        }
        else {
        	if(!ans.empty())
            ans.pop_back();
			return;
		}  //����Ԥ�賤�� ����
    }
    for(int i=0;i<4;i++)  
    {
        if(i+pre_move==3&&len>0) 
		continue;//���ƶ���ȥ 
        int tx=x+ moves[i][0];
        int ty=y+ moves[i][1];
        if(tx>=0&&tx<4&&ty>=0&&ty<4)
        {	
			swap(maze[x][y],maze[tx][ty]);

            ans.push_back(maze[x][y]);

            int p=h_manhadun(maze);
            if(p+len<=bound&&flag==0)
            {
                dfs(tx,ty,len+1,i);
                if(flag) return;

            }
            swap(maze[x][y],maze[tx][ty]);
            if(!ans.empty())
            ans.pop_back();
        }
    }
}
 
int main()  
{	
	//���Դ��� 
    int test=1;
    //string the_last="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0,";
    //string the_start;
    clock_t t_start,end;
    while(test--)       
    {
		int x1,y1;
        for(int i=0;i<16;i++)
        {
            cin>>maze2[i];
            if(maze2[i]==0)
            {
                x1=i/4;
				y1=i%4;
				maze[x1][y1]=0;
            }
            else
            {
                maze[i/4][i%4]=maze2[i];
            }
        }                                      
 		//���ñ߽� 
        bound=h_manhadun(maze);
        flag=0;
        lens=0;
		t_start = clock();
        while(flag==0&&lens<=90)//�������Ϊ90 
        {
        	ans.clear();
            dfs(x1,y1,0,0);
            if(flag==0) 
			bound++; //��ֵ���� 
        	//cout<<ans.size()<<endl;
		}
        if(flag){
		cout<<"steps:"<<lens<<endl;
		end=clock();
		cout<<"using time:";
		printf("%f",end-t_start);
		cout<<"ms"<<endl;
		}
		cout<<"swap orders:"<<endl;		
		for(int i=ans.size()-1;i>=0;i--){
			if(i!=0)
			cout<<ans[i]<<"-";
			else
			cout<<ans[i]<<endl;
		}

    }
    return 0;
}
