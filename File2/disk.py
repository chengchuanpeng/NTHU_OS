# 彭成全 105065532
# disk scheduling algorithms

class DiskScheduler:
    _POLICIES = ['FCFS', 'SSTF', 'SCAN', 'LOOK', 'C-SCAN', 'C-LOOK']

    def __init__(self, nCylinders):
        self.nCylinders = nCylinders

    def schedule(self, initPos, requestQueue, policy, direction):
        '''
            request is the list of cylinders to access
            policy is one of the strings in _POLICIES.
            direction is 'up' or 'down'
            returns the list for the order of cylinders to access.
        '''
        if policy == 'FCFS':
            # return the disk schedule for FCFS
            return requestQueue

        if policy == 'SSTF':
            # shortest seek time first
            # compute and return the schedule for the shortest seek time first
            resultQueue = []
            copyRequestQueue = requestQueue[::]
            curPos = initPos
            for i in range(len(copyRequestQueue)):
                curShortest = [ abs(curPos - p) for p in copyRequestQueue]
                pos = curShortest.index(min(curShortest))
                resultQueue.append(copyRequestQueue[pos])
                copyRequestQueue.remove(copyRequestQueue[pos])
            return resultQueue
            
        if policy in ['SCAN', 'C-SCAN', 'LOOK', 'C-LOOK']:
            # sequentially one direction to one end, 
            # then sequentially to the other `
            # decide on direction (up or down) based on initial request
            # compute and return the schedule accordingly
            resultQueue = []
            curPos = initPos
            newOrder = {}

            sortedDirection = sorted([ p - curPos for p in requestQueue])
            upDirection = [ p + curPos for p in sortedDirection if p > 0]
            downDirection = [ p + curPos for p in sortedDirection if p <=0][::-1]

            if policy == 'SCAN':
                
                if direction == 'up':
                    resultQueue += upDirection
                    if self.nCylinders - 1 not in resultQueue:
                        resultQueue += [self.nCylinders - 1]
                    resultQueue += downDirection

                if direction == 'down':
                    resultQueue += downDirection
                    if 0 not in resultQueue:
                        resultQueue += [0]
                    resultQueue += upDirection
            
            if policy == 'LOOK':
                if direction == 'up':
                    resultQueue += upDirection
                    resultQueue += downDirection

                if direction == 'down':
                    resultQueue += downDirection
                    resultQueue += upDirection
            
            if policy == 'C-SCAN':
                if direction == 'up':
                    resultQueue += upDirection
                    if self.nCylinders - 1 not in upDirection:
                        resultQueue += [self.nCylinders - 1]
                    if 0 not in downDirection:
                        resultQueue += [0]
                    resultQueue += downDirection[::-1]

                if direction == 'down':
                    resultQueue += downDirection
                    if 0 not in downDirection:
                        resultQueue += [0]
                    if self.nCylinders - 1 not in upDirection:
                        resultQueue += [self.nCylinders - 1]
                    resultQueue += upDirection[::-1]

            if policy == 'C-LOOK':
                if direction == 'up':
                    resultQueue += upDirection
                    resultQueue += downDirection[::-1]
                if direction == 'down':
                    resultQueue += downDirection
                    resultQueue += upDirection[::-1]

            return resultQueue

def totalSeeks(initPos, queue):
    lastPos = initPos
    totalMoves = 0
    for p in queue:
        totalMoves += abs(p - lastPos)
        lastPos = p
    return totalMoves

if __name__  == '__main__':
    def TestPolicy(scheduler, initHeadPos, requestQueue, policy, direction):
        s = scheduler.schedule(initHeadPos, requestQueue, policy, direction)
        t = totalSeeks(initHeadPos, s)
        print('policy %s %s (%d): %s' % (policy, direction, t, s))

    scheduler = DiskScheduler(200)
    requestQueue = [98, 183, 37, 122, 14, 124, 65, 67]
    initHeadPos = 53
    for policy in DiskScheduler._POLICIES:
        if policy[:2] == 'C-' or policy[-4:] in ['SCAN', 'LOOK']:
            TestPolicy(scheduler, initHeadPos, requestQueue, policy, 'up')
            TestPolicy(scheduler, initHeadPos, requestQueue, policy, 'down')
        else:
            TestPolicy(scheduler, initHeadPos, requestQueue, policy, '')

    print('more tests on SCAN and C-SCAN')
    rQs = [[98, 37, 0, 122, 14], [98, 37, 199, 122, 14], [98, 0, 37, 199, 14]]
    for q in rQs:
        print('Q=%s' % q)
        for policy in ['SCAN', 'C-SCAN']:
            for direction in ['up', 'down']:
                TestPolicy(scheduler, initHeadPos, q, policy, direction)
