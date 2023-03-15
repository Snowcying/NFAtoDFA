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
    def __init__(self, NFA={}, start=[], end=[]):
        self.NFA = NFA
        self.start = start
        self.end = end


class DFAgraph():
    def __init__(self, DFA={}, start=[], end=[]):
        self.DFA = DFA
        self.start = start
        self.end = end


#######################  在这里输入正规文法
# temp = construct.expression('b((ab)*|bb)*abb')
temp = construct.expression('(const|char|procedure|begin|end)*(begin|end)')
# temp = construct.expression('9162*3abc')
##  babababb  bbbbbabb  9162222223abc
# temp = construct.expression('b((ab)*|bb)*ab')
#######################
gra = construct.calculate(temp)

print("gra: ", gra.dic)


NFA1 = NFAgraph(gra.dic, gra.start, gra.end)
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
    return [keys[0], keys[-1]]


def closure(list):
    ans = []
    hadFind = []
    for x in list:
        findClosure(x, ans, hadFind)
    return ans


def notExist(x, ans):
    if ans.count(x) == 0:
        return True
    else:
        return False


def findClosure(x, ans, hadFind):
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
                findClosure(node, ans, hadFind)


def findClosureTerm(x, ans, hadFind):
    if notExist(x, hadFind):
        if graph[x]['null'] == []:
            appendNoRepeat(x, ans)
            hadFind.append(x)
        else:
            nodes = graph[x]['null']
            hadFind.append(x)
            for node in nodes:
                findClosureTerm(node, ans, hadFind)


def move(list, road, gra=graph):
    ans = []
    for x in list:
        getTerm(x, road, ans, gra)
    return ans


def getTerm(x, road, ans, gra=graph):
    if gra[x][road] != []:
        nodes = gra[x][road]
        for node in nodes:
            appendNoRepeat(node, ans)
        return
    elif 'null' in gra[x]:
        if gra[x]['null'] != []:
            terms = []
            hadFind = []
            findClosureTerm(x, terms, hadFind)
            for term in terms:
                termRoads = gra[term][road]
                for termRoad in termRoads:
                    appendNoRepeat(termRoad, ans)
    else:
        return


def appendNoRepeat(x, ans):
    if notExist(x, ans):
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


def cmpList(x, lists):
    flag = False
    for list in lists:
        if (operator.eq(list, x)):
            flag = True
    return flag


def DFS(x, ans):
    if cmpList(x, ans):
        return
    else:
        roads = getRoads(graph)
        ans.append(x)
        for road in roads:
            t = closureMove(x, road)
            if t == []:
                return
            DFS(t, ans)


def BFS(x, ans):
    ans.append(x)
    roads = getRoads(graph)
    head = 0
    rear = 1
    while head != rear:
        for road in roads:
            t = closureMove(ans[head], road)
            if not cmpList(t, ans):
                if t != []:
                    ans.append(t)
                    rear = rear + 1
        head = head + 1


def closureMove(list, road):
    return strsort(closure(move(list, road)))


def getFirstNode():
    for node in graph:
        return node


def indexLabel(index):
    start = NFA1.start[0]
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


def draw(ans, end):
    roads = getRoads(graph)
    # dot.node('start','start')
    for x in ans:
        index = ans.index(x)
        if newTerm(end, x):
            dot.node(indexLabel(index), indexLabel(index), color='red')
        else:
            dot.node(indexLabel(index), indexLabel(index))
        for road in roads:
            nextNode = closureMove(x, road)
            if nextNode != []:
                nextNodeIndex = ans.index(nextNode)
                dot.edge(indexLabel(index), indexLabel(nextNodeIndex), road)
    dot.edge('', indexLabel(0), 'start')
    dot.render('NFAtoDFA.gv', view=True)


def createNewgraph(ans, DFA):
    newGraph = {}
    roads = getRoads(graph)
    endNFA = NFA1.end
    endDFA = []
    for x in ans:
        index = ans.index(x)
        label = indexLabel(index)
        newGraph[label] = {}
        dictGraph = newGraph[label]
        if newTerm(endNFA, x):
            endDFA.append(indexLabel(index))
        for road in roads:
            nextNode = closureMove(x, road)
            if nextNode != []:
                nextNodeIndex = indexLabel(ans.index(nextNode))
                dictGraph[road] = [nextNodeIndex]
            else:
                dictGraph[road] = []
    DFA.DFA = newGraph
    DFA.end = endDFA
    DFA.start = [str(indexLabel(0))]


