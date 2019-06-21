from automato import *

def main():
    linhas = stringArq()

    afn = AFN()
    afd = AFD()

    afn.leAFN(linhas)
    print "AFN"
    afn.printaAFN()
    print
    print

    #print afn.alfabeto
   # dict = {simbolo: [] for simbolo in afn.alfabeto}

   # dict['1'].append('q1')
   # dict['1'].append('q2')

   # print str(dict)
   # estadosEq(afn,afd)
    #detAFN(afd)
    convertAFN_AFD(afn,afd)

    print
    print
    print "AFD"
    afd.printaAFD()
    #afn.printaAFN()



main()