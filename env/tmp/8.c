#include <assert.h>
#include<assert.h>
int count_acute_triangles(int edges_count, ...)
{
    va_list args;
    va_start(args, edges_count);
    int* edges = malloc(edges_count * sizeof(int));
    for (int i = 0; i < edges_count; i++) {
        edges[i] = va_arg(args, int);
    }
    va_end(args);
    qsort(edges, edges_count, sizeof(int), (int (*)(const void *, const void *)) int_cmp);
    int sum = 0;
    for (int i = 0; i < edges_count - 2; i++) {
        for (int j = i + 1; j < edges_count - 1; j++) {
            for (int k = j + 1; k < edges_count; k++) {
                int x = edges[i], y = edges[j], z = edges[k];
                if (x + y > z && x * x + y * y > z * z) {
                    sum++;
                }
            }
        }
    }
    free(edges);
    return sum;
}

int int_cmp(const void *a, const void *b) {
    return (*(int *)a - *(int *)b);
}

int main()
{
    assert(count_acute_triangles(4, 1, 1, 1, 1) == 4);
    assert(count_acute_triangles(3, 1, 2, 3) == 0);
    // Additional tests to ensure correctness
    assert(count_acute_triangles(5, 3, 4, 5, 7, 10) == 0);
    assert(count_acute_triangles(6, 6, 8, 10, 5, 5, 5) == 4);
    return 0;
}