import operator
 
opMap = {'+':operator.add,'-':operator.sub,"/":operator.truediv,"*":operator.mul}
proMap = {'(':100,'+':3,'-':3,'*':10,'/':8,')':1,'#':0,'|':3,'$':8}

#获取下个操作数
def getNext(leftExpress):
    t = leftExpress[0:1]
    if t.isnumeric():
        for s in leftExpress[1:]:
            if not s.isnumeric():
                break
            else:
                t += s
        return t
 
    else:
        return t
 
def popStack():
    while opStack[-1] != '(':
        nStack.append(opStack.pop())
    opStack.pop()
 
def popStack2(s):
    pro1 = proMap[s]
    for i in range(len(opStack)):
        op = opStack[-1]
        if op == '(':
            opStack.append(s)
            break
        else:
            pro0 = proMap[op]
            if pro0 < pro1:
                opStack.append(s)
                break
            else:
                nStack.append(opStack.pop())
 
def dealwith(s):
    if s.isalpha():
        nStack.append(s)
    elif s.isnumeric():
        nStack.append(s)
    elif s == '(':
        opStack.append(s)
    elif s == ')':
        popStack()
    elif opStack[-1] == '(':
        opStack.append(s)
    else:
        op = opStack[-1]
        pro0 = proMap[op]
        pro1 = proMap[s]
        if pro1 > pro0:
            opStack.append(s)
        else:
            popStack2(s)
 
def meger():            
    while len(opStack) > 1:
        nStack.append(opStack.pop())
 
 
# express = '9+2*3'
# express = '(a|b)*abb'
opStack = ['#']
nStack = []
def expression(str):
    strlist = splitStr(str)
    express = parse(strlist)
    i = 0
    l = len(express)
    while i < l:
        token = getNext(express[i:])
        dealwith(token)
        i+=len(token)
    meger()
    return nStack
 
def splitStr(str):
  ans = []
  for x in str:
    ans.append(x)
  return ans

def nextLetter(list,index):
  nextIndex = index + 1
  return list[nextIndex]


def parse(strlist):
  print('str',strlist)
  ans = []
  strlist.append(' ')
  index = -1
  for x in strlist:
    index = index + 1
    if x != ' ':
      aim = x
      nextLe = nextLetter(strlist,index)
      if (x.isalpha() and nextLe.isalpha()) or (x.isalpha() and nextLe == '(') :
        aim = aim + '$'
      elif x == '*' and (nextLe.isalpha() or nextLe == '|' or nextLe == '('):
        aim = aim + '1$'
      elif x == '*' and nextLe == ' ':
        aim = aim + '1'
      elif x == ')' and nextLe.isalpha():
        aim = aim + '$'
      
      ans.append(aim)
  out = ''.join(ans)
  print('strAf',out)
  return out

def isOperator(op):
  if op == '$' or op == '|' or op == '*':
    return True
  else:
    return False

def calculate(ex):
  print('start')
  num = len(ex)
  i = 0
  while num > 1:
    c = ex[i]
    if isOperator(c):
      x = ex[i-2]
      y = ex[i-1]
      res = construct(x,y,c)
      ex[i] = res
      ex.remove(x)
      ex.remove(y)
      i = 0
    else:
      i = i + 1
    num = len(ex)
  # print('ex',ex[0].dic)
  return ex[0]

class graph():
  def __init__(self,dic={},start=[],end=[]):
    self.dic = dic
    self.start = start
    self.end = end

indexNum = 0

def initDic():
  dic = {'null':[]}
  letterList = list(map(chr, range(ord('a'), ord('b') + 1)))
  for letter in letterList:
    dic[letter] = []
  return dic 

