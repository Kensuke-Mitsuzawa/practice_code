#include<cstdio>

const int MAX_N = 50;

int main()
{
  int n,m,k[MAX_N];

  //from standard input
  printf ("input first n, next m\n");
  scanf("%d %d", &n,&m);
  for (int i=0;i<n;i++){
    printf ("input element of list.Input %d elements\n",n-i);
    scanf("%d",&k[i]);
  }

  //和がmになる組み合わせが見つかったかどうか？のフラグ
  bool f =false;

  for (int a =0;a<n;a++){
    for (int b=0;b<n;b++){
      for (int c=0;c<n;c++){
	for (int d=0;d<n;d++){
	  
	  if (k[a] + k[b] + k[c] + k[d] == m) {
	    f =true;
	  }
	}
      }
    }
  }
  if (f) puts("YES");
  else; puts("No");

  return 0;
}
