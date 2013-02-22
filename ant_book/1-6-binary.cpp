#include<iostream>
#include<cstdio>

using namespace std;

const int MAX_N = 50;

int n,m,k[MAX_N];

bool binary_search(int x){
  int l = 0,r = n;
  

  while (r-1 >= 1) {
    int i = (l+r) / 2;
    if (k[i] == x) return true; //見つかった
    else if (k[i] < x) l = i + 1;
    else r = i;
  }

  return false;
}

void solve(){

  printf ("input n\n");
  scanf("%d",&n);
  printf ("input m\n");
  scanf("%d",&m);
  for (int i=0;i<n;i++){
    printf("input element of list.Input %d elements\n",n-i);
    scanf("%d",&k[i]);
  }

  sort (k, k+n);

  bool f = false;

  for (int a =0; a<n; a++) {
    for (int b =0;b<n;b++) {
      for (int c=0;c<n;c++){
	if (binary_search(m-k[a]-k[b]-k[c])) {
	  f = true;
	}
      }
    }
  }
  if (f) puts ("Yes");
  else puts("No");

}

int main() {
  solve();
}



