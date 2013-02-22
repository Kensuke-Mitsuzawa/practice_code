#include<iostream>

using namespace std;

int main(){
  int i;
  float f;
  char s[80];

  cout << "enter an integer,float,and string";

  cin >> i >> f >> s;
  
  cout << "here are your data:";

  // char型のstring s[80]への代入も cin << s で終了。これは便利
  cout << i << ' ' << f << ' ' << s << '\n';
  
  return 0;
}
