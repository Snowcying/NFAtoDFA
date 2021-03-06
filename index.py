import re
import sys
import operator
from graphviz import Digraph
import construct

dot = Digraph(comment='NFAtoDFA', format="png")
dot2 = Digraph(comment='minDFA', format="png")

# import networkx
# import matplotlib.pyplot as plt

# NFAtoDFA
class NFAgraph():
  def __init__(self,NFA = {},start = [],end = []):
    self.NFA = NFA
    self.start = start
    self.end = end

class DFAgraph():
  def __init__(self,DFA = {},start = [],end = []):
    self.DFA = DFA
    self.start = start
    self.end = end


#######################  在这里输入正规文法
temp = construct.expression('b((ab)*|bb)*ab')
# temp = construct.expression('b((ab)*|bb)*ab')
#######################
gra = construct.calculate(temp)

def createNFAgraph():
  return gra.dic
  # p50 3.6
  # return {'0':{'null':['1','7'],'a':[],'b':[]},
  #         '1':{'null':['2','4'],'a':[],'b':[]},
  #         '2':{'null':[],'a':['3'],'b':[]},
  #         '3':{'null':['6'],'a':[],'b':[]},
  #         '4':{'null':[],'a':[],'b':['5']},
  #         '5':{'null':['6'],'a':[],'b':[]},
  #         '6':{'null':['1','7'],'a':[],'b':[]},
  #         '7':{'null':[],'a':['8'],'b':[]},
  #         '8':{'null':[],'a':[],'b':['9']},
  #         '9':{'null':[],'a':[],'b':['10']},
  #         '10':{'null':[],'a':[],'b':[]}
  # }
  # return { 0 :{ 'null' :[], 'a' :[1], 'b' :[6]},
  #          1 :{ 'null' :[], 'a' :[1], 'b' :[2,7]},
  #          2 :{ 'null' :[], 'a' :[6], 'b' :[3]},
  #          3 :{ 'null' :[], 'a' :[1], 'b' :[2]},
  #          4 :{ 'null' :[], 'a' :[2], 'b' :[5]},
  #          5 :{ 'null' :[], 'a' :[4], 'b' :[3,7]},
  #          6 :{ 'null' :[], 'a' :[6], 'b' :[3,7]},
  #          7 :{ 'null' :[], 'a' :[  ], 'b' :[]},
  # }
  # 0 1 2 3 4 5 6 7 8 9 10
  # A B C D E F G H I J H
  # return {'A':{'null':['B','I'],'a':[],'b':[]},
  #         'B':{'null':['C','E'],'a':[],'b':[]},
  #         'C':{'null':[],'a':['D'],'b':[]},
  #         'D':{'null':[],'a':[],'b':['C']},
  #         'E':{'null':[],'a':[],'b':['F']},
  #         'F':{'null':[],'a':[],'b':['G']},
  #         'G':{'null':['H'],'a':[],'b':[]},
  #         'H':{'null':['B','I'],'a':['I'],'b':[]},
  #         'I':{'null':[],'a':['J'],'b':['J']},
  #         'J':{'null':[],'a':[],'b':['H']},
  #         'H':{'null':[],'a':[],'b':[]}
  # }
  # return {'S': {'null':[],'0':['V','Q'],'1':['Q','U']}, 'Q': {'null':[],'0':['V'],'1':['Q','U']}, 'V': {'null':[],'0':['Z'],'1':[]}, 
  # 'U': {'null':[],'0':[],'1':['Z']}, 'Z':{'null':[],'0':['Z'],'1':['Z']}}

  #  return {'0':{'null':[],'a':['0','1'],'b':['1']},
  #         '1':{'null':[],'a':['0'],'b':[]},
  # }

  # return {'0':{'null':[],'a':['1'],'b':['2']},
  #       '1':{'null':[],'a':['1'],'b':['4']},
  #       '2':{'null':[],'a':['1'],'b':['3']},
  #       '3':{'null':[],'a':['3'],'b':['2']},
  #       '4':{'null':[],'a':['0'],'b':['5']},
  #       '5':{'null':[],'a':['5'],'b':['4']},
  # }
  # a 1 b 0
  # return {0:{'null':[],'a':[1],'b':[]},
  #       1:{'null':[2,6,12],'a':[],'b':[]},
  #       2:{'null':[],'a':[3],'b':[]},
  #       3:{'null':[],'a':[],'b':[4]},
  #       4:{'null':[5],'a':[],'b':[]},
  #       5:{'null':[12],'a':[],'b':[5]},
  #       6:{'null':[],'a':[7],'b':[]},
  #       7:{'null':[10],'a':[],'b':[8]},
  #       8:{'null':[],'a':[9],'b':[]},
  #       9:{'null':[],'a':[],'b':[10]},
  #       10:{'null':[7],'a':[11],'b':[]},
  #       11:{'null':[12],'a':[],'b':[]},
  #       12:{'null':[],'a':[],'b':[13]},
  #       13:{'null':[],'a':[],'b':[]},
  # }
  # return {'X':{'null':[],'a':[],'b':['A']},
  #       'A':{'null':['B','F','L'],'a':[],'b':[]},
  #       'B':{'null':[],'a':[],'b':['C']},
  #       'C':{'null':[],'a':['D'],'b':[]},
  #       'D':{'null':[],'a':[],'b':['E']},
  #       'E':{'null':['L'],'a':['E'],'b':[]},
  #       'F':{'null':[],'a':[],'b':['G']},
  #       'G':{'null':['J'],'a':['H'],'b':[]},
  #       'H':{'null':[],'a':[],'b':['I']},
  #       'I':{'null':[],'a':['J'],'b':[]},
  #       'J':{'null':['G'],'a':[],'b':['K']},
  #       'K':{'null':['L'],'a':[],'b':[]},
  #       'L':{'null':['A'],'a':['Y'],'b':[]},
  #       'Y':{'null':[],'a':[],'b':[]},
  # }
  # 64 3t
  # return{
  #   0:{'null':[],'a':[1,2],'b':[2,3]},
  #   1:{'null':[],'a':[4],'b':[]},
  #   2:{'null':[],'a':[1],'b':[2,3]},
  #   3:{'null':[],'a':[],'b':[4]},
  #   4:{'null':[],'a':[4],'b':[4]},
  # }
  # 65 4t b
  # return{
  #   0:{'null':[],'a':[1],'b':[2]},
  #   1:{'null':[],'a':[1],'b':[4]},
  #   2:{'null':[],'a':[1],'b':[3]},
  #   3:{'null':[],'a':[3],'b':[2]},
  #   4:{'null':[],'a':[0],'b':[5]},
  #   5:{'null':[],'a':[5],'b':[4]},
  # }
  # 65 7t 
  # return{
  #   0:{'null':[],'a':[1],'b':[6]},
  #   1:{'null':[],'a':[1],'b':[2,7]},
  #   2:{'null':[],'a':[6],'b':[3]},
  #   3:{'null':[],'a':[1],'b':[2]},
  #   4:{'null':[],'a':[2],'b':[5]},
  #   5:{'null':[],'a':[4],'b':[3,7]},
  #   6:{'null':[],'a':[6],'b':[3,7]},
  #   7:{'null':[],'a':[],'b':[]},
  # }
