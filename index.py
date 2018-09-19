import re
import sys
import operator
from graphviz import Digraph

dot = Digraph(comment='NFAtoDFA', format="png")

# import networkx
# import matplotlib.pyplot as plt

# NFAtoDFA


def createDFAgraph():
  return {'0':{'null':['1','7'],'a':[],'b':[]},
          '1':{'null':['2','4'],'a':[],'b':[]},
          '2':{'null':[],'a':['3'],'b':[]},
          '3':{'null':['6'],'a':[],'b':[]},
          '4':{'null':[],'a':[],'b':['5']},
          '5':{'null':['6'],'a':[],'b':[]},
          '6':{'null':['1','7'],'a':[],'b':[]},
          '7':{'null':[],'a':['8'],'b':[]},
          '8':{'null':[],'a':[],'b':['9']},
          '9':{'null':[],'a':[],'b':['10']},
          '10':{'null':[],'a':[],'b':[]}
  }
  # return {'S': {'null':[],'0':['V','Q'],'1':['Q','U']}, 'Q': {'null':[],'0':['V'],'1':['Q','U']}, 'V': {'null':[],'0':['Z'],'1':[]}, 
  # 'U': {'null':[],'0':[],'1':['Z']}, 'Z':{'null':[],'0':['Z'],'1':['Z']}}

graph = createDFAgraph()

def getRoads():
  for key in graph:
    ans = []
    for road in graph[key]:
      ans.append(road)
    ans.remove('null')
    return strsort(ans)

def getStartEnd():
  keys = []
  for x in graph:
    keys.append(x)
  return [keys[0],keys[-1]]

def closure(list):
  ans = []
  for x in list:
    findClosure(x,ans)
  return ans

def notExist(x,ans):
  if ans.count(x) == 0:
    return True
  else:
    return False

def findClosure(x,ans):
  if graph[x]['null'] == []:
    appendNoRepeat(x,ans)
  else:
    nextNodes = graph[x]['null']
    appendNoRepeat(x,ans)
    for node in nextNodes:
      appendNoRepeat(node,ans)
      findClosure(node,ans)

def findClosureTerm(x,ans):
    if graph[x]['null'] == []:
      appendNoRepeat(x,ans)
    else:
      nodes = graph[x]['null']
      for node in nodes:
        findClosureTerm(node,ans)
      

def move(list,road):
  ans = []
  for x in list:
    getTerm(x,road,ans)
  return ans

def getTerm(x,road,ans):
  if graph[x][road] != []:
    nodes = graph[x][road]
    for node in nodes:
      appendNoRepeat(node,ans)
    return
  elif graph[x]['null'] != []:
    terms = []
    findClosureTerm(x,terms)
    for term in terms:
      termRoads = graph[term][road]
      for termRoad in termRoads:
        appendNoRepeat(termRoad,ans)
  else:
    return

def appendNoRepeat(x,ans):
  if notExist(x,ans):
    ans.append(x)
    strsort(ans)

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

  if alist[0].isdigit():  
    alist.sort(key=sort_key)
    return alist
  else:
    return sorted(alist)

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
    roads = getRoads()
    ans.append(x)
    for road in roads:
      t = closureMove(x,road)
      if t == []:
        return
      DFS(t,ans)

def BFS(x,ans):
  ans.append(x)
  roads = getRoads()
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
  startEnd = getStartEnd()
  start = startEnd[0]
  if start.isdigit():
    numList = list(map(chr, range(ord('0'), ord('9') + 1)))
    return numList[index]
  elif start.isalpha():
    letterList = list(map(chr, range(ord('A'), ord('Z') + 1)))
    return letterList[index]

def draw(ans):
  roads = getRoads()
  startEnd = getStartEnd()
  # start = startEnd[0]
  end = startEnd[1]
  dot.node('start','start')
  for x in ans:
    index = ans.index(x)
    if not notExist(end,x):
      dot.node(indexLabel(index),indexLabel(index),color='red')
    else:
      dot.node(indexLabel(index),indexLabel(index))
    for road in roads:
      nextNode = closureMove(x,road)
      if nextNode != []:
        print(x,nextNode,road)
        nextNodeIndex = ans.index(nextNode)
        dot.edge(indexLabel(index),indexLabel(nextNodeIndex),road)
  dot.edge('start',indexLabel(0),'start')
  dot.view()
      

if __name__ == '__main__':

  t0 = closure(getFirstNode())
  ans = []
  BFS(t0,ans)
  print(ans)
  draw(ans)
