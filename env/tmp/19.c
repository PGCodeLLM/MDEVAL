#include <assert.h>
#include<assert.h>
#include <stdio.h>
#include <string.h>

int countPermutations(int n, int k, int qq[])
{
    const int N = 505, P = 998244353;
    int q[N], dp[N][N], jc[N], f[N], ans;
    memset(q, 0, sizeof(q));
    memset(dp, 0, sizeof(dp));
    memset(jc, 0, sizeof(jc));
    memset(f, 0, sizeof(f));
    ans = 0;
    for (int i = 1; i <= n; i++)
        q[i] = qq[i - 1];
    dp[0][0] = f[0] = 1;
    for (int i = jc[0] = 1; i <= n; i++)
        jc[i] = 1LL * jc[i - 1] * i % P;
    for (int i = 1; i <= n; i++)
    {
        f[i] = jc[i];
        for (int j = 1; j < i; j++)
            f[i] = (f[i] + P - 1LL * f[j] * jc[i - j] % P) % P;
    }
    for (int i = 1; i <= n; i++)
    {
        for (int j = 0; j < i; j++)
            for (int kk = 1; kk <= k; kk++)
                dp[i][kk] = (dp[i][kk] + dp[j][kk - 1] * 1LL * f[i - j] % P) % P;
    }
    int m = 0;
    for (int i = 1; i < n; i++)
        if (q[i] > q[i + 1])
        {
            m = i;
            break;
        }
    if (m == 0)
    {
        for (int i = k; i <= n; i++)
            ans = (ans + dp[n][i]) % P;
    }
    else
    {
        for (int i = m + 1; i <= n; i++)
        {
            if (i != m + 1 && (q[i - 1] > q[i] || q[i] < q[m]))
                break;
            int c = k + i - n - 1;
            if (c >= 0)
                ans = (ans + dp[m][c] * 1LL * jc[i - m - 1] % P) % P;
        }
    }
    return ans;
}

int main() {
    int q1[] = {1, 2};
    assert(countPermutations(2, 1, q1) == 2);

    int q2[] = {3, 1, 2};
    assert(countPermutations(3, 3, q2) == 1);

    int q3[] = {1, 2, 3, 6, 5, 4};
    assert(countPermutations(6, 3, q3) == 13);

    int q4[] = {1, 2, 3, 4, 5, 6};
    assert(countPermutations(6, 1, q4) == 720);

    int q5[] = {1, 2, 5, 3, 4, 5};
    assert(countPermutations(6, 3, q5) == 0);

    int q6[] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    assert(countPermutations(9, 9, q6) == 1);

    int q7[] = {1, 2, 3, 4, 5, 6, 7, 9, 8};
    assert(countPermutations(9, 2, q7) == 29093);
    return 0;}