NFA1 = NFAgraph(createNFAgraph(),gra.start,gra.end)
# NFA1 = NFAgraph(createNFAgraph(),[0],[10])
graph = NFA1.NFA

def getRoads(gra):
  for key in gra:
    ans = []
    for road in gra[key]:
      ans.append(road)
    if 'null' in ans:
      ans.remove('null')
    return strsort(ans)

def getStartEnd():
  keys = []
  for x in graph:
    keys.append(x)
  return [keys[0],keys[-1]]

def closure(list):
  ans = []
  hadFind = []
  for x in list:
    findClosure(x,ans,hadFind)
  return ans

def notExist(x,ans):
  if ans.count(x) == 0:
    return True
  else:
    return False

def findClosure(x,ans,hadFind):
  if notExist(x,hadFind):
    if graph[x]['null'] == []:
      appendNoRepeat(x,ans)
      hadFind.append(x)
    elif graph[x]['null'] != []  :
      nextNodes = graph[x]['null']
      appendNoRepeat(x,ans)
      hadFind.append(x)
      for node in nextNodes:
        appendNoRepeat(node,ans)
        findClosure(node,ans,hadFind)

def findClosureTerm(x,ans,hadFind):
  if notExist(x,hadFind):
    if graph[x]['null'] == []:
      appendNoRepeat(x,ans)
      hadFind.append(x)
    else:
      nodes = graph[x]['null']
      hadFind.append(x)
      for node in nodes:
        findClosureTerm(node,ans,hadFind)
      

