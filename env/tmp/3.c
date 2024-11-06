#include<assert.h>
#include <assert.h>
#include <stdio.h>

int hamming_distance(int x, int y)
{
    int distance = 0;
    int xor_result = x ^ y; 
    while (xor_result) {
        if (xor_result & 1) {
            distance++;
        }
        xor_result >>= 1;
    }
    return distance;
}

int main() {
    assert(hamming_distance(1, 2) == 2); // 01 and 10 have 2 different bits
    assert(hamming_distance(4, 7) == 2); // 100 and 111 have 2 different bits
    assert(hamming_distance(25, 30) == 3); // Additional test: 11001 and 11110 have 3 different bits
    assert(hamming_distance(0, 0) == 0); // Additional test: Same numbers have 0 different bits
    assert(hamming_distance(0xFFFFFFF, 0x0000000) == 28); // Additional test: Max unsigned int and 0 have 32 different bits
    return 0;
}