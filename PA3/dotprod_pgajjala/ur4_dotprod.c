float dotprod(float x[], float y[], int n)
{
    int i;
    float ans = 0.0;

    //unrolls 4 at a time

    for(i = 0; i < n/4; i++)
    {
        ans += x[i*4] * y[i*4];
        ans += x[i*4+1] * y[i*4+1];
        ans += x[i*4+2] * y[i*4+2];
        ans +=x[i*4+3] * y[i*4+3];
    }

    return ans;
}