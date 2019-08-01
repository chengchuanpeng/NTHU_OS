import bisect

class MemAlloc:

   _POLICIES = ('FirstFit', 'BestFit', 'WorstFit')

   def __init__(self, totalMemSize, policy = 'BestFit'):
      if not policy in MemAlloc._POLICIES:
         raise ValueError('policy must be in %s' % MemAlloc._POLICIES)
      self.allocation = {} # map pointer to (size)
      self.holes = [(0, totalMemSize)] # sorting by pointer
      # your code here
      self.policy = policy

   # insert your own utility methods as needed
   def firstPos(self, reqSize):
       if self.holes[0][1] >= reqSize: return 0
       else: return -1
   
   def bestPos(self, reqSize):
       holes_size = [ hole[1]-reqSize for hole in self.holes]
       available_space = [ hole for hole in holes_size if hole >=0]
       if available_space:
           hole_pos = holes_size.index(min(available_space))
           return hole_pos
       else:
           return -1

   def maxPos(self, reqSize):
       # return idx
       holes_size = [ hole[1] for hole in self.holes]
       if max(holes_size) >= reqSize:
           return holes_size.index(max(holes_size))
       else:
           return -1
   
   def merge(self):
       merge_finish = False
       while not merge_finish:
           lastpos = -1
           for holepos in range(len(self.holes)):
               hole = self.holes[holepos]
               if lastpos > -1 and lastpos == hole[0]:
                   new_hole = (self.holes[holepos-1][0], self.holes[holepos-1][1]+hole[1])
                   self.holes.pop(holepos-1)
                   self.holes.pop(holepos-1)
                   bisect.insort(self.holes, new_hole)
                   break
               lastpos = hole[0]+hole[1]
           if holepos == len(self.holes)-1:
               merge_finish = True

   def malloc(self, reqSize):
      '''return the starting address of the block of memory, or None'''
      # your code here
      if not self.holes or reqSize is None : return None
      
      if self.policy == 'FirstFit':
          pos = self.firstPos(reqSize)
      elif self.policy == 'WorstFit':
          pos = self.maxPos(reqSize)
      else:
          pos = self.bestPos(reqSize)
      if pos == -1:
          return None

      address, remainMemSize, nextaddress = self.holes[pos][0], self.holes[pos][1] - reqSize \
      ,self.holes[pos][0]+reqSize
      self.allocation.update({address:reqSize})
      self.holes.pop(pos)
      if remainMemSize == 0:
        return address
      bisect.insort(self.holes, (nextaddress, remainMemSize))
      return address

   def free(self, pointer):
      '''free the previously allocated memory starting at pointer'''
      # your code here
      if pointer not in self.allocation : return
      free_space = (pointer, self.allocation[pointer])
      bisect.insort(self.holes, free_space)
      del self.allocation[pointer]
      self.merge()

   def __str__(self):
      return repr(self.allocation)


def runTestScript(requests):
   ff = MemAlloc(20, 'FirstFit')
   bf = MemAlloc(20, 'BestFit')
   wf = MemAlloc(20, 'WorstFit')
   ffSym = {}
   bfSym = {}
   wfSym = {}
   for name, size in requests:
      if size is None:
         # do a free() call
         ff.free(ffSym[name]); del(ffSym[name])
         bf.free(bfSym[name]); del(bfSym[name])
         wf.free(wfSym[name]); del(wfSym[name])
         print('free(%s)' % name)
      else: 
         # do an malloc() call
         ffSym[name] = ff.malloc(size)
         bfSym[name] = bf.malloc(size)
         wfSym[name] = wf.malloc(size)
         print('%s=malloc(%d):' % (name, size))
      print(' FirstFit symbols=%s holes=%s allocation=%s' % (ffSym, ff.holes, ff.allocation))
      print(' BestFit symbols=%s holes=%s allocation=%s' % (bfSym, bf.holes, bf.allocation))
      print(' WorstFit symbols=%s holes=%s allocation=%s' % (wfSym, wf.holes, wf.allocation))

if __name__ == '__main__':

   requests = [('a', 10), ('b', 1), ('c', 4), ('c', None), ('a', None),
               ('d', 9),  # worst fit and first fit would use (0, 10), but best fit would use (11, 9)
               ('e', 10), # worst fit and first fit wold fail, but best fit would succeed with (0, 10)
    ]
   runTestScript(requests)

   print('------------------------')

   requests = [('a', 3), ('b', 6), ('c', 2), ('d', 5), # malloc
               ('a', None), ('c', None), # free
               ('e', 2),  # best fit (9, 2), first fit (0, 2), worst fit (16, 2)
               ('b', None), # free: best fit merges (0,3) and (3,6) => (0,9)
                   # first fit merges (3,6), (9,2) => (3, 8)
                   # worst fit merges (0,3), (3,6), (9,2) => (0,11)
               ('f', 11)   # both best fit and first fit fail, but worst fit succeeds
    ]
   runTestScript(requests)

   print('---------Bonus---------------')

   requests = [('a', 5), ('b', 3) , ('c', 4), ('b', None), 
               ('d', 3), ('e', 1), ('f', 4), ('c', None), ('g', 3), ('h', 1), ('f', None), ('i', 6)
    ]
   runTestScript(requests)