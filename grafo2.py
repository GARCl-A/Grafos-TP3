from collections import defaultdict
from typing import *

class Vertice:  
    def __init__(self, identificacao:int, capacidade:int, fluxo:int) -> None:
        self.identificacao = identificacao
        self.capacidade = capacidade
        self.fluxo = fluxo

class Grafo:
    def __init__(self, txt:str) -> None:
        self.grafo = defaultdict(list)
        arquivo = open(txt, 'r')
        self.tamanho = int(arquivo.readline())
        for linha in arquivo:   #Adicionando vizinhos às listas
            split = linha.split() #Split 0:vertice1, 1:vertice2, 2:peso, necessário casing para inteiro, já que no txt são strings
            self.grafo[int(split[0])].append(Vertice(int(split[1]), int(split[2]),0))
        arquivo.close

    def get_vizinhos_identificacao(self, vertice:int) -> List[int]:
        vizinhos = []
        for vizinho in self.grafo[vertice]:
            vizinhos.append(vizinho.identificacao)
        return vizinhos

    def get_vizinhos_objeto(self, vertice:int) -> List[Vertice]:
        vizinhos = []
        for vizinho in self.grafo[vertice]:
            vizinhos.append(vizinho)
        return vizinhos


