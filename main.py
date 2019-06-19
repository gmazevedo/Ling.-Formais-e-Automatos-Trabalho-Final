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

    estadosEq(afn,afd)
    detAFN(afd)

    print
    print
    print "AFD"
    afd.printaAFD()



main()