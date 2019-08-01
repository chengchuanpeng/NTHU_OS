from fifo import FIFO
from minheap import MinHeap
from task import Task
from npsched import NPScheduler

def DEBUG(*item):
    print("DEBUG:{0}".format(item))
    
class PScheduler(NPScheduler):
   # this means it can inherit 
   # __init__(), addTask(), dispatch(), releaseTasks()
   # clockGen(), getSchedule(), and other methods

   def preempt(self):
      # this is the new method to add to put the running task
      # back into ready queue, plus any bookkeeping if necessary.
      # back into queue
      self.readyQueue.put(self.running)
      # get new higher prioirty task
      self.running = self.readyQueue.get()

   def schedule(self):
      self.releaseTasks() # same as before
      if self.checkTaskCompletion() == False:
         # still have operation to do.
         # see if running task or next ready task has higher priority
         # hint: compare by first typecasting the tasks to tuple() first
         #   and compare them as tuples.  The tuples are defined in
         #   the __iter__() method of the Task class based on policy.
         # if next ready is not higher priority, redispatch current task.
         # otherwise,
         # - swap out current running (by calling preempt method)
         #val = compare(self.running, self.readyQueue.head())

         self.readyQueue.put(self.running)
         self.running = self.readyQueue.get()
         self.dispatch(self.running)
      # task completed or swapped out
      # pick next task from ready queue to dispatch, if one exists.
      else:
        if len(self.readyQueue) == 0: 
            self.dispatch(None)
        # pop finishing
        if len(self.readyQueue) > 0:
            task = self.readyQueue.get()
            # another turn to run
            self.running = task
            self.dispatch(self.running)

   
   # inherit 
   # - clockGen(self):
   # - getSchedule(self):
   # - getThroughput(self):
   # - getWaitTime(self):
   # - getTurnaroundTime(self):

def testPScheduler(tasks, policy):
   # the tuples are release time, cpuBurst, taskName
   nClocks = 20
   scheduler = PScheduler(nClocks, policy)
 
   for t in tasks:
      scheduler.addTask(t)

   for clock in scheduler.clockGen():
      pass

   # the following are for part 2.5
   thruput = scheduler.getThroughput()
   waittime = scheduler.getWaitTime()
   turnaround = scheduler.getTurnaroundTime()

   print('preemptive %s: %s' % (policy, scheduler.getSchedule()))
   #print("preemptive RR: A-A-B-A-B-C-A-D-B-A-D-B-A-D-A-D-None-None-None-None")
   # the following is for testing part 2.5
   '''print('  thruput = %s = %.2f, waittimes = %s = %.2f, turnaroundtime = %s = %.2f'\
       % (thruput, thruput[0]/thruput[1],
          waittime, waittime[0]/waittime[1],
          turnaround, turnaround[0]/turnaround[1]))'''

if __name__ == '__main__':
   tasks = [Task(*i) for i in [('A', 0, 7), ('B', 2, 4), ('C', 4, 1), ('D', 5, 4)]]
   print('tasks = %s' % tasks)
   for policy in ['SJF', 'FCFS', 'RR']:
      tasks = [Task(*i) for i in [('A', 0, 7), ('B', 2, 4), ('C', 4, 1), ('D', 5, 4)]]
      testPScheduler(tasks, policy)
