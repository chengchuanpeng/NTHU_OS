import threading
import queue
import time

MAXTHREAD = 200

def Partition(A, p, r):
    x = A[r]
    i = p - 1
    for j in range(p, r):
        if (A[j] <= x):
            i = i + 1
            A[i], A[j] = A[j], A[i]
    A[i+1], A[r] = A[r], A[i+1]
    return i + 1

'''
Create a new thread for one of the two recursive calls by calling threading.Thread(), and assign it to a variable.  
The target parameter is the function for the thread to call, and the args parameter is the tuple of parameters to pass.

Unlike POSIX threads, instantiating a thread does not start running it; you have to explicitly call the .start() method
on the thread to start running it.  
The parent thread itself can do the other recursive call concurrently.
 (The parent could create two threads but it would be wasteful, since the parent would have nothing else to do).

(parent) wait for the (child) thread to complete by calling the .join() method on it.

When the data size is small (e.g., 10), it probably does not hurt to create threads for recursive calls, 
but when the data size is large (e.g., 20 million), then you want to limit the number of threads you create. 
Add code to limit thread creation based on the number of threads currently running.  
If it exceeds the (self-imposed) maximum number of threads (that you allow), then don’t make a new thread for recursive call;
instead, just call QuickSort normally. 
Otherwise, make a new thread, start it, and join it.
'''
def QuickSort(A, p, r):
    if p < r :
        t = None
        q = Partition(A, p, r)
        if threading.active_count() < MAXTHREAD:
            t = threading.Thread(target = QuickSort, args = (A, p, q-1))
            t.start() 
        #if GetThreadNumber()!=-1: 
        #    t.start()
        else :
            QuickSort(A, p, q-1)

        QuickSort(A, q+1, r)
        
        if t is not None:
            t.join()
        #if threading.active_count() > 0:
        #    t.join()
        #if not thread_queue.empty():
        #    t.join()

if __name__ == '__main__':
    LEN = 20000000
    #LEN = 200
    L = list(range(LEN))
    import random
    random.shuffle(L)
    QuickSort(L, 0, len(L)-1)
    if L == list(range(LEN)):  # Python3 list(range(LEN)) instead of range(LEN)
        print("successfully sorted")
    else:
        print("sort failed: %s" % L)

