'''
    pfs.py is a toy file system in python.
'''
# 彭成全 105065532



from cntlblks import *

class PFS:
    def __init__(self, nBlocks=16, nDirs=32, nFCBs=64):
        '''
            nBlocks is an int for the number of blocks in this file system (for user)
            root is the directory control block of the root and
            has the link to some initial directories.
        '''
        # - on-disk structure, assuming one partition:
        #   - list of directory control blocks (more like a tree)
        #   - list of file control blocks
        self.nBlocks = nBlocks

        self.FCBs = [ ] # file control blocks
        self.freeBlockSet = set(range(nBlocks)) # not used yet
        self.freeDEntrys = [DEntry() for i in range(nDirs)]
        self.freeFCBs = [FCB() for i in range(nFCBs)]

        self.root = self.allocDEntry()

        # - in-memory structure
        #   - in-memory directory structure
        #   - system-wide open file table
        #   - per-process open file table
        self.sysOpenFileTable = []
        self.sysOpenFileCount = []

        self.storage = [None for i in range(nBlocks)]  # physical storage


    def allocFCB(self):
        f = self.freeFCBs.pop()
        FCB.__init__(f)
        return f

    def freeFCB(self, f):
        self.freeFCBs.append(f)

    def allocDEntry(self):
        d = self.freeDEntrys.pop() # recycle
        DEntry.__init__(d)  # start fresh
        return d

    def freeDEntry(self, d):
        self.freeDEntrys.append(d)


    def parsePath(self, path, defaultDir):
        '''
            utility function to convert from file path (absolute or relative)
            to (DEntry, filename).
            If no directory is specified, then the current working directory
            is returned; filename may be None if empty string.
        '''
        t = path.split('/')
        d = self.root
        filename = ''  # by default, name is empty
        if len(t) == 1:
            # no slash = use defaultDir
            d = defaultDir
            return d, t[0]
        elif len(t) > 1:
            # at least we have a slash
            if t[0] == '':
                # start from root
                d = self.root
            else: # relative to current directory
                d = defaultDir.lookup(t[0])
            # remove trailing / if there is one
            if t[-1] == '':
                filename = t.pop()
            for i, n in enumerate(t[1:]):
                #print("i &n :", i , n, t)
                member = d.lookup(n)
                if member is None:
                    filename = n
                    break
                if isinstance(member, DEntry):
                    # keep going
                    d = member
                    continue
                if isinstance(member, FCB):
                    # this must be the last
                    if i == len(t[1:]) - 1:
                        filename = n
                        break
                raise ValueError('%s is not a directory' % n)
            # now d points to the directory
            return (d, filename)
        else: # len(t) < 1: not possible
            raise ValueError('split error on %s' % path)


    def createFile(self, name, enclosingDir):
        # @@@ write your code here
        # pass
        # allocate a new FCB and update its directory structure:
        # * if default directory is None, set it to root. ???
        # * if name already exists, raise exception
        # * allocate a new FCB, add it to the enclosing dir by name,
        # * append to the FCB list of the file system.
        # Note: this does not allocate blocks for the file.
        if enclosingDir is None :
            enclosingDir = root
        if name in enclosingDir.names:
            raise ValueError("File %s exits in Dirs" % name)
        else:
            newfile = self.allocFCB()
            self.FCBs.append(newfile)
            enclosingDir.addFile(newfile, name)

    def createDir(self, name, enclosingDir):
        # @@@ write your code here
        # create a new directory under name in enclosing directory.
        # * check if name already exists; if so, raise exception.
        # * allocate a DEntry, add it to enclosing directory,
        # * return the new DEntry.
        if name in enclosingDir.names:
            raise ValueError("Dir %s exits in ParentDirs" % name)
        else:
            newDEntry = self.allocDEntry()
            enclosingDir.addDir(newDEntry, name)
            return newDEntry

    def deleteFile(self, name, enclosingDir):
        # @@@ write your code here
        # pass
        # * lookup the fcb by name in the enclosing directory.
        # * if linkCount is 1 (which means about to be 0 after delete)
        #   and the file is still opened by others, then
        #   raise an exception about unable to delete open files.
        # * call rmFile on enclosingDir to remove the fcb (and name).
        # * if no more linkCount, then 
        #   * recycle free the blocks.
        #   * recycle the fcb
        file = enclosingDir.lookup(name)
        if file.linkCount > 0 and file.openCount > 0: 
            raise ValueError("Delete %s failed, some Dir may link or the file is opened." % name)
        elif file.openCount > 0 : 
            raise ValueError("Delete %s failed, file may opened." % name)
        else:
            enclosingDir.rmFile(file)
            self.freeFCB(file)
            self.FCBs.remove(file)

    def deleteDirectory(self, name, enclosingDir):
        # @@@ write your code here
        # * lookup the dentry by name in the enclosing directory.
        # * if the directory is not empty, raise exception about
        #   unable to delete nonempty directory.
        # * call rmDir on enclosing directory
        # * recycle the dentry
        # pass
        dentry = enclosingDir.lookup(name)
        if len(dentry.content) > 0:
            raise ValueError("Unable to delete nonempty directory %s " % name)
        else:
            enclosingDir.rmDir(dentry)
            self.freeDEntry(dentry)

    def rename(self, name, newName, enclosingDir):
        # @@@ write your code here
        # fs.rename('hello.c', 'goodbye.py', d)
        # pass
        # * check if newName is already in enclosingDir, raise exception
        # * find position of name in names list of enclosingDir
        # * change the name to newName in that list
        # * set last modification time of enclosing directory
        if newName in enclosingDir.names:
            raise ValueError("File %s exits in Dirs" % name)
        else:
            name_idx = enclosingDir.names.index(name)
            enclosingDir.names[name_idx] = newName
            enclosingDir.updateModTime()

    def move(self, name, fromDir, toDir):
        # @@@ write your code here
        # pass
        # * check if name is already in toDir, raise exception
        # * lookup name and see if it is directory or file.
        # * if directory, remove it from fromDir (by calling rmDir),
        #   add it to toDir (by calling addDir)
        # * if file, remove it from fromDir (by calling rmFile)
        #   add it to toDir (by calling addFile)
        if name in toDir.names:
            raise ValueError("File %s exits in toDir" % name)
        else:
            target = fromDir.lookup(name)
            if isinstance(target, DEntry):
                self.deleteDirectory(name, fromDir)
                self.createDir(name, toDir)
            if isinstance(target, FCB):
                self.deleteFile(name, fromDir)
                self.createFile(name, toDir)



