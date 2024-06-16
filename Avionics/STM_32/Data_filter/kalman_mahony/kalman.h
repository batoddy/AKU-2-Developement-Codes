
#ifndef H
#define H [3][3] = {{1, 0, 0}, {0, 1, 0}, {0, 0, 1}}
#endif

#ifndef Q
#define Q [3][3] = {{0.01, 0, 0}, {0, 0.01, 0}, {0, 0, 0.01}} // process noise covariance matrix
#endif

#ifndef R
#define R [3][3] = {{25, 0, 0}, {0, 25, 0}, {0, 0, 25}} // measurement noise covariance matrix
#endif

#ifndef x
#define x [3][1] = {{0}, {0}, {0}}
#endif

#ifndef P
#define P [3][3] = {{1, 0, 0}, {0, 1, 0}, {0, 0, 1}}
#endif

#ifndef A
#define A [3][3] = {{1, 0, 0}, {0, 1, 0}, {0, 0, 1}}
#endif

#include <math.h>
#include <stdio.h>

static void multiplyMatrix(float m1[3][3], float m2[3][3], float result[3][3], float R1, float R2, float C2)
{
  for (int i = 0; i < R1; i++)
  {
    for (int j = 0; j < C2; j++)
    {
      result[i][j] = 0;

      for (int k = 0; k < R2; k++)
      {
        result[i][j] += m1[i][k] * m2[k][j];
      }
    }
  }
  return result;
}

static void transpose(float A[3][3], float B[3][3])
{
  int i, j;
  for (i = 0; i < 3; i++)
    for (j = 0; j < 3; j++)
      // Assigns the transpose of element A[j][i] to
      // B[i][j]
      B[i][j] = A[j][i];
}

static void sum(float a[3][3], float b[3][3], float sum[3][3], float r, float c)
{
  for (i = 0; i < r; ++i)
  {
    for (j = 0; j < c; ++j)
    {
      sum[i][j] = a[i][j] + b[i][j];
    }
  }
}

static inline void sub(float a[3][3], float b[3][3], float sub[3][3], float r, float c)
{
  for (i = 0; i < r; ++i)
  {
    for (j = 0; j < c; ++j)
    {
      sub[i][j] = a[i][j] - b[i][j];
    }
  }
}

float determinant(float a[3][3], float k)
{
  float s = 1, det = 0, b[25][25];
  int i, j, m, n, c;
  if (k == 1)
  {
    return (a[0][0]);
  }
  else
  {
    det = 0;
    for (c = 0; c < k; c++)
    {
      m = 0;
      n = 0;
      for (i = 0; i < k; i++)
      {
        for (j = 0; j < k; j++)
        {
          b[i][j] = 0;
          if (i != 0 && j != c)
          {
            b[m][n] = a[i][j];
            if (n < (k - 2))
              n++;
            else
            {
              n = 0;
              m++;
            }
          }
        }
      }
      det = det + s * (a[0][c] * determinant(b, k - 1, 3));
      s = -1 * s;
    }
  }

  return (det);
}

void cofactor(float num[3][3], float inv[3][3], float f)
{
  float b[25][25], fac[25][25];
  int p, q, m, n, i, j;
  for (q = 0; q < f; q++)
  {
    for (p = 0; p < f; p++)
    {
      m = 0;
      n = 0;
      for (i = 0; i < f; i++)
      {
        for (j = 0; j < f; j++)
        {
          if (i != q && j != p)
          {
            b[m][n] = num[i][j];
            if (n < (f - 2))
              n++;
            else
            {
              n = 0;
              m++;
            }
          }
        }
      }
      fac[q][p] = pow(-1, q + p) * determinant(b, f - 1);
    }
  }
  transpose(num, fac, inv, 3);
}

/*Finding transpose of matrix*/

void transpose(float num[3][3], float fac[3][3], float inverse[3][3], float r)
{
  int i, j;
  float b[25][25], inverse[25][25], d;

  for (i = 0; i < r; i++)
  {
    for (j = 0; j < r; j++)
    {
      b[i][j] = fac[j][i];
    }
  }
  d = determinant(num, r);
  for (i = 0; i < r; i++)
  {
    for (j = 0; j < r; j++)
    {
      inverse[i][j] = b[i][j] / d;
    }
  }
}