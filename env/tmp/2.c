#include<assert.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>

char* create_id(const char* word1, const char* word2)
{
    int length1 = strlen(word1);
    int length2 = strlen(word2);
    int total_length = length1 + length2;
    char* id = malloc(sizeof(char) * (total_length + 1));
    assert(id != NULL);

    for (int i = 0, j = 0, k = length2 - 1; i < total_length; ++i) {
        if (i % 2 == 1) {
            id[i] = word2[k--]; // Take character from word2 in reverse
        } else {
            id[i] = word1[j++];
        }
    }
    
    id[total_length] = '\0';
    return id;
}

int main() {
    char* id; // To hold the results from create_id

    id = create_id("fish", "cat");
    assert(strcmp(id, "ftiasch") == 0);
    free(id);

    id = create_id("icpc", "acm");
    assert(strcmp(id, "imccpac") == 0);
    free(id);

    id = create_id("oo", "w");
    assert(strcmp(id, "owo") == 0);
    free(id);

    // Add more test samples
    id = create_id("hello", "world");
    assert(strcmp(id, "hdellrloow") == 0);
    free(id);

    id = create_id("abc", "def");
    assert(strcmp(id, "afbecd") == 0);
    free(id);

    id = create_id("buaanb", "nbbuaa");
    assert(strcmp(id, "bauaauabnbbn") == 0);
    free(id);

    id = create_id("xtuisgood", "ilovextu");
    assert(strcmp(id, "xuttuxiesvgooloid") == 0);
    free(id);

    return 0;
}