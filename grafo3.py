from collections import defaultdict
from typing import *
import numpy as np
import time
from math import ceil

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
        
        self.original_pointer = None
        self.reversa_pointer = None
        
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
            self.reversa_pointer.atualizar(gargalo)
    
    def elegivel(self, delta: int) -> bool:
        if self.capacidade_residual >= delta:
            return True
        else:
            return False

class Grafo:
    def __init__(self, dados:str, direcionado: bool = True) -> None:
        self.dados = dados

        self.grafo = defaultdict(list) 
        arquivo = open(self.dados, 'r')
        self.tamanho = int(arquivo.readline())
        if direcionado == True:
            for linha in arquivo:   #Criando grafo residual
                split = linha.split()
                vertice1 = int(split[0])
                vertice2 = int(split[1])
                capacidade = int(split[2])
                original = self.add_aresta(vertice1, vertice2, capacidade, 0, False)
                reversa = self.add_aresta(vertice2, vertice1, capacidade, 0, True)
                
                original.reversa_pointer = reversa
                reversa.original_pointer = original
                
        if direcionado == False:
            for linha in arquivo:   #Criando grafo residual
                split = linha.split()
                vertice1 = int(split[0])
                vertice2 = int(split[1])
                capacidade = int(split[2])
                self.add_aresta(vertice1, vertice2, capacidade, 0, False)
                self.add_aresta(vertice2, vertice1, capacidade, 0, True)
                self.add_aresta(vertice1, vertice2, capacidade, 0, True)
                self.add_aresta(vertice2, vertice1, capacidade, 0, False)
        arquivo.close

    def add_aresta(self, vertice1: int, vertice2: int, capacidade:int, fluxo:int, reversa:bool) -> None:
        self.grafo[vertice1].append(Aresta(vertice1, vertice2, capacidade, fluxo, reversa))
        return self.grafo[vertice1][-1]

    def get_vizinhos(self, vertice: int):
        vizinhos = self.grafo[vertice]
        return vizinhos

    def bfs(self, inicio: int, fim: int, delta: int) -> List[Aresta]:
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
                if explorados[vizinho.vertice2] == 0 and vizinho.elegivel(delta):
                    explorados[vizinho.vertice2] = 1
                    pais[vizinho.vertice2] = atual
                    if vizinho.vertice2 == fim:
                        pais.append(vizinho)
                        return pais
                    fila.append(vizinho)
        return False

    def get_caminho(self, inicio: int, fim: int, delta: int = 1) -> List[Aresta]:
        pais = self.bfs(inicio, fim, delta)
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

    def ford_fulkerson(self, inicio: int, fim:int, escrita: str, delta: bool = False, reset: bool = False) -> int:
        if reset == True:
            self.reset()

        if delta == False:
            caminho = self.get_caminho(inicio, fim)
            while caminho:
                self.aumentar(caminho)
                caminho = self.get_caminho(inicio, fim)

        if delta == True:
            capacidade = self.get_capacidade(inicio)
            delta = ceil(capacidade/2)
            while delta != 1:     
                caminho = self.get_caminho(inicio, fim, delta)
                while caminho:
                    self.aumentar(caminho)
                    caminho = self.get_caminho(inicio, fim, delta)
                delta = ceil(delta/2)
            caminho = self.get_caminho(inicio, fim)
            while caminho:
                self.aumentar(caminho)
                caminho = self.get_caminho(inicio, fim)

        fluxo = self.get_fluxo(inicio)
        tempo_leitura = self.alocacao(escrita)
        reset = True
        return fluxo, tempo_leitura

    def get_fluxo(self, vertice: int) -> int:
        fluxo = 0
        vizinhos = self.get_vizinhos(vertice)
        for aresta in vizinhos:
            fluxo += aresta.fluxo
        return fluxo

    def get_capacidade(self, vertice: int) -> int:
        capacidade = 0
        vizinhos = self.get_vizinhos(vertice)
        for aresta in vizinhos:
            capacidade += aresta.capacidade
        return capacidade

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

    def alocacao(self, escrita: str) -> int:
        arquivo = open(escrita, 'w')
        arquivo.writelines('aresta,vertice1,vertice2,fluxo\n')
        grafo = self.grafo
        count=0
        inicio = time.time()
        for vertice in grafo:
            for aresta in grafo[vertice]:
                if aresta.reversa == False:
                    count += 1
                    arquivo.writelines(f'{count},{aresta.vertice1},{aresta.vertice2},{aresta.fluxo} \n')
        fim = time.time()
        tempo=(fim - inicio)
        arquivo.close()
        return tempo