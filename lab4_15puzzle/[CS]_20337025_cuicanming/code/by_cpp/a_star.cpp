#include<iostream>
#include<cmath>
#include<vector>
#include<queue>
#include<map>
#include<unordered_map>
#include<time.h> 
using namespace std;

int goal[16]={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0};
extern int id=0;
unordered_map<int,int> close;

int h_manhadun(int *maze)//启发函数h1(x)取15个数码距离目标位置的曼哈顿距离
{
    int cost=0;
    int x,gx;
	int y,gy;
    for(int i=0;i<16;i++){
    	if(maze[i]!=0){
    		int w=maze[i];
    		x=i/4;
    		y=i%4;
    		
    		gx=(w-1)/4;
    		gy=(w-1)%4;
    		cost=cost+abs(gx-x)+abs(gy-y);
    		
		}
	}
    return cost;
}

int h_2(int *maze)//启发函数h2(x)取错牌数 
{
    int cost=0;
    int x,gx;
	int y,gy;
    for(int i=0;i<16;i++){
    	if((maze[i]!=0)&&(maze[i]!=i/4+i%4+1)){
		cost+=1;
		}
	}
    return cost;
}

struct state{
	int a[16];
	int f;
	int g;
	int sid;
	
	bool operator ==(const state& n2) const{
	for(int i=0;i<16;i++){
		if(this->a[i]!=n2.a[i])
			return false;
	}
	return true;
	}
	
	bool operator <(const state& other)const{
		return this->f > other.f;
	}

	state(int t[4][4],int &last_g){
		sid=id++;
		int index=0;
		for(int i=0;i<4;i++)
		for(int j=0;j<4;j++)
		this->a[index++]=t[i][j];
		
		this->g=last_g+1;
		this->f=this->g+h_manhadun(this->a);
	}
	
	state(int t[16],int last_g){
		sid=id++;
		int index=0;
		for(index=0;index<16;index++)
		this->a[index]=t[index];
		
		this->g=last_g+1;
		this->f=this->g+h_manhadun(this->a);
	}
};




void p_in_16(state& show){
	int index=0;
	for(int i=0;i<4;i++){
		for(int j=0;j<4;j++){
			printf("%2d ",show.a[index++]);
		}
		cout<<endl;
	}
	cout<<"-------------------"<<endl;
}

bool is_goal(state &tmp){
	for(int i=0;i<16;i++){
		if(tmp.a[i]!=goal[i])
		return false;
	}
	return true;
} 



vector<state> neibour(state &now){
	int temp[4][4];
	int index=0;
	int zx,zy;
	for(int i=0;i<4;i++){
		for(int j=0;j<4;j++){
			temp[i][j]=now.a[index++];
			if(temp[i][j]==0){
				zx=i;
				zy=j;
			}
		}
	}
	
	int moves[4][2]={{1,0},{-1,0},{0,1},{0,-1}};
	
	vector<state> next_state;

	
	int nx,ny;
	
	for(int i=0;i<4;i++){
		nx=zx+moves[i][0];
		ny=zy+moves[i][1];
		if(nx>-1&&nx<4&&ny>-1&&ny<4){
			temp[zx][zy]=temp[nx][ny];
			temp[nx][ny]=0;
			
			state new_state(temp,now.g);
			next_state.push_back(new_state);
			
			temp[nx][ny]=temp[zx][zy];
			temp[zx][zy]=0;
		}
	}
	
	return next_state;
}


int main(){
	priority_queue<state> frontier; 

	//int sta[16]={1,2,4,8,5,7,11,10,13,15,0,3,14,6,9,12};
	int sta[16]={5,1,3,4,2,7,8,12,9,6,11,15,0,13,10,14};
	//int sta[16]={14,10,6,0,4,9,1,8,2,3,5,11,12,13,7,15};
	//int sta[16]={6,10,3,15,14,8,7,11,5,1,0,2,13,12,9,4};
	state start(sta,0);
	
	frontier.push(start);//优先队列 
	close[start.sid]=start.f;//close表 

	clock_t t_start,end;
	t_start=clock();//计时 
	while(!frontier.empty()){
		state current = frontier.top();
		//取f值最小的 
		if(current.g>40)
			break;
		cout<<current.f<<endl;
		if(is_goal(current)){
			//cout<<"find!"<<endl;
			cout<<"steps:"<<current.g-1<<endl;
			break;//找到了便进行输出 
		}
		frontier.pop();
		vector<state> next_states=neibour(current);//找到邻接的状态 

		for(int i=0;i<next_states.size();i++){

			if(close.find(next_states[i].sid) == close.end() || close[next_states[i].sid]>next_states[i].f ){
				close[next_states[i].sid]=next_states[i].f;//如果没出现过或者f值更小 ，入队 
				frontier.push(next_states[i]);
			} 
		} 

		
	}
	end=clock();
	cout<<"using time:"<<end-t_start<<"ms"<<endl;
	
	return 0;
}
