#include<assert.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>

int decode_numbers(const char* data_str)
{
    int a[] = {4, 1, 0, 0, 1, 0, 1, 0, 2, 1};
    int ans = 0;
    for(int i = 0; i < strlen(data_str); i++) {
        ans += a[data_str[i] - '0'];
    }
    return ans;
}

int main() {
    assert(decode_numbers("0000") == 4);
    assert(decode_numbers("8888") == 8);
    assert(decode_numbers("1234") == 1);
    assert(decode_numbers("5678") == 3);
    assert(decode_numbers("9012") == 2);
    assert(decode_numbers("1357") == 0);
    assert(decode_numbers("2468") == 4);

    // Additional test samples
    assert(decode_numbers("9999") == 4);
    assert(decode_numbers("1111") == 0);
    assert(decode_numbers("2222") == 0);
    assert(decode_numbers("3333") == 0);
    assert(decode_numbers("4444") == 4);
    assert(decode_numbers("5555") == 0);
    assert(decode_numbers("6666") == 4);
    assert(decode_numbers("7777") == 0);
    assert(decode_numbers("0001") == 3);
    assert(decode_numbers("2301") == 1);

    return 0;
}