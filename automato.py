def stringArq():
    nomeArq = raw_input("Nome do arquivo com o automato: ")
    #nomeArq = "teste.txt"

    arquivo = open(nomeArq, 'r')

    linhas = arquivo.read()

    arquivo.close()

    linhas = linhas.splitlines()

    return linhas


class AFN():
    def __init__(self):
        self.estados =[]
        self.numEstados = 0
        self.alfabeto = []
        self.estInicial = []
        self.estFinais = []
        self.numFinais = 0
        self.transicoes = []

    def init_estados(self):
        self.estados = list(range(self.numEstados))

    def leAFN(self,linhas):
        """Indices da linha 0:
        [0]-ESTADOS [1]-ALFABETO [2]-EST INICIAL [3]-EST FINAL"""
        linhas[0] = linhas[0].split('(')
        linhas[0] = linhas[0][1].split('}')

        self.numEstados = len(linhas[0][0][1:].split(','))
        self.estados = linhas[0][0][1:].split(',')
        self.alfabeto = linhas[0][1][2:].split(',')
        self.estInicial = linhas[0][2][2:].split(',')
        self.estFinais = linhas[0][3][2:].split(',')
        self.numFinais = len(linhas[0][3][2:].split(','))
        self.transicoes = linhas[2:]

        return self.estInicial


    def printaAFN(self):
        print "Numero de estados: "+str(self.numEstados)
        print "Estados: "+str(self.estados)
        print "Alfabeto: "+str(self.alfabeto)
        print "Estados iniciais: " + str(self.estInicial)
        print "Estados finais: "+str(self.estFinais)
        print "Numero de estados finais: " + str(self.numFinais)
        print "Transicoes: "+str(self.transicoes)


class AFD():
    def __init__(self):
        self.estados = []
        self.numEstados = 0
        self.alfabeto = []
        self.estInicial = []
        self.estFinais = []
        self.numFinais = 0
        self.transicoes = []
        self.q = []
        self.aux = []

    def printaAFD(self):
        print "Numero de estados: "+str(self.numEstados)
        print "Estados: "+str(self.estados)
        print "Alfabeto: "+str(self.alfabeto)
        print "Estados iniciais: " + str(self.estInicial)
        print "Estados finais: "+str(self.estFinais)
        print "Numero de estados finais: " + str(self.numFinais)
        print "Transicoes: "+str(self.transicoes)
        print "Estados temporarios: " + str(self.q)


def estadosEq(afn,afd):

    deletar = []
    afd.alfabeto = afn.alfabeto
    #afd.numFinais = afn.numFinais
    #afd.numEstados = afn.numEstados
    #afd.numEstados -= 1
    afd.estInicial = afn.estInicial
    afd.estados = afd.estados + afn.estInicial

    for a in range(afn.numEstados):
        pos1 = afn.transicoes[a].find(',')
        pos2 = afn.transicoes[a+1].find(',')

        if (afn.transicoes[a][1:pos1] == afn.transicoes[a+1][1:pos2]):    # se os estados sao os mesmos
            pos3 = afn.transicoes[a].find(')')
            pos4 = afn.transicoes[a+1].find(')')

            pos1 += 1
            pos2 += 1

            if(afn.transicoes[a][pos1:pos3] == afn.transicoes[a+1][pos2:pos4] ):   #e as entradas sao as mesmas
                afd.numEstados = afd.numEstados + 1

                pos5 = afn.transicoes[a].find('=') + 1
                pos6 = afn.transicoes[a+1].find('=') + 1

                deletar.append(afn.transicoes[a])
                deletar.append(afn.transicoes[a+1])
                #afd.estados.append(afn.transicoes[a][pos5+1] + afn.transicoes[a][pos5+2] + afn.transicoes[a+1][pos6+1] + afn.transicoes[a+1][pos6+2])
                afd.q.append([afn.transicoes[a][pos5:],afn.transicoes[a+1][pos6:]])#resultando na concatenacao dos destinos (ex: q5q6)
                afd.estados = afd.estados + [(afn.transicoes[a][pos5:] + afn.transicoes[a + 1][pos6:])]
                afd.transicoes = afd.transicoes+ [('('+afn.transicoes[a][1:pos1-1]+','+afn.transicoes[a][pos1:pos3]+')='+(afn.transicoes[a][pos5:] + afn.transicoes[a + 1][pos6:]))]
    #indices = set(indices)
    afd.aux = afn.transicoes
    afd.transicoes = afd.transicoes + afn.transicoes

    return deletar


def detAFN(afd):

    estadosProcessados = []
    novaTrans =[]

    # para cada estado na lista temporaria de estados
    for estado in afd.q:
        # cria um dicionario com os simbolos do alfabeto
        dict = {simbolo: [] for simbolo in afd.alfabeto}
        # para cada estado concatenado nesse novo estado do AFD
        for parte in estado:
            # triplas eh uma lista de todas as transicoes deste estado individual
            triplas = procuraTrans(parte,afd.aux)
            # para cada transicao em triplas
            for item in triplas:
                # verifica se destino nao eh zero (se for zero, significa indefinicao)
                if item[2] != '0':
                    # adiciona na lista de estados gerados por um determinado simbolo
                    dict[item[1]].append(item[2])

        # inclui em uma lista de novas transicoes, as transicoes deste novo estado que eh a concatenacao de estados
        # equivalentes
        estadosProcessados = estadosProcessados + [estado]
        estadoConc = ''.join(estado)

        for chave in dict.keys():
            if len(dict[chave]) > 0:
                if dict[chave] not in afd.q and ''.join(dict[chave]) not in afd.estados:
                    afd.q = afd.q + [dict[chave]]
                novaTrans.append('('+estadoConc+','+chave+')='+''.join(dict[chave]))

    print estadosProcessados
    for processado in estadosProcessados:
        afd.q.remove(processado)

    afd.transicoes = afd.transicoes+novaTrans
    print "novas transicoes: "+str(novaTrans)

# dado um estado e uma lista de transicoes, retorna uma lista de tuplas com todas as transicoes
# do estado recebido
def procuraTrans(origem,transicoes):

    triplaTransicoes = []

    for transicao in transicoes:
        virgula = transicao.find(',')
        igual = transicao.find('=')

        if(transicao[1:virgula] == origem):
            triplaTransicoes.append([origem,transicao[virgula+1:igual-1],transicao[igual+1:]])

    return triplaTransicoes


def deletaTrans(lista,transicoes):
    for transicao in lista:
        if transicao not in transicoes:
            pass
        else:
            transicoes.remove(transicao)

    return transicoes

def incluiEstados(afd):
   # lista = []
   # for estado in afd.q:
   #     lista = lista + [(''.join(estado))]

  #  lista = list(set(lista))

    for transicao in afd.transicoes:
        igual = transicao.find('=')
        igual += 1

        if transicao[igual:] != '0':
            if transicao[igual:] not in afd.estados:
                afd.estados.append(transicao[igual:])


def convertAFN_AFD(afn,afd):
    lista = estadosEq(afn,afd)
    detAFN(afd)
    deletaTrans(lista,afd.transicoes)
    incluiEstados(afd)

    while (len(afd.q) > 0):
        detAFN(afd)
        incluiEstados(afd)