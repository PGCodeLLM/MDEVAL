#include<assert.h>
#include <assert.h>
#include <stdio.h>

int count_coloring_methods(int n, int m)
{
    int f[1111]; 
    if (n == 1) return m;
    if (n == 2) return (long long)m * (m - 1) % 1000003;
    f[1] = m;
    f[2] = (long long)m * (m - 1) % 1000003;
    f[3] = (long long)f[2] * (m - 2) % 1000003;
    for(int i = 4; i <= n; i++) {
        f[i] = ((long long)f[i - 1] * (m - 2) % 1000003 +
                (long long)f[i - 2] * (m - 1) % 1000003) % 1000003;
    }
    return f[n];
}

int main() {
    assert(count_coloring_methods(1, 1) == 1);
    assert(count_coloring_methods(2, 2) == 2);
    assert(count_coloring_methods(3, 3) == 6);
    assert(count_coloring_methods(4, 2) == 2);
    assert(count_coloring_methods(1000, 10) == 566585); // We don't have the expected result for this case

    // Additional test cases
    assert(count_coloring_methods(2, 3) == 6);
    assert(count_coloring_methods(1000, 1000) == 67911);
    assert(count_coloring_methods(999,66) == 501817);
    assert(count_coloring_methods(5, 3) == 30); // Example of an expected output

    // printf("All tests passed!\n");
    return 0;
}