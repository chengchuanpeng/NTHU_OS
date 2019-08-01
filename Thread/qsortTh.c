
#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#define MAXTHRAED 2000

int *A; // array
int worker = 0;
pthread_mutex_t threadMutex;

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

int GetThreadNumber()
{
    int threadNum;
    if (worker >= MAXTHRAED)
        return -1;
    pthread_mutex_trylock(&threadMutex);

    if (worker < MAXTHRAED)
    {
        threadNum = worker++;
        //printf("%d\n", threadNum);
    }
    else
        threadNum = -1;

    pthread_mutex_unlock(&threadMutex);
    return threadNum;
}

void *QuickSort(void *arg)
{
    int *data = (int *)arg;
    int p = data[0], r = data[1];
    if (p < r)
    {
        int q = Partition(A, p, r);
        int argsp[2] = {p, q - 1};
        pthread_t thread;

        int idx = GetThreadNumber();

        // generate thread to assign for 
        if (idx != -1)
        {
            int rc = pthread_create(&thread, 0, QuickSort, argsp);
            if (rc)
            {
                printf("ERROR; return code from pthread_create() is %d\n", rc);
                exit(-1);
            }
        }
        else // self do 
        {
            QuickSort(argsp);
        }
        int argsr[2] = {q + 1, r};
        QuickSort(argsr);
        pthread_join(thread, NULL);
    }
}

int main(int argc, char *argv[])
{

    pthread_mutex_init(&threadMutex, NULL);
    FILE *fh = fopen("randomInt.txt", "r");
    int len;
    fscanf(fh, "%d", &len);
    A = calloc(len, sizeof(int));
    for (int i = 0; i < len; i++)
    {
        fscanf(fh, "%d", A + i);
    }
    fclose(fh);

    int args[2] = {0, len - 1};
    QuickSort(args);
    pthread_mutex_destroy(&threadMutex);

    for (int i = 0; i < len; i++)
    {
        if (A[i] != i)
        {
            fprintf(stderr, "error A[%d]=%d\n", i, A[i]);
        }
        /*else
            //fprintf(stdout, "Correct: A[%d]=%d\n", i, A[i]);*/
    }
}