from collections import defaultdict
from typing import *
import numpy as np

class Aresta:
    def __init__(self, vertice1: int, vertice2:int, capacidade:int, fluxo:int, reversa:bool) -> None:
        """O vertice1 aponta para o vertice2, por meio de uma aresta com capacidade e fluxo

        Args:
            vertice1 (int): 
            vertice2 (int): 
            capacidade (int): 
            fluxo (int): 
        """
        self.vertice1 = int(vertice1)
        self.vertice2 = int(vertice2)

        self.capacidade = int(capacidade)
        self.fluxo = int(fluxo)

        self.reversa = reversa
        self.capacidade_residual = 0
        if reversa:
            self.capacidade_residual = self.fluxo
        else:
            self.capacidade_residual = self.capacidade - self.fluxo

    def atualizar(self, gargalo:int):
        self.fluxo += gargalo
        if self.reversa == True:
            self.capacidade_residual = self.fluxo
        else:
            self.capacidade_residual = self.capacidade - self.fluxo
    
    def elegivel(self):
        if self.capacidade_residual == 0:
            return False
        else:
            return True

class Grafo:
    def __init__(self, dados:str) -> None:
        self.dados = dados

        self.grafo = defaultdict(list) 
        arquivo = open(self.dados, 'r')
        self.tamanho = int(arquivo.readline())

        for linha in arquivo:   #Criando grafo residual
            split = linha.split()
            vertice1 = int(split[0])
            vertice2 = int(split[1])
            capacidade = int(split[2])
            self.add_aresta(vertice1, vertice2, capacidade, 0, False)
            self.add_aresta(vertice2, vertice1, capacidade, 0, True)
        arquivo.close

    def add_aresta(self, vertice1: int, vertice2: int, capacidade:int, fluxo:int, reversa:bool) -> None:
        self.grafo[vertice1].append(Aresta(vertice1, vertice2, capacidade, fluxo, reversa))

    def get_vizinhos(self, vertice: int):
        vizinhos = self.grafo[vertice]
        return vizinhos

    def bfs(self, inicio:int, fim:int) -> List[Aresta]:
        setup = 1
        explorados = [0] * (self.tamanho + 1) #O Zero não será utilizado
        pais = [0] * (self.tamanho + 1) #O Zero não será utilizado
        explorados[inicio] = 1
        pais[inicio] = None

        fila = [inicio]
        while fila != []:
            atual = fila.pop()
            vizinhos = []
            if setup == 1:
                vizinhos = self.get_vizinhos(atual)
                setup = 0
            else:
                vizinhos = self.get_vizinhos(atual.vertice2)
            for vizinho in vizinhos:
                if explorados[vizinho.vertice2] == 0 and vizinho.elegivel():
                    explorados[vizinho.vertice2] = 1
                    pais[vizinho.vertice2] = atual
                    if vizinho.vertice2 == fim:
                        pais.append(vizinho)
                        return pais
                    fila.append(vizinho)
        return False

    def get_caminho(self, inicio: int, fim: int) -> List[int]:
        pais = self.bfs(inicio, fim)
        if pais:
            caminho = [pais[-1]]
            atual = pais[fim]
            while atual != inicio:
                caminho.append(atual)
                atual = pais[atual.vertice2]
            return caminho
        else:
            return False

    def get_gargalo(self, caminho: List[Aresta]) -> Aresta:
        gargalo = caminho[0]
        for aresta in caminho:
            if aresta.capacidade_residual < gargalo.capacidade_residual:
                gargalo = aresta
        return gargalo

    def aumentar(self, caminho: List[Aresta]) -> None:
        gargalo = self.get_gargalo(caminho)
        gargalo_valor = gargalo.capacidade_residual
        for aresta in caminho:
            aresta.atualizar(gargalo_valor)

    def ford_fulkerson(self, inicio: int, fim:int, reset: bool = False) -> int:
        if reset == True:
            self.reset()
        caminho = self.get_caminho(inicio, fim)
        while caminho:
            self.aumentar(caminho)
            caminho = self.get_caminho(inicio, fim)
        fluxo = self.get_fluxo(inicio)
        reset = True
        return fluxo

    def get_fluxo(self, vertice: int) -> int:
        fluxo = 0
        vizinhos = self.get_vizinhos(vertice)
        for aresta in vizinhos:
            fluxo += aresta.fluxo
        return fluxo

    def reset(self):
        self.grafo = defaultdict(list) 
        arquivo = open(self.dados, 'r')
        self.tamanho = int(arquivo.readline())

        for linha in arquivo:   #Criando grafo residual
            split = linha.split()
            vertice1 = int(split[0])
            vertice2 = int(split[1])
            capacidade = int(split[2])
            self.add_aresta(vertice1, vertice2, capacidade, 0, False)
            self.add_aresta(vertice2, vertice1, capacidade, 0, True)
        arquivo.close