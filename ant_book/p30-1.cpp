#include <iostream>
#include <cstdio>

using namespace std;

int fact(int n) {
  if (n == 0) return 1;
  return n * fact(n-1);
}


int main() {
  int a;
  a = 10;
  printf ("%d\n",fact(a));

}
 
