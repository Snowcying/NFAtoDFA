import construct
import re
import operator
from graphviz import Digraph

class NFAgraph():
    def __init__(self, NFA={}, start=[], end=[]):
        self.NFA = NFA
        self.start = start
        self.end = end


class DFAgraph():
    def __init__(self, DFA={}, start=[], end=[]):
        self.DFA = DFA
        self.start = start
        self.end = end

def closure(list,graph):
    ans = []
    hadFind = []
    for x in list:
        findClosure(x, ans, hadFind,graph)
    return ans

def notExist(x, ans):
    if ans.count(x) == 0:
        return True
    else:
        return False

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

    if isinstance(alist[0], str):
        if alist[0].isdigit():
            alist.sort(key=sort_key)
            return alist
        else:
            temp = sorted(alist)
            return temp
    else:
        temp = sorted(alist)
        return temp

def appendNoRepeat(x, ans):
    if notExist(x, ans):
        ans.append(x)
        temp = strsort(ans)
        ans = temp

def findClosure(x, ans, hadFind,graph):
    if notExist(x, hadFind):
        if graph[x]['null'] == []:
            appendNoRepeat(x, ans)
            hadFind.append(x)
        elif graph[x]['null'] != []:
            nextNodes = graph[x]['null']
            appendNoRepeat(x, ans)
            hadFind.append(x)
            for node in nextNodes:
                appendNoRepeat(node, ans)
                findClosure(node, ans, hadFind,graph)

def getRoads(gra):
    for key in gra:
        ans = []
        for road in gra[key]:
            ans.append(road)
        if 'null' in ans:
            ans.remove('null')
        return strsort(ans)

def findClosureTerm(x, ans, hadFind,graph):
    if notExist(x, hadFind):
        if graph[x]['null'] == []:
            appendNoRepeat(x, ans)
            hadFind.append(x)
        else:
            nodes = graph[x]['null']
            hadFind.append(x)
            for node in nodes:
                findClosureTerm(node, ans, hadFind,graph)

def getTerm(x, road, ans, gra):
    if gra[x][road] != []:
        nodes = gra[x][road]
        for node in nodes:
            appendNoRepeat(node, ans)
        return
    elif 'null' in gra[x]:
        if gra[x]['null'] != []:
            terms = []
            hadFind = []
            findClosureTerm(x, terms, hadFind,gra)
            for term in terms:
                termRoads = gra[term][road]
                for termRoad in termRoads:
                    appendNoRepeat(termRoad, ans)
    else:
        return

def move(list, road, gra):
    ans = []
    for x in list:
        getTerm(x, road, ans, gra)
    return ans

def cmpList(x, lists):
    flag = False
    for list in lists:
        if (operator.eq(list, x)):
            flag = True
    return flag

def closureMove(list, road,gra):
    return strsort(closure(move(list, road,gra),gra))

def BFS(x, ans,graph):
    ans.append(x)
    roads = getRoads(graph)
    head = 0
    rear = 1
    while head != rear:
        for road in roads:
            # t = closureMove(ans[head], road)
            t = closureMove(ans[head], road,graph)
            if not cmpList(t, ans):
                if t != []:
                    ans.append(t)
                    rear = rear + 1
        head = head + 1

def indexLabel(index,start):
    # start = NFA1.start[0]
    if isinstance(start, int):
        return str(index)
    else:
        if start.isdigit():
            numList = list(map(chr, range(ord('0'), ord('9') + 1)))
            return numList[index]
        elif start.isalpha():
            letterList = list(map(chr, range(ord('A'), ord('Z') + 1)))
            return letterList[index]

def newTerm(ends, list):
    for end in ends:
        if not notExist(end, list):
            return True
    return False

def createNewgraph(ans, DFA,NFA1):
    newGraph = {}
    graph = NFA1.NFA
    start = NFA1.start[0]
    roads = getRoads(graph)
    endNFA = NFA1.end
    endDFA = []
    for x in ans:
        index = ans.index(x)
        label = indexLabel(index,start)
        newGraph[label] = {}
        dictGraph = newGraph[label]
        if newTerm(endNFA, x):
            endDFA.append(indexLabel(index,start))
        for road in roads:
            nextNode = closureMove(x, road,graph)
            if nextNode != []:
                nextNodeIndex = indexLabel(ans.index(nextNode),start)
                dictGraph[road] = [nextNodeIndex]
            else:
                dictGraph[road] = []
    DFA.DFA = newGraph
    DFA.end = endDFA
    DFA.start = [str(indexLabel(0,start))]

def nextNode(graphDFA, node, road):
    # print(graphDFA,node,road)
    if graphDFA[node][road] != []:
        return graphDFA[node][road][0]
    else:
        return []

def nextNodes(graphDFA, node,graph):
    roads = getRoads(graph)
    nodes = []
    for road in roads:
        if nextNode(graphDFA, node, road) != []:
            nodes.append(nextNode(graphDFA, node, road))
    return nodes

