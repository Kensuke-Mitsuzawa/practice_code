#include<queue>
#include<cstdio>

using namespace std;

int main(){
  queue<int> que; //これでint型のキュー構造を用意している
  que.push(1); //{}から{1}に
  que.push(2); //{1}から{1,2}に
  que.push(3);
  
  printf("%d\n",que.front());
  
  que.pop();
  printf("%d\n",que.front());
  que.pop();
  printf("%d\n",que.front());
  que.pop();
  printf("%d\n",que.front());
  
  return 0;
}

  
