# this is template code for graph and DFS

class Graph:
   def __init__(self, G):
      '''
          G is a dictionary of adjacency list that maps each vertex u (string)
          to a list of vertices v (so (u, v) is an edge)
      '''
      self.G = G
      self.vertices = list(G.keys())

   def Adj(self, v):
      '''iterator for the adjacency list'''
      for i in self.G[v]:
         yield i

   def V(self):
      '''iterator for the vertices'''
      for i in self.vertices:
         yield i

   def findCycle(self):
      '''
         your code to return a list of vertice that form a cycle
         by calling a modified version of DFS or some other algorithm.
      '''
      #cycle_record = DFS(self)
      DFS(self)
      if len(self.cycle_record) > 0:
            # print one cycle
            # as begin
            cycle_list = list(self.cycle_record[0])
            cycle_order = [cycle_list[0]]
            cycle_queue = [self.cycle_record[0][cycle_list[0]]]
            while(cycle_queue[0]!=cycle_order[0]):
                  nextnode = cycle_queue.pop()
                  cycle_order.append(nextnode)
                  cycle_queue.append(self.cycle_record[0][nextnode])
            cycle_order.append(cycle_queue[0])
            return cycle_order
      else:
            return None # return None for now but you should return list


### Code for DFS ###
# you may want to adopt it into the Graph class or keep it as separate code.

WHITE = 'white'
GRAY =  'gray'
BLACK = 'black'


def DFS(G):
   G.color = {} # color, which is WHITE, GRAY, or BLACK
   G.pred = {}  # the predecessor
   # you may add your own field for tracking cycles
   G.cycle_record = []

   for u in G.V():
      G.color[u] = WHITE
      G.pred[u] = None
   for u in G.V():
      if G.color[u] == WHITE:
         DFSVisit(G, u)

def DFSVisit(G, u):
   G.color[u] = GRAY
   for v in G.Adj(u):
      if G.color[v] == WHITE:
         G.pred[v] = u
         DFSVisit(G, v)
         
      # add your own code for cycle detection
      if G.color[v] == GRAY: 
         G.pred[v] = u
         G.cycle_record.append( { G.pred[v]: v for v in G.pred if G.pred[v]!=None and G.color[v]==GRAY})
         G.pred = {v: None for v in G.V()}

   G.color[u] = BLACK # RUNNED

# our test case. Define a dictionary of adjacency lists for each vertex.

if __name__ == '__main__':
   L = [
        {'P1':['R1'], 'P2':['R3', 'R4', 'R5'], 'P3': ['R5'], 'P4': ['R2'],
         'P5': [], 'R1':['P2'], 'R2': ['P1'], 'R3': ['P5'], 'R4': ['P3'], 
         'R5': ['P4'] },
        {'P1': ['P2'], 'P2': ['P3', 'P4', 'P5'], 'P3':['P4'], 
         'P4': ['P1'], 'P5': [] },
        ]

   for g in map(Graph, L):
      print('g=%s, cycle=%s' % (g.G, g.findCycle()))
