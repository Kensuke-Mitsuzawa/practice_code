#include <iostream>
#include <cstdio>

using namespace std;

const int MAX_N = 50;

int fib(int n) {

  int memo[MAX_N + 1];

  if  (n <= 1) return n;
  if (memo[n] != 0) return memo[n];
  
  return memo[n] = fib(n-1) + fib(n-2);

}



int main() {
  int n;
  
  printf ("input n\n");
  scanf ("%d",&n);
  
  int result = fib(n);
  printf ("%d\n",result);
}

  
