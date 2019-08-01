_KNOWN_SCHEMES = ["FCFS", "SJF", "RR"]
from minheap import MinHeap

class Task:
   def __init__(self, name, release, cpuBurst):
       
       # the task has a string name, release time and cpuBurst.
       self.name = name
       self.release = release
       self.cpuBurst = cpuBurst

       # the constructor may also need to initialize other fields,
       # for statistics purpose.  Examples include
       # waiting time
       # remaining time
       # last dispatched time, and
       # completion time
       self.wait_time = 0
       self.remain_time = cpuBurst
       # start from 0
       self.last_dispatched = release-1
       self.completion = 0


   def __str__(self):
     return self.name

   def __repr__(self):
     # note: the field names here are just examples.
     # if you name them differently, please change them accordingly.
     return self.__class__.__name__ + '(%s, %d, %d)' % (repr(self.name), self.release, self.cpuBurst)

   _KNOWN_SCHEMES = ["FCFS", "SJF", "RR"]

   def setPriorityScheme(self, scheme="SJF"):
     """
        the scheme can be "FCFS", "SJF", "RR", etc
     """
     if not scheme in _KNOWN_SCHEMES:
        raise ValueError("unknown priority scheme %s: must be FCFS, SJF, RR")
     self.scheme = scheme

   def __str__(self):
     return self.name

   def decrRemaining(self):
     # call this method to decrement the remaining CPU burst time
     self.remain_time-=1

   def remainingTime(self):
     # return the remaining CPU burst time
     return self.remain_time

   def done(self):
     # returns a boolean for if this task has remaining work to do
     return self.remain_time == 0
     
   def setCompletionTime(self, time):
     # records the clock value when the task is completed
     self.completion = time

   def turnaroundTime(self):
      # returns the turnaround time of this atask, as on
      # week 7 lecture slide 10
      return self.completion-self.release

   def incrWaitTime(self):
      # increments the amount of waiting time
      self.wait_time+=1

   def releaseTime(self):
     # returns the release time of ths task
     return self.release

   def __iter__(self):
      # this enables converting the task into a tuple() type so that
      # the priority queue can just cast it to tuple before comparison.
      # it depends on the policy
      if (self.scheme == 'FCFS'):
         t = (self.release, self.cpuBurst, str(self))  # example, but you may want a secondary
           # priority for tie-breaker. if so, just add them to the tuple.
      elif (self.scheme == 'SJF'): # shortest job first ??? why add self.release  t = (self.cpuBurst, self.release) become correct?? 
         t = (self.remainingTime(), self.release, str(self)) 
            # tuple that defines priority in terms of "job length"
            # or is it really job length
      elif (self.scheme == 'RR'): # round robin
         # 2nd arguemt: check if it have run 
         t = (self.last_dispatched, self.cpuBurst-self.remainingTime(), str(self))  
            # define round robin priority if you use a MinHeap;
            # or you could just use a FIFO.
      else:
         raise ValueError("Unknown scheme %s" % self.scheme)
      for i in t:
         yield i