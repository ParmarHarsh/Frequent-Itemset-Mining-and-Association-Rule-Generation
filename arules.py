'''
------------------------------------------------------------------------------
arules
------------------------------------------------------------------------------
'''
import sys
import time

startTime = time.time()

#=============================================================================
# FUNCTIONS

def istrClean(istr):
    istr = ' '.join(istr.strip('\n').split())
    for token in istr.split():
        if not token.isnumeric():
            print('Item "%s" is not an integer!' % token)
            exit(-1)
    return istr

def string2iset(istr):
    return [int(token) for token in istr.split()]

def iset2string(iset):
    itok = [str(item) for item in iset]
    return ' '.join(itok)

# function to read the length of itemsets from files
def readFile(file_path):
    j = 0
    k = 0
    if(file_path == sys.argv[1]):
        itemsetJ = {}
        with open(file_path, 'r', encoding='utf-8') as inJ:
            for lineJ in inJ:
                lineJ = istrClean(lineJ)
                itemsetJ = string2iset(lineJ.strip('\n'))
                j = len(itemsetJ)
                break
            else:
                print('Empty input file!');
                exit();    
        return j
    elif (file_path == sys.argv[2]):
        k = 0
        itemsetK = {}
        with open(file_path, 'r', encoding='utf-8') as inK:
            for lineK in inK:
                lineK = istrClean(lineK)
                itemsetK = string2iset(lineK.strip('\n'))
                k = len(itemsetK)
                break
            else:
                print('Empty input file!');
                exit();    
        return k
    else:
        print('Command-line input error!')

def getSets(s, j):
    def getSubsets(cSets, remElements, tLength):
        if len(cSets) == tLength:
            yield cSets
        elif remElements:
            yield from getSubsets(cSets + [remElements[0]], remElements[1:], tLength)
            yield from getSubsets(cSets, remElements[1:], tLength)

    subsets = getSubsets([], list(s), j)
    return subsets

def generateRules(itemsetK, itemsK, itemsetJ, itemsJ, p, asRules):
    for subset in getSets(itemsetK, j):
        if iset2string(subset) in itemsetJ:
            if itemsK/itemsetJ[iset2string(subset)] >= p:
                rule = iset2string(subset) + ' => ' + iset2string([x for x in itemsetK if x not in subset])
                conf = itemsK/itemsetJ[iset2string(subset)]
                asRules[rule] = conf
    return asRules

#=============================================================================
# MAIN

if __name__ == '__main__':
    j = readFile(sys.argv[1])
    k = readFile(sys.argv[2])

    if not (0<j<k):
        print('Error in frequent itemset length')
        exit();
    
    p = float(sys.argv[3])

    if not (0<=p<=1):
        print('Confidence not between 0-1')
        exit();

    itemsetJ = {}
    itemsetK = {}
    asRules = {}

    with open(sys.argv[1], 'r', encoding='utf-8') as fileJ:
        for lineJ in fileJ:
           lineJ = istrClean(lineJ)
           itemwcountJ = string2iset(lineJ.strip('\n'))
           itemsJ = itemwcountJ[0]
           itemsetK = iset2string(itemwcountJ[1:])
           itemsetJ[itemsetK] = itemsJ;

    with open(sys.argv[2], 'r', encoding='utf-8') as fileK:
        for lineK in fileK:
            lineK = istrClean(lineK)
            itemwcountK = string2iset(lineK.strip('\n'))
            itemsK = itemwcountK[0]
            itemsetK = itemwcountK[1:]
            asRules = generateRules(itemsetK, itemsK, itemsetJ, itemsJ, p, asRules)
                    
    endTime = time.time()

    for rule, conf in asRules.items():
        print('{:.3f} {} => {}'.format(conf, rule.split(' => ')[0], rule.split(' => ')[1]))

    print('')
    print('Lapsed time:     %.3f' % (endTime - startTime))