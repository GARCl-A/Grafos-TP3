from grafo3 import Grafo
import time


#Grafo a ser analisado:
grafo_atual = 'grafo_rf_7.txt'

#Ford-Fulkerson com grafo restringido ou não?

delta = True

#Leitura do grafo:
grafo = Grafo(grafo_atual)

#Ford-Fulkerson:
arquivo = open(f'tempo_{grafo_atual}.txt','w')
arquivo.writelines('passo,tempo\n')

tempo_total = 0

for i in range(10):
  
    inicio = time.time()
    tempo_escrita = grafo.ford_fulkerson(1, 2, f'alocacao_{grafo_atual}.txt', delta = delta)[1]
    fim = time.time()
    tempo_algoritmo = fim - inicio

    tempo_total += tempo_algoritmo-tempo_escrita

    arquivo.writelines(
        f'{i},{fim - inicio}\n'
        )
    print({i})

fluxo = grafo.ford_fulkerson(1, 2, f'alocacao_{grafo_atual}.txt', delta = delta)[0]
print(f'Tempo médio = {tempo_total/10} segundos')
print(f'Fluxo máximo = {fluxo}')
arquivo.close()
