#include<iostream>
#include<cstdio>

using namespace std;

const int MAX_N = 50;

void solve(){

  int n,a[MAX_N];
  printf ("input n\n");
  scanf("%d",&n);
  for (int ii=0;ii<n;ii++){
    printf("input element of list.Input %d elements\n",n-ii);
    scanf("%d",&a[ii]);
  }
  
  int ans = 0;
  
  for (int i=0;i<n;i++){
    for(int j=0;j<n;j++){
      for(int k=0;k<n;k++){
	
	int len = a[i] + a[j] + a[k];
	int ma = max(a[i],max(a[j],a[k]));
	
	int rest = len - ma;
	
	if(ma<rest) {
	  ans = max(ans,len);
	}
      }
    }
  }
  printf ("the answer is %d\n",ans);
}

int main(){
  solve();
}