def move(list,road,gra = graph):
  ans = []
  for x in list:
    getTerm(x,road,ans,gra)
  return ans

def getTerm(x,road,ans,gra = graph):
  if gra[x][road] != []:
    nodes = gra[x][road]
    for node in nodes:
      appendNoRepeat(node,ans)
    return
  elif 'null' in gra[x]:
    if gra[x]['null'] != []:
      terms = []
      hadFind = []
      findClosureTerm(x,terms,hadFind)
      for term in terms:
        termRoads = gra[term][road]
        for termRoad in termRoads:
          appendNoRepeat(termRoad,ans)
  else:
    return

def appendNoRepeat(x,ans):
  if notExist(x,ans):
    ans.append(x)
    temp = strsort(ans)
    ans = temp
    

def sort_key(s):
    if s:
        try:
            c = re.findall(r'^\d+', s)[0]
        except:
            c = -1
        return int(c)

def strsort(alist):

  if alist == []:
    return []

  if isinstance(alist[0],str):
    if alist[0].isdigit():  
      alist.sort(key=sort_key)
      return alist
    else:
      temp = sorted(alist)
      return temp
  else:
    temp = sorted(alist)
    return temp

def cmpList(x,lists):
  flag = False
  for list in lists:
    if(operator.eq(list,x)):
      flag = True
  return flag

def DFS(x,ans):
  if cmpList(x,ans):
    return
  else:
    roads = getRoads(graph)
    ans.append(x)
    for road in roads:
      t = closureMove(x,road)
      if t == []:
        return
      DFS(t,ans)

def BFS(x,ans):
  ans.append(x)
  roads = getRoads(graph)
  head = 0
  rear = 1
  while head != rear:
    for road in roads:
      t = closureMove(ans[head],road)
      if not cmpList(t,ans):
        if t != []:
          ans.append(t)
          rear = rear + 1
    head = head + 1

def closureMove(list,road):
  return strsort(closure(move(list,road)))

def getFirstNode():
  for node in graph:
    return node

def indexLabel(index):
  start = NFA1.start[0]
  if isinstance(start,int):
    return str(index)
  else:  
    if start.isdigit():
      numList = list(map(chr, range(ord('0'), ord('9') + 1)))
      return numList[index]
    elif start.isalpha():
      letterList = list(map(chr, range(ord('A'), ord('Z') + 1)))
      return letterList[index]

def newTerm(ends,list):
  for end in ends:
    if not notExist(end,list):
      return True
  return False

def draw(ans,end):
  roads = getRoads(graph)
  # dot.node('start','start')
  for x in ans:
    index = ans.index(x)
    if newTerm(end,x):
      dot.node(indexLabel(index),indexLabel(index),color='red')
    else:
      dot.node(indexLabel(index),indexLabel(index))
    for road in roads:
      nextNode = closureMove(x,road)
      if nextNode != []:
        nextNodeIndex = ans.index(nextNode)
        dot.edge(indexLabel(index),indexLabel(nextNodeIndex),road)
  dot.edge('',indexLabel(0),'start')
  dot.render('NFAtoDFA.gv', view=True)

