from reconhecedor import *

def main():

    """ CONVERSAO AFN => AFD """
    # inicializa os objetos que serao usados como AFN e AFD
    afn = AFN()
    afd = AFD()

    # le o AFN do arquivo e passa para o objeto
    linhas = stringArq()
    afn.leAFN(linhas)
    print "AFN ORIGINAL"
    afn.printaAFN()
    print

    # funcao que converte o AFN para AFD
    convertAFN_AFD(afn,afd)

    # imprime AFD gerado
    print
    print "AFD EQUIVALENTE"
    afd.printaAFD()

    """ RECONHECIMENTO DE PALAVRAS """
    print
    dict = criaDict(afd)
    print

    nomeArq = raw_input("Digite arquivo com a lista de palavras: ")

    lista = listaDef(nomeArq)

    print
    print "RESULTADOS"

    for palavra in lista:
        palavra = palavra[1:]
        if reconhece(dict,afd.estInicial[0],afd.estFinais,palavra):
            print "A palavra "+palavra+" eh ACEITA"
        else:
            print "A palavra "+palavra+" eh REJEITA"

if __name__ == "__main__":
    main()