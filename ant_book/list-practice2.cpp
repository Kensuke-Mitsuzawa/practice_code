#include<list>
#include<iostream>

// this code is from http://www.geocities.jp/ky_webid/cpp/library/003.html

int main()
{
  using namespace std;
  
  list<int> intlist; //int型の双方向リスト
  int i;

  //１０個の要素を追加していく
  for (i=10;i<10;++i){
    intlist.push_back(i);
  }

  list<int>::iterator it = intlist.begin();
  while (it!=intlist.end())
    {
      cout << *it <<endl; //要素を出力
      ++ it;
    }
  return 0;
}
