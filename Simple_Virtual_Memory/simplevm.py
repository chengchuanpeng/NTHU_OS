"""
彭成全 105065532
"""

class SimpleVM:
    _ReplacementPolicies = ['OPT', 'LRU', 'FIFO', 'SecondChance']
    def __init__(self, numPages, numFrames, replacementPolicy):
        
        self.pageFaultCount = 0
        self.pageInCount = 0
        self.pageOutCount = 0

        self.numPages = numPages
        self.numFrames = numFrames
        if not replacementPolicy in SimpleVM._ReplacementPolicies:
            raise ValueError('Unknown replacement policy %s' % replacementPolichy)

        self.replacementPolicy = replacementPolicy
        self.pageTable = [None for i in range(numPages)]
        self.valid = ['i' for i in range(numPages)]

        self.frames = [None for i in range(numFrames)] # storage
        self.dirty = [False for i in range(numFrames)]

        # we prefill swapspace content with chars '0'... 
        # we assume swap space is the size of virtual memory.
        # this is ok since we are dealing with just one process.
        # in practice, it should be larger to handle multiple processes.
        self.swapSpace = [chr(ord('0')+i) for i in range(numPages)]

        # pretty much all of them use a frameTable since the policies
        # work on frame age, frame index etc that then gets mapped to page.
        self.frameTable = [None for i in range(numFrames)]
        if self.replacementPolicy in ['LRU']:
            # use a "stack" (really more like a queue) to track age.
            self.stack = []
        if self.replacementPolicy in ['FIFO', 'SecondChance']:
            # 'FIFO' policy is just round-robin, so just keep index.
            # similarly, SecondChance is roundRobin except it skips
            # invalid ones.
            self.turn = 0
        if self.replacementPolicy == 'SecondChance':
            self.reference = [False for i in range(numFrames)]


    def getFreeFrame(self, pageNum):
        '''
            find a free frame if any and return its frameNum, or None if not.
            You could just go down linearly until finding one, and grab it,
            or you could queue up free pages and dequeue from it.
            The assumption is caller will use it immediately to fulfill a 
            page fault.
            The pageNum is provided because we may want to optimize it 
            in case of page buffering (slide 47 of week 9).
        '''
        for i in range(self.numFrames):
            if self.frames[i] is None:
                return i
        return None

    def pickVictim(self, future=None):
        '''
            finds a page whose frame is to be taken away.
        '''
        if self.replacementPolicy == 'OPT':
            # use future knowledge to pick victim
            if future is None:
                raise ValueError('cannot pick OPT without future')
            # Your code here!!
            # find page that won't be used for longest time in future
            # Note if future is empty list, then any page is ok!
            # in any case, return the victim page's frame number.
            longest, victim = -1, None
            for index in range(len(self.valid)):
                if self.valid[index] == 'v':
                    if index in future:
                        distance = future.index(index)
                        if distance > longest:
                            longest = distance 
                            victim = index
                    else:
                        # not used anymore
                        return self.frameTable.index(index)

            return self.frameTable.index(victim)

        if self.replacementPolicy == 'LRU':
            # Your code here!!
            # pull the victim from the bottom of this "stack"
            # the assumption is if we have free frame in the first place,
            # we would not need to evict anybody.
            victim = self.stack.pop(0)
            return victim

        if self.replacementPolicy == 'FIFO':
            # Your code here!!
            # pick victim according to FIFO order
            victim = self.turn % numFrames
            self.turn +=1
            return victim

        if self.replacementPolicy == 'SecondChance':
            # Your code here!!
            # like FIFO, if found referenceBit==0 then use it; if not, 
            # mark the first whose referencedBit==1 as 0, continue.
            for _ in range(numFrames):
                for _ in range(numFrames):
                    turn = self.turn%self.numFrames
                    if self.reference[turn]==False:
                        self.turn +=1 
                        return turn
                    else:
                        self.reference[turn] = False
                        self.turn +=1 

        # if we have not returned by then, it?�s an unknown policy
        raise ValueError('unknown poliy %s' % self.replacementPolicy)

    def pageIn(self, frameNum, pageNum):
        # Your code here!!
        # called to bring in a page from swap space to the frame.
        # pageNum is used to find location in swap space.
        # for simplicity, we use pageNum to index into swap space.
        # Assume frameNum is free, and thus no page is currently using it.
        # Update the page-to-frame table and frame-to-page table,
        # set valid bit for the page, and clear dirty bit for the frame.
        # in case of SecondChance, also clear reference bit.
        content = self.swapSpace[pageNum]
        self.frames[frameNum] = content
        self.frameTable[frameNum] = pageNum
        self.pageTable[pageNum] = frameNum
        self.valid[pageNum] = 'v'

        if self.replacementPolicy=='SecondChance':
            self.reference[frameNum] = True

        self.dirty[frameNum] = False

    def pageOut(self, frameNum):
        # Your code here!!
        # this flushes a frame (for a given pageNum) to swap space.
        # Note that we only mark it as not-dirty, but it does not
        # change state of valid bit because that is someone else's decision
        # whether they want to reclaim the page or just flush it.
        # Similar to pageIn, we assume swap space uses the virtual address
        # as we have only one process.
        content = self.frames[frameNum]
        if content != self.swapSpace[self.frameTable[frameNum]]:
            self.pageOutCount +=1
            self.swapSpace[self.frameTable[frameNum]] = content
        
        self.dirty[frameNum] = False


    def getFrame(self, pageNum, future=None):
        # this is a utility that may be helpful, but not required.
        # - see if pageHit, if so, return valid frame # for read/write.
        # - if pageFault,
        #      - see if free frame available; if so, grab it;
        #      - but if no free frame, pick victim, page out first,
        #        fall thru to page-in
        #      - page-in and return the frame number
        # - bookkeeping: look up the page number whose frame is about to be reassigned
        #   - set its pageTable entry to None, clear that page's valid bit
        # finally, return the frame number for caller to use.
        # pageFault
        if repr(pageNum) not in self.frames:
            if None in self.frames:
                ff_idx = self.frames.index(None)
                self.pageTable[pageNum] = ff_idx # pidx put frameidx
                self.frames[ff_idx] = repr(pageNum) # put contents
                self.frameTable[ff_idx] = pageNum # frame_table lookup pageNum
                self.valid[pageNum] = 'v'
                self.pageFaultCount +=1
                self.pageInCount +=1
                return ff_idx
            else:
                victim = self.pickVictim(future)
                self.pageOut(victim)
                self.valid[self.frameTable[victim]] = 'i'

                self.pageTable[self.frameTable[victim]] = None
                self.frames[victim] = None
                self.pageIn(victim, pageNum)

            self.pageFaultCount +=1
            self.pageInCount +=1
        
        return self.frames.index(repr(pageNum))


    def updateAccess(self, frameNum, write=False):
        # utility to update access (common to read/write) after
        # a page has been accessed.
        if self.replacementPolicy == 'LRU':
            # Your code here!!
            # find frame in stack; if found, pop it.
            # in either case, push back on stack.
            if frameNum in self.stack: self.stack.pop(self.stack.index(frameNum))
            self.stack.append(frameNum)

        if self.replacementPolicy == 'SecondChance':
            # Your own code!! - mark the reference bit
            self.reference[frameNum] = True

        if write:  # for future use, supporting write access.
            self.dirty[frameNum] = True

    def readPage(self, pageNum, future=None):
        # Your code here!!
        # get the frame number -- can call the getFrame() method for this.
        # use the frame number to get the data so we can return it.
        # do some bookkeeping by calling updateAccess

        frame_number = self.getFrame(pageNum, future)
        self.updateAccess(frame_number)
        return self.frames[frame_number]

    def writePage(self, pageNum, data, future=None):
        # Your code here!!
        # analogous to the readPage, except 
        # the frame is written to with data.
        # do bookkeeping with write=True
        if data not in self.frames:
            if None in self.frames:
                ff_idx = self.frames.index(None)
                self.pageTable[pageNum] = ff_idx # pidx put frameidx
                self.frameTable[ff_idx] = pageNum # frame_table lookup pageNum
                self.frames[ff_idx] = data # put contents
                self.valid[pageNum] = 'v'
                self.updateAccess(ff_idx)
            else:
                if self.valid[pageNum] == 'v':
                    self.frames[self.pageTable[pageNum] ] = data
                    self.updateAccess(self.pageTable[pageNum], write = True)
                    return 
                else:
                    victim = self.pickVictim(future)
                    self.valid[self.frameTable[victim]] = 'i'
                    self.pageOut(victim)
                    self.frames[victim] = None
                    self.pageTable[self.frameTable[victim]] = None
                    self.pageIn(victim, pageNum)
                    self.frames[victim] = data
                    self.updateAccess(victim, write = True)
        
        self.pageFaultCount +=1
        self.pageInCount +=1

