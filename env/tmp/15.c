#include<assert.h>
#include <assert.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

unsigned long long count_valid_coin_toss_sequences(int n)
{
    unsigned long long a[41][2];
    a[1][0] = 1;
    a[1][1] = 1;
    
    for(int i = 2; i <= n; i++){
        a[i][0] = a[i - 1][1] + a[i - 1][0];
        a[i][1] = a[i - 1][0];
    }
    
    return a[n][0] + a[n][1];
}

int main() {
    assert(count_valid_coin_toss_sequences(1) == 2);
    assert(count_valid_coin_toss_sequences(2) == 3);
    assert(count_valid_coin_toss_sequences(3) == 5);
    assert(count_valid_coin_toss_sequences(4) == 8); // Additional test
    assert(count_valid_coin_toss_sequences(5) == 13); // Additional test
    // Feel free to add more tests here
    assert(count_valid_coin_toss_sequences(40) == 267914296); // Additional test
    assert(count_valid_coin_toss_sequences(39) == 165580141); 
    assert(count_valid_coin_toss_sequences(38) == 102334155);
    // printf("All tests passed!\n");
    return 0;
}