class Group:
    def __init__(self, list=[], certain=False):
        self.list = list
        self.certain = certain


def nextNode(graphDFA, node, road):
    # print(graphDFA,node,road)
    if graphDFA[node][road] != []:
        return graphDFA[node][road][0]
    else:
        return []


def nextNodes(graphDFA, node):
    roads = getRoads(graph)
    nodes = []
    for road in roads:
        if nextNode(graphDFA, node, road) != []:
            nodes.append(nextNode(graphDFA, node, road))
    return nodes


def sameGroup(groups, list1, list2):
    if len(list1) != len(list2):
        return False
    for x in range(len(list1)):
        list1Node = list1[x]
        list2Node = list2[x]
        if findNode(groups, list1Node) != findNode(groups, list2Node):
            return False
    return True


def groupCertain(groups, list1, graphDFA):
    roads = getRoads(graph)
    for road in roads:
        groupList = []
        for x in list1:
            groupList.append(findNode(groups, nextNode(graphDFA, x, road)))
        for g1 in groupList:
            for g2 in groupList:
                if g2 != g1:
                    return False
    return True


def findNode(groups, x):
    for group in groups:
        if not notExist(x, group):
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
    groups = [group1, group2]
    for x in DFAgraph:
        if notExist(x, group1):
            group2.append(x)
    print('g:', groups)
    while 1:
        oldgroups = groups.copy()
        for group in oldgroups:
            if len(group) != 1:
                listOne = group[0]
                listOneNextNodes = nextNodes(DFAgraph, listOne)
                glist1 = []
                glist2 = []
                glist1.append(listOne)
                for x in group:
                    if x != listOne:
                        listNextNodes = nextNodes(DFAgraph, x)
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
        print('g:', groups)


def minIndex(list, graphList):
    for x in list:
        for y in graphList:
            if not notExist(x, y):
                return graphList.index(y)


g1=[["" for j in range(100)]for i in range(100)]


def drawMinDFA(min, DFA):
    graphDic = DFA.DFA
    roads = getRoads(graphDic)

    for x in min:
        if newTerm(DFA.end, x):
            dot2.node(x[0], x[0], color='red')

            x0=int(x[0])
            end = x0
            # g1[x0][x0]=0
        else:
            dot2.node(x[0], x[0])
            # g1[x0][x0] = 0
        for road in roads:
            nodes = move(x, road, graphDic)
            nextNodes = strsort(nodes)
            if nextNodes != []:
                nextNodeIndex = minIndex(nextNodes, min)
                dot2.edge(x[0], min[nextNodeIndex][0], road)
                # g1[x[0],int(min[nextNodeIndex][0])]=1
                x0=int(x[0])
                y0=int(min[nextNodeIndex][0])
                if g1[x0][y0]!="":
                    oldRoad = g1[x0][y0]
                    newRoad = oldRoad+road
                    g1[x0][y0]=newRoad
                else: g1[x0][y0]=road
                # print(type(x[0]),type(min[nextNodeIndex][0]))



    dot2.edge('', indexLabel(0), 'start')
    dot2.render('minDFA.gv', view=True)


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


if __name__ == '__main__':
    # t0 = closure([0])
# [['13', '19'], ['0', '16', '20', '25'], ['2'], ['8', '15'], ['11', '17', '24'], ['3', '10'], ['6', '12', '23'], ['5'], ['7', '22'], ['18'], ['1'], ['21'], ['14'], ['4'], ['9']]

    t0 = closure(gra.start)
    ans = []
    print(t0)
    BFS(t0, ans)
    print('DFA', ans)
    draw(ans, NFA1.end)

    DFA1 = DFAgraph()
    createNewgraph(ans, DFA1)

    min = minDFA(DFA1)
    print('minDFA: ', min)
    drawMinDFA(min, DFA1)

    # print(g1)

    # for x in g1:
    #     print(x)
    # p b((ab)*|bb)*abb
    # p (const|char|procedure|begin|end)*(begin|end)
    test1 = "babababb"
    test2 = "constcharbeginendend"
    # test3= "9162222223abc"
    end = DFA1.end[0]
    print(isConnect(test2,g1,end))
    # for c in test1: