#include<stack>
#include<cstdio>

using namespace std;

int main() {
  stack<int> s; //int型をデータとするスタックを用意
  s.push(1); //{}が{1}に
  s.push(2); //{}が{1,2}に
  s.push(3); //{}が{1,2,3}に
  printf("%d\n",s.top()); //スタックの一番上の内容を表示
  
  s.pop();
  printf("%d\n",s.top());
  s.pop();
  printf("%d\n",s.top());
  s.pop();
  
  return 0;
}

  
  
