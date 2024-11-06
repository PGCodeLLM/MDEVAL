#include<assert.h>
#include <assert.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

int process_request(int n)
{
    int a[10010];
    a[0] = 1;
    a[1] = 1;
    // find the factorial
    for(int i = 2; i <= 10000; i++) {
        a[i] = (a[i-1] * i) % 10007;
    }
    return a[n];
}

int main()
{
    assert(process_request(0) == 1); // Added test for boundary condition
    assert(process_request(1) == 1);
    assert(process_request(2) == 2);
    assert(process_request(3) == 6);
    assert(process_request(4) == 24);
    assert(process_request(10) == 6266); // 10! % 10007 = 3628800 % 10007 = 362
    assert(process_request(10000) == 6991); // Added a test for upper boundary condition
    // printf("All tests passed.\n");
    return 0;
}