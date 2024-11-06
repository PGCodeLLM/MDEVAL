#include<assert.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>

int minRoundsToSameChar(const char* s)
{
    int charCount[26] = {0};
    while (*s) {
        charCount[*s - 'a']++;
        s++;
    }
    int maxCount = 0;
    for (int i = 0; i < 26; i++) {
        if (charCount[i] > maxCount) {
            maxCount = charCount[i];
        }
    }
    return strlen(s) - maxCount;
}

int main() {
    assert(minRoundsToSameChar("aab") == 1);
    assert(minRoundsToSameChar("abc") == 2);
    assert(minRoundsToSameChar("aaa") == 0);
    assert(minRoundsToSameChar("abab") == 1);
    assert(minRoundsToSameChar("zzzzz") == 0);
    return 0;
}