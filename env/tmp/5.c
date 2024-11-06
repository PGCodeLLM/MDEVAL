#include<assert.h>
#include <assert.h>
#include <stdio.h>

void find_max_min(int a, int b, int c, int *max, int *min)
{
    if (a > b) {
        if (a > c) {
            *max = a;
            *min = (b < c) ? b : c;
        } else {
            *max = c;
            *min = b;
        }
    } else {
        if (b > c) {
            *max = b;
            *min = (a < c) ? a : c;
        } else {
            *max = c;
            *min = a;
        }
    }
}

int main() {
    int max, min;

    find_max_min(1, 2, 3, &max, &min);
    assert(max == 3 && min == 1);

    // Additional tests
    find_max_min(5, 3, 4, &max, &min);
    assert(max == 5 && min == 3);

    find_max_min(10, -2, 7, &max, &min);
    assert(max == 10 && min == -2);

    find_max_min(-1, -3, -2, &max, &min);
    assert(max == -1 && min == -3);

    return 0;
}