#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int *A; // array

int Partition(int A[], int p, int r)
{

    int position = p;
    int temp;

    for (int i = p; i < r; i++)
    {
        if (A[i] <= A[r])
        {
            temp = A[position];
            A[position++] = A[i];
            A[i] = temp;
        }
    }

    temp = A[position];
    A[position] = A[r];
    A[r] = temp;

    return position;
}

void *QuickSort(int A[], int p, int r)
{
    if (p < r)
    {
        int q = Partition(A, p, r);
        //int q = Partition(p, r);
        QuickSort(A, p, q - 1);
        QuickSort(A, q + 1, r);
    }
}

int main(int argc, char *argv[])
{
    // FILE* fh = fopen("randomInt.txt", "r");
    FILE *fh = fopen("randomInt.txt", "r");
    int len;
    fscanf(fh, "%d", &len);
    A = calloc(len, sizeof(int));
    for (int i = 0; i < len; i++)
    {
        fscanf(fh, "%d", A + i);
    }

    fclose(fh);
    QuickSort(A, 0, len - 1);
    // check if they are sorted
    for (int i = 0; i < len; i++)
    {
        if (A[i] != i) {
            fprintf(stderr, "error A[%d]=%d\n", i, A[i]);
        }
    }
}