if __name__ == '__main__':
    def TestRead(numPages, numFrames, refString, policy):
        # ['OPT', 'LRU', 'FIFO', 'SecondChance']
        print('-------------- policy (read): %s-------------- ' % policy)
        vm = SimpleVM(numPages, numFrames, policy)
        for i, pageNum in enumerate(refString):
            nextIndex = i+1
            if nextIndex >= len(refString):
                future = []
            else:
                future = refString[nextIndex:]
            #print(future)
            r = vm.readPage(pageNum, future)
            print('readPage(%d)=%s, pageTable=%s, valid=%s, frames=%s' %\
                (pageNum, repr(r), vm.pageTable, ''.join(vm.valid), vm.frames))
        print('   page faults = %d, page ins = %d, page outs = %d' % (vm.pageFaultCount, vm.pageInCount, vm.pageOutCount))

    def TestWrite(numPages, numFrames, refString, wrData, policy):
        print('-------------- policy (write): %s-------------- ' % policy)
        vm = SimpleVM(numPages, numFrames, policy)
        for i, testData in enumerate(map(lambda x,y:(x,y), refString, wrData)):
            pageNum, data = testData
            nextIndex = i+1
            if nextIndex >= len(refString):
                future = []
            else:
                future = refString[nextIndex:]
                #print(future)
            vm.writePage(pageNum, data, future)
            print('writePage(%d, %s), frames=%s, swapSpace=%s' %\
                (pageNum, repr(data), vm.frames, vm.swapSpace))
        print('   page faults = %d, page ins = %d, page outs = %d' % (vm.pageFaultCount, vm.pageInCount, vm.pageOutCount))

    # define the script, or 
    numPages = 8
    numFrames = 3
    refString = [7,0,1,2,0,3,0,4,2,3,0,3,0,3,2,1,2,0,1,7,0,1]
    wrData = [chr(ord('A')+i) for i in range(len(refString))]
    for policy in SimpleVM._ReplacementPolicies:
        TestRead(numPages, numFrames, refString, policy)
        TestWrite(numPages, numFrames, refString, wrData, policy)
