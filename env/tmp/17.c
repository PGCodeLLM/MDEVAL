#include<assert.h>
#include <assert.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

int find_longest_consecutive_ones_length(unsigned long long n)
{
    int max = 0;
    int ans = 0;
    while(n){
        if(n & 1)
            ans++;
        else{
            if(ans > max)
                max = ans;
            ans = 0;
        }
        n >>= 1;
    }
    if(ans > max)
        max = ans;
    return max;
}

int main()
{
    assert(find_longest_consecutive_ones_length(7) == 3);
    assert(find_longest_consecutive_ones_length(13) == 2);
    assert(find_longest_consecutive_ones_length(12345) == 3); // New test sample
    assert(find_longest_consecutive_ones_length(0b11011101111) == 4); // New test sample using binary literal for clarity
    assert(find_longest_consecutive_ones_length(0xFFFFFFFF) == 32); // New test sample: all ones for a 32-bit number
    assert(find_longest_consecutive_ones_length(0) == 0); // New test sample: no ones in a zero

    // printf("All tests passed!\n");
    return 0;
}