def construct(x,y,op):
  global indexNum
  # print('construct')
  dic = {}
  g1 = graph()
  if op == '$':
    # a$a
    if isinstance(x,str) and isinstance(y,str):
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1
      dic[str(indexNum)] = initDic()
      dic[str(indexNum-2)][x].append(str(indexNum-1))
      dic[str(indexNum-1)][y].append(str(indexNum))
      g1 = graph(dic,[str(indexNum-2)],[str(indexNum)])
      indexNum = indexNum + 1
    # obj$a
    elif (not isinstance(x,str)) and isinstance(y,str):
      dic = x.dic
      dicEnd = x.end
      dic[str(indexNum)] = initDic()
      for end in dicEnd:
        dic[end][y].append(str(indexNum))
      g1 = graph(dic,x.start,[str(indexNum)])
      indexNum = indexNum + 1
    # obj$obj
    elif (not isinstance(x,str)) and (not isinstance(y,str)):
      dicx = x.dic
      dicxEnd = x.end
      dicy = y.dic
      dicyStart = y.start

      dic = dicx
      for dicxx in dicx:
        dic[dicxx] = dicx[dicxx]
      for dicyy in dicy:
        dic[dicyy] = dicy[dicyy]
      
      for xend in dicxEnd:
        for ystart in dicyStart:
          dic[xend]['null'].append(ystart)
      g1 = graph(dic,x.start,y.end)
    # a$obj
    else:
      dic = y.dic
      dic[str(indexNum)] = initDic()
      dicyStart = y.start
      for ystart in dicyStart:
        dic[str(indexNum)][x].append(ystart)
      g1 = graph(dic,[str(indexNum)],y.end)
      indexNum = indexNum + 1
  elif op == '*':
    if isinstance(x,str):
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1
      dic[str(indexNum-1)]['null'].append(str(indexNum-2))
      dic[str(indexNum-2)][x].append(str(indexNum-1))
      g1 = graph(dic,[str(indexNum-2)],[str(indexNum-1)])
    else:
      dic = x.dic
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1
      dicStart = x.start[0]
      dicEnd = x.end[0]
      dic[dicEnd]['null'].append(dicStart)
      dic[str(indexNum-2)]['null'].append(dicStart)
      dic[str(indexNum-2)]['null'].append(str(indexNum-1))
      dic[dicEnd]['null'].append(str(indexNum-1))
      g1 = graph(dic,[str(indexNum-2)],[str(indexNum-1)])
  elif op == '|':
    # a|a
    if isinstance(x,str) and isinstance(y,str):
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1

      dic[str(indexNum-6)]['null'].append(str(indexNum-5))
      dic[str(indexNum-6)]['null'].append(str(indexNum-3))
      dic[str(indexNum-5)][x].append(str(indexNum-4))
      dic[str(indexNum-4)]['null'].append(str(indexNum-1))
      dic[str(indexNum-3)][y].append(str(indexNum-2))
      dic[str(indexNum-2)]['null'].append(str(indexNum-1))

      g1 = graph(dic,[str(indexNum-6)],[str(indexNum-1)])
      
    # obj|a
    elif (not isinstance(x,str)) and isinstance(y,str):
      dic = x.dic
      dicEnd = x.end[0]
      dicStart = x.start[0]

      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1

      dic[str(indexNum-4)]['null'].append(dicStart)
      dic[str(indexNum-4)]['null'].append(str(indexNum-3))
      dic[str(indexNum-3)][y].append(str(indexNum-2))
      dic[str(indexNum-2)]['null'].append(str(indexNum-1))
      dic[dicEnd]['null'].append(str(indexNum-1))

      g1 = graph(dic,[str(indexNum-4)],[str(indexNum-1)])

    # obj|obj
    elif (not isinstance(x,str)) and (not isinstance(y,str)):
      dicx = x.dic
      dicxEnd = x.end[0]
      dicxStart = x.start[0]
      dicy = y.dic
      dicyStart = y.start[0]
      dicyEnd = y.end[0]

      # dic = dicx
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1

      for dicxx in dicx:
        dic[dicxx] = dicx[dicxx]
      for dicyy in dicy:
        dic[dicyy] = dicy[dicyy]
      
      dic[str(indexNum-2)]['null'].append(dicxStart)
      dic[str(indexNum-2)]['null'].append(dicyStart)
      dic[dicxEnd]['null'].append(str(indexNum-1))
      dic[dicyEnd]['null'].append(str(indexNum-1))

      g1 = graph(dic,[str(indexNum-2)],[str(indexNum-1)])
    # a|obj
    else:
      dic = y.dic
      dicEnd = y.end[0]
      dicStart = y.start[0]

      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1
      dic[str(indexNum)] = initDic()
      indexNum = indexNum + 1

      dic[str(indexNum-4)]['null'].append(dicStart)
      dic[str(indexNum-4)]['null'].append(str(indexNum-3))
      dic[str(indexNum-3)][x].append(str(indexNum-2))
      dic[str(indexNum-2)]['null'].append(str(indexNum-1))
      dic[dicEnd]['null'].append(str(indexNum-1))

      g1 = graph(dic,[str(indexNum-4)],[str(indexNum-1)])

  print('dic',dic)
  print('start',g1.start,'end',g1.end)

  return g1

if __name__ == '__main__':
  express = 'abb*(a|b)abb(a|b)'
  # express = '(a|b)*abb'
  ans = expression(express)
  print(ans)

  # dic = construct('a','b','$')
  # dic2 = construct(dic,'b','$')
  # print('index',indexNum,'div',dic2)
  dic = calculate(ans)
