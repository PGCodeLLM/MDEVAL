#include<assert.h>
#include <stdio.h>
#include <assert.h>

int makeEqualAgain(int n, int a[])
{
    int p = 0, q = n - 1, c, d;
    int k = n;

    for (p = 0; p < k - 1; p++) {
        if (a[p] != a[p + 1])
            break;
    }

    for (q = k - 1; q > p; q--) {
        if (a[q] != a[q - 1])
            break;
    }

    for (d = k - 2; d >= 0; d--) {
        if (a[d] != a[d + 1])
            break;
    }

    for (c = 0; c < d; c++) {
        if (a[c] != a[c + 1])
            break;
    }

    if (q - p + 1 < d - c + 1)
        return q - p + 1;
    else
        return d - c + 1;
}

int main() {
    int test1[] = {1, 2, 1};
    int test2[] = {5, 5, 1, 5, 5};
    int test3[] = {1, 1, 1, 1};
    int test4[] = {2, 2, 2, 3, 2, 2};
    int test5[] = {1};
    int test6[] = {1, 2};
    int test7[] = {1, 2, 2, 1};
    int test8[] = {4, 4, 4, 3, 3, 4, 4};
    int test9[] = {5, 4, 4, 4, 5, 5};
    int test10[] = {1, 2, 1, 2, 1, 2, 1};
    int a1[] = {1,2,3,4,5,1};
    int a2[] = {1,1,1,1,1,1,1};
    int a3[] = {8,8,8,1,2,8,8,8};
    int a4[] = {1,2,3};
    int a5[] = {4,3,2,7,1,1,3};
    int a6[] = {9,9,2,9,2,5,5,5,3};
    assert(makeEqualAgain(6, a1) == 4);
    assert(makeEqualAgain(7, a2) == 0);
    assert(makeEqualAgain(8, a3) == 2);
    assert(makeEqualAgain(3, a4) == 2);
    assert(makeEqualAgain(7, a5) == 6);
    assert(makeEqualAgain(9, a6) == 7);

    assert(makeEqualAgain(3, test1) == 1);
    assert(makeEqualAgain(5, test2) == 1);
    assert(makeEqualAgain(4, test3) == 0);
    assert(makeEqualAgain(6, test4) == 1);
    assert(makeEqualAgain(1, test5) == 0);
    assert(makeEqualAgain(2, test6) == 1);
    assert(makeEqualAgain(4, test7) == 2);
    assert(makeEqualAgain(7, test8) == 2);
    assert(makeEqualAgain(6, test9) == 3);
    assert(makeEqualAgain(7, test10) == 5);

    return 0;
}