def MakeFSFromTree(fs, tree, root=None):
    '''
        utility function to make directory from tree
    '''
    if tree == ():
        return None
    if isinstance(tree, str):
        fs.createFile(name=tree, enclosingDir=root)
    elif tree[0][-1] == '/':
        if root is None:
            c = fs.root
            root = c
        else:
            # c = root.makeDir(tree[0][:-1])
            name = tree[0][:-1]
            c = fs.createDir(name, enclosingDir=root)
        if len(tree) > 1:
            for t in tree[1:]:
                MakeFSFromTree(fs, t, c)
    return root


if __name__ == '__main__':
    directoryTree = ( '/',  ('home/', ('u1/', 'hello.c', 'myfriend.h'),
                                    ('u2/', 'world.h'), 'homefiles'),
                            ('bin/', 'ls'),
                            ('etc/', ))

    # make an initial directory
    print('input directory tree=%s' % repr(directoryTree))

    fs = PFS(nBlocks = 16)
    root = MakeFSFromTree(fs, directoryTree)
    print('directory=%s' % repr(MakeTreeFromDir(root)))
    d, f = fs.parsePath('/home/u1/', root)
    print('last modification date for /home/u1/ is %s' %  d.modTime)
    time.sleep(5)
    fs.rename('hello.c', 'goodbye.py', d)
    print('after renaming=%s' % repr(MakeTreeFromDir(root)))
    print('last modification date for /home/u1/ is %s' %  d.modTime)
    t, f = fs.parsePath('/home/u2/', root)
    fs.move('myfriend.h', d, t) # from /home/u1 to /home/u2
    print('after moving=%s' % repr(MakeTreeFromDir(root)))
    fs.move('etc', root, d)  # move /etc to /home/u1
    print('after moving=%s' % repr(MakeTreeFromDir(root)))

