#include<assert.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

bool isPalindrome(const char* str);

bool isPalindrome(const char* str)
{
    int start = 0;
    int end = strlen(str) - 1;
    
    while (start < end) {
        while (!isalnum(str[start]) && start < end) start++;
        while (!isalnum(str[end]) && start < end) end--;
        if (tolower(str[start]) != tolower(str[end]))
            return false;
        start++;
        end--;
    }
    return true;
}

int main()
{
    assert(isPalindrome("A man a plan a canal Panama") == true);
    assert(isPalindrome("No lemon, no melon") == true);
    assert(isPalindrome("Was it a car or a cat I saw") == true);
    assert(isPalindrome("Madam, in Eden, I'm Adam") == true);
    assert(isPalindrome("Never odd or even") == true);
    assert(isPalindrome("Eva, can I see bees in a cave") == true);
    assert(isPalindrome("hello") == false);
    assert(isPalindrome("GitHub") == false);
    assert(isPalindrome("programming") == false);
    
    return 0;
}