#include<assert.h>
#include <assert.h>
#include <stdio.h>

long long maxModeSum(int n, const int counts[])
{
    long long ans = 0;
    int mx = 0;
    long long f[100001] = {0};
    
    for (int i = n; i > 0; --i) {
        while (mx < counts[i - 1]) {
            mx++;
            f[mx] = f[mx - 1] + i;
        }
        ans += f[counts[i - 1]];
    }
    return ans;
}

int main() {
    assert(maxModeSum(3, (int[]){1, 3, 2}) == 17);
    assert(maxModeSum(4, (int[]){4, 1, 2, 3}) == 37);
    assert(maxModeSum(2, (int[]){1, 1}) == 4);
    assert(maxModeSum(5, (int[]){1, 2, 3, 4, 5}) == 75);
    assert(maxModeSum(1, (int[]){100000}) == 100000);
    assert(maxModeSum(5, (int[]){5, 3, 2, 4, 1}) == 62);
    assert(maxModeSum(3, (int[]){100000, 100000, 100000}) == 900000);
    assert(maxModeSum(3, (int[]){2, 2, 5}) == 27);
    assert(maxModeSum(4, (int[]){4, 4, 4, 4}) == 64);
    assert(maxModeSum(6, (int[]){1, 2, 3, 4, 5, 6}) == 126);
    assert(maxModeSum(3, (int[]){3, 1, 2}) == 16);
    return 0;
}