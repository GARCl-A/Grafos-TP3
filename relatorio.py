from grafo3 import Grafo
import time


#Grafo a ser analisado:
grafo_atual = 'grafo_rf_2.txt'

#Leitura do grafo:
grafo = Grafo(grafo_atual)

#Ford-Fulkerson:
arquivo = open(f'tempo_{grafo_atual}.txt','w')
arquivo.writelines('passo,tempo\n')

tempo_total = 0

for i in range(10):
  
    inicio = time.time()
    grafo.ford_fulkerson(1, 2, f'alocacao_{grafo_atual}.txt')
    fim = time.time()

    tempo_total += fim - inicio

    arquivo.writelines(
        f'{i},{fim - inicio}\n'
        )
    print({i})


print(f'Tempo médio = {tempo_total/10} segundos')
print(grafo.ford_fulkerson(1, 2, f'alocacao_{grafo_atual}.txt'))
arquivo.close()
