#include<assert.h>
#include <assert.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

char* shift_characters(char* text)
{
    size_t len = strlen(text);
    for (size_t i = 0; i < len; ++i) {
        if ('A' <= text[i] && text[i] <= 'E') {
            text[i] = text[i] + 21; // 'V' - 'A' = 21
        } else if ('F' <= text[i] && text[i] <= 'Z') {
            text[i] = text[i] - 5; // 'A' - 'F' = -5
        }
    }
    return text;
}

int main()
{
	char test1[] = "NS BFW, JAJSYX TK NRUTWYFSHJ FWJ YMJ WJXZQY TK YWNANFQ HFZXJX";
    char test2[] = "N BTZQI WFYMJW GJ KNWXY NS F QNYYQJ NGJWNFS ANQQFLJ YMFS XJHTSI NS WTRJ";
    char test3[] = "IFSLJW PSTBX KZQQ BJQQ YMFY HFJXFW NX RTWJ IFSLJWTZX YMFS MJ";

    assert(strcmp(shift_characters(test1), "IN WAR, EVENTS OF IMPORTANCE ARE THE RESULT OF TRIVIAL CAUSES") == 0);
    assert(strcmp(shift_characters(test2), "I WOULD RATHER BE FIRST IN A LITTLE IBERIAN VILLAGE THAN SECOND IN ROME") == 0);
    assert(strcmp(shift_characters(test3), "DANGER KNOWS FULL WELL THAT CAESAR IS MORE DANGEROUS THAN HE") == 0);
	return 0;
}