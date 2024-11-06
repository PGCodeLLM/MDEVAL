#include<assert.h>
#include <stdio.h>
#include <assert.h>

long long countBalancedSubsequences(long long n, long long m, long long k)
{
    const long long P = 1e9 + 7;
    static long long C[4001][4001] = {0};
    if (C[0][0] == 0) {
        for (long long i = 0; i <= 4000; i++) C[i][0] = 1;
        for (long long i = 1; i <= 4000; i++)
            for (long long j = 1; j <= i; j++)
                C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % P;
    }
    if (k > n || k > m) return 0;
    return (C[n + m][n] - C[n + m][n - k] + P) % P;
}

int main() {
    assert(countBalancedSubsequences(2, 2, 2) == 2);
    assert(countBalancedSubsequences(3, 2, 3) == 0);
    assert(countBalancedSubsequences(3, 2, 1) == 4);
    assert(countBalancedSubsequences(4, 3, 2) == 14);
    assert(countBalancedSubsequences(5, 5, 2) == 35);
    assert(countBalancedSubsequences(6, 1, 1) == 6);
    assert(countBalancedSubsequences(1, 6, 1) == 6);
    assert(countBalancedSubsequences(7, 2, 2) == 27);
    assert(countBalancedSubsequences(8, 3, 3) == 110);
    assert(countBalancedSubsequences(10, 10, 5) == 10659);
    assert(countBalancedSubsequences(20, 20, 10) == 574221648);
    assert(countBalancedSubsequences(2000, 2000, 1000) == 854104531);
    assert(countBalancedSubsequences(2000, 1999, 1000) == 334874485);
    assert(countBalancedSubsequences(2000, 2000, 1999) == 259428024);
    return 0;
}