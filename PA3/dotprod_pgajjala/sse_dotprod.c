#include <emmintrin.h>

float dotprod(float x[], float y[], int n)
{
    int i=0;

    __attribute__ ((aligned(16))) float sum[n];
    int lim = (n/4)*4;
    float ans = 0.0;

    for(i = 0; i < lim; i += 4)
    {
        __m128 a_v = _mm_load_ps(&x[i]);
        __m128 b_v = _mm_load_ps(&y[i]);
        __m128 sum_v = _mm_load_ps(&sum[i]);
        __m128 prod_v = _mm_mul_ps(a_v, b_v);
        _mm_store_ps(&sum[i], prod_v);
        ans += (sum[i] + sum[i+1] + sum[i+2] + sum[i+3]);
    }

    return ans;
}