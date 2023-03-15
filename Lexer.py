import regex as r

if __name__ == '__main__':
    regex = "(const|char|procedure|begin|end)*(begin|end)"
    test1 = "babababb"
    test2 = "constcharbeginendend"
    test3 = "constconstconstend"
    # res = stringBelongRegex(test3,regex)
    array,end=r.regexToDFAArray(regex)
    res = r.stringBelongRegexByArray(test3,array,end)
    print(res)