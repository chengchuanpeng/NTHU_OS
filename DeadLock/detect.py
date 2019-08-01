from banker import Banker, sumColumn, IncrVec, DecrVec, GtVec

class DeadlockDetector(Banker):
   def __init__(self, alloc, totalRsrc):
      Banker.__init__(self, alloc, None, totalRsrc)
      self.trace = True

   def detect(self, Request):
      '''detect deadlock with the request matrix'''
      # 1(a) initialize Work = a copy of Available
      # 1(b) Finish[i] = (Allocation[i] == [0, ...0])
      # optionally, you can keep a Sequence list
      Work = self.Available[:]
      # sequenece
      Sequence = []
      not_done = []
      last_not_done = [-1]

      Finish = [ all([ r == 0 for r in process]) for process in self.Allocation ]
      print("Finish=%s" %(Finish))
      for _ in range(self.n):
          for i in range(self.n):
              if self.trace: print('i=%d, ' % i, end="")
              # Step 2: similar to safety algorithm
              #   if there is an i such that (Finish[i] == False)
              #   and Request_i <= Work, (hint: LeVec() or GtVec()) then
              #   Step 3: 
              #     Work += Allocation[i] # hint IncrVec()
              #     Finish[i] = True
              #        continue Step 2
              if Finish[i] == False and not GtVec(Request[i], Work):
                  temp_work = Work[:]
                  IncrVec(Work, self.Allocation[i])
                  Finish[i] = True
                  Sequence.append(i)
                  if self.trace:
                    print("(Request[%d]=%s) <= (Work=%s) %r, append P%d (+Allocation[%d]=%s)=> Work=%s, Finish=%s" % \
                    (i, Request[i], temp_work, Finish[i], i, i, self.Allocation[i], Work, Finish))
                  if all(Finish):
                      return Sequence
              # printing
              elif self.trace and Finish[i]:
                  print("Finish[%d] is %r, skipping" % (i, Finish[i]))
              
              else:
                  print("(Request[%d]=%s) <= (Work=%s) %r, P%d must wait" % \
                  (i, Request[i], Work, Finish[i], i))
                  not_done.append(i)
          
          if not_done == last_not_done: break
          last_not_done = not_done[:]
          not_done = []
      # Step 4: either done iterating or (no such i exists)
      #    Finish vector indicates deadlocked processes.
      #    if all True then no deadlock.
      if any([ done == False for done in Finish]) :
          return None
      else:
          return Sequence


if __name__ == '__main__':

   Allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 3], [2, 1, 1], [0, 0, 2]]
   #Request    = [[0, 0, 0], [2, 0, 2], [0, 0, 0], [1, 0, 0], [0, 0, 2]]
   Request    = [[[0, 0, 0], [2, 0, 2], [0, 0, 0], [1, 0, 0], [0, 0, 2]]
   ,[[0, 0, 0], [2, 0, 2], [0, 0, 1], [1, 0, 0], [0, 0, 2]]]
   Available  = [0, 0, 0]
   TotalResources = [7, 2, 6]
   d = DeadlockDetector(Allocation, TotalResources)
   for req in Request:
    s = d.detect(req)
    if s is not None:
        print('sequence = %s' % s)
    else:
        print('deadlock')
 