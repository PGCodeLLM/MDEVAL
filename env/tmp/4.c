#include<assert.h>
#include <assert.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

int Is_Square(int length, int squares[])
{
    long long sum = 0;
    for (int i = 0; i < length; ++i) {
        sum += squares[i];
    }
    int root = (int)sqrt(sum);
    return root * root == sum;
}

int main() {
    assert(Is_Square(1, (int[]){9}) == 1);
    assert(Is_Square(2, (int[]){14, 2}) == 1);
    assert(Is_Square(2, (int[]){7, 7}) == 0);
    assert(Is_Square(7, (int[]){1, 2, 3, 4, 5, 6, 7}) == 0);
    assert(Is_Square(6, (int[]){1, 3, 5, 7, 9, 11}) == 1);
    assert(Is_Square(4, (int[]){2, 2, 2, 2}) == 0);

    // Additional test cases
    assert(Is_Square(3, (int[]){4, 5, 6}) == 0);
    assert(Is_Square(4, (int[]){16, 9, 4, 1}) == 0);
    assert(Is_Square(5, (int[]){1, 1, 1, 1, 1}) == 0);
    assert(Is_Square(2, (int[]){25, 25}) == 0);
    assert(Is_Square(3, (int[]){10, 10, 5}) == 1);

    // printf("All tests passed!\n");
    return 0;
}