def createNewgraph(ans,DFA):
  newGraph = {}
  roads = getRoads(graph)
  endNFA = NFA1.end
  endDFA = []
  for x in ans:
    index = ans.index(x)
    label = indexLabel(index)
    newGraph[label] = {}
    dictGraph = newGraph[label]
    if newTerm(endNFA,x):
      endDFA.append(indexLabel(index))
    for road in roads:
      nextNode = closureMove(x,road)
      if nextNode != []:
        nextNodeIndex = indexLabel(ans.index(nextNode))
        dictGraph[road] = [nextNodeIndex]
      else:
        dictGraph[road] = []
  DFA.DFA = newGraph
  DFA.end = endDFA
  DFA.start = [str(indexLabel(0))]

class Group:
  def __init__(self,list = [],certain = False):
    self.list = list
    self.certain = certain

def nextNode(graphDFA,node,road):
  # print(graphDFA,node,road)
  if graphDFA[node][road] != []:
    return graphDFA[node][road][0]
  else:
    return []

def nextNodes(graphDFA,node):
  roads = getRoads(graph)
  nodes = []
  for road in roads:
    if nextNode(graphDFA,node,road) != []:
      nodes.append(nextNode(graphDFA,node,road))
  return nodes

def sameGroup(groups,list1,list2):
  if len(list1) != len(list2):
    return False
  for x in range(len(list1)):
    list1Node = list1[x]
    list2Node = list2[x]
    if findNode(groups,list1Node) != findNode(groups,list2Node):
      return False
  return True

def groupCertain(groups,list1,graphDFA):
  roads = getRoads(graph)
  for road in roads:
    groupList = []
    for x in list1:
      groupList.append(findNode(groups,nextNode(graphDFA,x,road)))
    for g1 in groupList:
      for g2 in groupList:
        if g2 != g1:
         return False
  return True


def findNode(groups,x):
  for group in groups:
    if not notExist(x,group):
      return group

def allGroupCertain(groups):
  for group in groups:
    if group.certain == False:
      return False
  return True


def minDFA(DFA):
  DFAgraph = DFA.DFA
  group1 = DFA.end
  group2 = []
  groups = [group1,group2]
  for x in DFAgraph:
    if notExist(x,group1):
      group2.append(x)
  print('g:',groups)
  while 1:
    oldgroups = groups.copy()
    for group in oldgroups:
      if len(group) != 1:
        listOne = group[0]
        listOneNextNodes = nextNodes(DFAgraph,listOne)
        glist1 = []
        glist2 = []
        glist1.append(listOne)
        for x in group:
          if x != listOne:
            listNextNodes = nextNodes(DFAgraph,x)
            if sameGroup(oldgroups,listOneNextNodes,listNextNodes):
              glist1.append(x)
            else:
              glist2.append(x)
        if glist2 != []:
          groups.append(glist1)
          groups.append(glist2)
          groups.remove(group)

    if oldgroups == groups:
      return groups
    print('g:',groups)


def minIndex(list,graphList):
  for x in list:
    for y in graphList:
      if not notExist(x,y):
        return graphList.index(y)

def drawMinDFA(min,DFA):
  graphDic = DFA.DFA
  roads = getRoads(graphDic)

  for x in min:
    if newTerm(DFA.end,x):
      dot2.node(x[0],x[0],color='red')
    else:
      dot2.node(x[0],x[0])
    for road in roads:
      nodes = move(x,road,graphDic)
      nextNodes = strsort(nodes)
      if nextNodes != []:
        nextNodeIndex = minIndex(nextNodes,min)
        dot2.edge(x[0],min[nextNodeIndex][0],road)
  dot2.edge('',indexLabel(0),'start')
  dot2.render('minDFA.gv', view=True)

if __name__ == '__main__':

  # t0 = closure([0])
  t0 = closure(gra.start)
  ans = []
  print(t0)
  BFS(t0,ans)
  print('DFA',ans)
  draw(ans,NFA1.end)

  DFA1 = DFAgraph()
  createNewgraph(ans,DFA1)

  min = minDFA(DFA1)
  print('minDFA: ',min)
  drawMinDFA(min,DFA1)
