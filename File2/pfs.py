# 彭成全 105065532

'''
    pfs.py is a toy file system in python.
'''

from cntlblks import *
from pfsHW9 import *

class PFS(PFSHW9):
    def __init__(self, nBlocks=16, nDirs=32, nFCBs=64):
        PFSHW9.__init__(self, nBlocks, nDirs, nFCBs)

    def readBlock(self, physicalBlockNumber):
        return self.storage[physicalBlockNumber]

    def writeBlock(self, physicalBlockNumber, data):
        self.storage[physicalBlockNumber] = data

    def allocateBlocks(self, nBlocksToAllocate):
        # allocates free blocks from the pool and return the set of
        # block numbers 
        # * if there are not enough blocks, then return None
        # * find S = nBlocksToAllocate members from the free set
        # * remove S from the free set
        # * return S

        if nBlocksToAllocate > len(self.freeBlockSet):
            return None
        space = set()
        for i in range(nBlocksToAllocate):
            space.add(self.freeBlockSet.pop())
        return space

    def freeBlocks(self, blocksToFree):
        # blocksToFree is the set of block numbers as returned from
        # allocateBlocks().
        # * set the free set to union with the blocksToFree.
        # * strictly speaking, those blocks should also be erased.
        self.freeBlockSet = self.freeBlockSet.union(blocksToFree)
        del blocksToFree
        return None

    ''' The following functions was inherited from the provided pfsHW9.pyc '''
    # def allocFCB(self):
    # def freeFCB(self, f):
    # def allocDEntry(self):
    # def freeDEntry(self, d):
    # def parsePath(self, path, defaultDir):
    # def createFile(self, name, enclosingDir):
    # def createDir(self, name, enclosingDir):
    # def deleteFile(self, name, enclosingDir):
    # def deleteDirectory(self, name, enclosingDir):
    # def rename(self, name, newName, enclosingDir):
    # def move(self, name, fromDir, toDir):

def testBlockAlloc(fs):
    print('freeblocks=%s' % fs.freeBlockSet)
    a = fs.allocateBlocks(5)
    b = fs.allocateBlocks(3)
    c = fs.allocateBlocks(2)
    d = fs.allocateBlocks(1)
    e = fs.allocateBlocks(4)
    print('allocate (5)a=%s, (3)b=%s, (2)c=%s, (1)d=%s, (4)e=%s' % (a,b,c,d,e))
    print('freeBlockSet=%s' % fs.freeBlockSet)
    fs.freeBlocks(b)
    print('after freeBlocks(%s), freeBlockSet=%s' % (b, fs.freeBlockSet))
    fs.freeBlocks(d)
    print('after freeBlocks(%s), freeBlockSet=%s' % (d, fs.freeBlockSet))
    f = fs.allocateBlocks(4)
    print('after allocateBlocks(4)=%s, freeBlockSet=%s' % (f, fs.freeBlockSet))
    fs.freeBlocks(a | c)
    print('after freeBlocks(a|c)=%s, freeBlockSet=%s' % (a|c, fs.freeBlockSet))
    
if __name__ == '__main__':
    fs = PFS(nBlocks = 16)
    testBlockAlloc(fs)