def findNode(groups, x):
    for group in groups:
        if not notExist(x, group):
            return group


def sameGroup(groups, list1, list2):
    if len(list1) != len(list2):
        return False
    for x in range(len(list1)):
        list1Node = list1[x]
        list2Node = list2[x]
        if findNode(groups, list1Node) != findNode(groups, list2Node):
            return False
    return True

def minDFA(DFA,graph):
    DFAgraph = DFA.DFA
    group1 = DFA.end
    group2 = []
    groups = [group1, group2]
    for x in DFAgraph:
        if notExist(x, group1):
            group2.append(x)
    # print('g:', groups)
    while 1:
        oldgroups = groups.copy()
        for group in oldgroups:
            if len(group) != 1:
                listOne = group[0]
                listOneNextNodes = nextNodes(DFAgraph, listOne,graph)
                glist1 = []
                glist2 = []
                glist1.append(listOne)
                for x in group:
                    if x != listOne:
                        listNextNodes = nextNodes(DFAgraph, x,graph)
                        if sameGroup(oldgroups, listOneNextNodes, listNextNodes):
                            glist1.append(x)
                        else:
                            glist2.append(x)
                if glist2 != []:
                    groups.append(glist1)
                    groups.append(glist2)
                    groups.remove(group)

        if oldgroups == groups:
            return groups
        # print('g:', groups)

def minIndex(list, graphList):
    for x in list:
        for y in graphList:
            if not notExist(x, y):
                return graphList.index(y)

def minDFAArray(min, DFA):
    graphDic = DFA.DFA
    roads = getRoads(graphDic)
    g2 = [["" for j in range(100)] for i in range(100)]
    for x in min:
        for road in roads:
            nodes = move(x, road, graphDic)
            nextNodes = strsort(nodes)
            if nextNodes != []:
                nextNodeIndex = minIndex(nextNodes, min)
                x0=int(x[0])
                y0=int(min[nextNodeIndex][0])
                if g2[x0][y0]!="":
                    oldRoad = g2[x0][y0]
                    newRoad = oldRoad+road
                    g2[x0][y0]=newRoad
                else: g2[x0][y0]=road
    return g2
                # print(type(x[0]),type(min[nextNodeIndex][0]))

def isConnect(k1,p,end):
    start = 0
    tailIndex=0
    for k in k1:
        flag=0
        node = p[start]
        for index,n in  enumerate(node):
            if k in n:
                start=index
                tailIndex=index
                flag=1
                break;
        if flag==0:
            return False
    if int(tailIndex)==int(end):
        return True
    else:
        return False

def regexToDFAArray(regex):
    g1 = construct.calculate(construct.expression(regex))
    NFA1 = NFAgraph(g1.dic, g1.start, g1.end)
    NFAG = NFA1.NFA
    t0 = closure(g1.start, NFAG)
    ans = []
    BFS(t0, ans, NFAG)
    # print('DFA', ans)
    DFA1 = DFAgraph()
    createNewgraph(ans, DFA1, NFA1)

    min = minDFA(DFA1, NFAG)

    # print('minDFA: ', min)

    ret = minDFAArray(min, DFA1)
    return ret,DFA1.end[0]

def stringBelongRegex(testString,regex):
    ret,end=regexToDFAArray(regex)
    connectFlag=isConnect(testString, ret, end)
    return connectFlag

def stringBelongRegexByArray(testString,array,end):
    return isConnect(testString,array,end)

if __name__ == '__main__':
    # g1=construct.calculate(construct.expression('(const|char|procedure|begin|end)*(begin|end)'))
    # NFA1 = NFAgraph(g1.dic, g1.start, g1.end)
    # NFAG = NFA1.NFA
    # t0 = closure(g1.start,NFAG)
    # ans = []
    # BFS(t0, ans,NFAG)
    # # print('DFA', ans)
    # DFA1 = DFAgraph()
    # createNewgraph(ans, DFA1,NFAG)
    #
    # min = minDFA(DFA1,NFAG)
    # print('minDFA: ', min)
    # ret = minDFAArray(min,DFA1)
    # regex="(const|char|procedure|begin|end)*(begin|end)"
    # ret,end = regexToDFAArray(regex)
    # test1 = "babababb"
    # test2 = "constcharbeginendend"
    # test3 = "constconstconstend"
    # connectFlag=isConnect(test3, ret, end)
    # print("ret: ",connectFlag)

    regex = "(const|char|procedure|begin|end)*(begin|end)"
    test1 = "babababb"
    test2 = "constcharbeginendend"
    test3 = "constconstconstend"
    # res = stringBelongRegex(test3,regex)
    array,end=regexToDFAArray(regex)
    res = stringBelongRegexByArray(test3,array,end)
    print(res)