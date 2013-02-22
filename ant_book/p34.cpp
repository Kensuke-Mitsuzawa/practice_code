#include<cstdio>

using namespace std;

const int MAX_N = 50;
  int a[MAX_N];
  int n,k;
  printf ("input n\n");
  scanf("%d",&n);
  scanf("%d",&n);
  for (int ii=0;ii<n;ii++){
    printf("input element of list.Input %d elements\n",n-ii);
    scanf("%d",&a[ii]);
  }

//関数呼び出し時に与えられる数からiを増やしていって、n（設定された配列の要素数）に達したら、trueかfalseを判断して返す
bool dfs(int i,int sum,int n,int k,int a[MAX_N]) {
  
  //n個決め終わったら、今までの合計sumがkと等しいかを判断してtrue or falseを返す
  if (i == n) return sum == k;
  
  //配列を使わない場合（？）
  if (dfs(i+1,sum)) return true;

  //配列を使う場合
  if(dfs(i+1,sum+a[i])) return true;

  //配列を使う、使わないに関わらず、kが作れないので、falseを返す（引数が足りない場合？）
  return false;

}

void solve{

  
  if (dfs(0,0,n,k,a[MAX_N])) printf("yes\n");
  else printf("no\n");
}
