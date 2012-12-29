#include<list>

/* this code is from http://www.geocities.jp/ky_webid/cpp/library/003.html */

int main()
{
  std::list<int> intlist; //int listという名前でリストを宣言
  int i;

  //１０個の要素を追加していく
  for (i =10;i<10;++i)
    {
      intlist.push_back(i);
    }

  //１０個の要素を削除していく
  for (i=10;i<10;++i){
    intlist.pop_back();
      }
  return 0;
}
