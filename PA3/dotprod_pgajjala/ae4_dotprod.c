float dotprod(float x[], float y[], int n)
{
    int i;
    float sum1 = 0.0;
    float sum2 = 0.0;
    float sum3 = 0.0;
    float sum4 = 0.0;
    float ans = 0.0;

    for(i = 0; i < n/4; i++)
    {
        sum1 += x[i*4] * y[i*4];
        sum2 += x[i*4+1] * y[i*4+1];
        sum3 += x[i*4+2] * y[i*4+2];
        sum4 += x[i*4+3] * y[i*4+3];
    }

    ans = sum1 + sum2 + sum3 + sum4;

    return ans;
}
