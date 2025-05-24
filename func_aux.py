import numpy as np
import random
from numba import njit
from numba.typed import List
from collections import Counter

def square_lattice(L):
    """
    Calculamos la matriz de adyacencia de una lattice cuadrada NxN con condiciones de contorno periódicas.
    """ 
    size = L * L
    adjacency_matrix = np.zeros((size, size), dtype=int)
    for i in range(L):
        for j in range(L):
            current = i * L + j
            # Vecino de arriba (con contorno periódico)
            up = ((i - 1) % L) * L + j
            adjacency_matrix[current, up] = 1
            # Vecino de abajo (con contorno periódico)
            down = ((i + 1) % L) * L + j
            adjacency_matrix[current, down] = 1
            # Vecino de la izquierda (con contorno periódico)
            left = i * L + (j - 1) % L
            adjacency_matrix[current, left] = 1
            # Vecino de la derecha (con contorno periódico)
            right = i * L + (j + 1) % L
            adjacency_matrix[current, right] = 1
    return adjacency_matrix
#Calculamos la lista de vecinos
def obtener_vecinos(adj_matrix, N, p):
    vecinos_list = List()  # Lista compatible con Numba
    for i in range(N):
        vecinos = List()
        # Añade los vecinos de la matriz de adyacencia
        for idx in np.nonzero(adj_matrix[i])[0]:
            vecinos.append(int(idx))

        # Añade los medios (de N a N+p-1)
        for medio in range(N, N + p):
            vecinos.append(medio)

        vecinos_list.append(vecinos)
    
    return vecinos_list

#Inicializa al azar la matriz de agentes
@njit
def MatrizInicial(agentes, N, f, q, prensas):
    for i in range(N+prensas):
         for j in range(f):
            agentes[i, j] = np.random.integers(0, q - 1)
    

#Calcula la fracción de rasgos compartidos entre agentes i y j 
@njit
def similarity(i, j, agentes,f):
    sim = 0
    for k in range(f):
        if agentes[i, k] == agentes[j, k]:
            sim += 1
    return sim / f

#Comprueba si ha finalizado la interacción
@njit
def FinInteraccion(agentes, vecinos_list, N,f, p, sim_min):
    linksactivos = 0
    for i in range(N):
        for j in vecinos_list[i]:
            if j < i or (N <= j < N + p):
                sim= similarity(i, j, agentes, f)
                if sim<1 and sim>=sim_min:
                    linksactivos = linksactivos + 1
    if linksactivos == 0: #or prensas>1:  
        # Si no queda interacción posible, devuelve True                    
        return True, linksactivos 
    else:           
        #Si encuentra al menos una interacción posible, devuelve False
        return False, linksactivos
          

#Comprueba si dos agentes tienen exactamente la misma cultura. Devuelve True si son iguales y False si son diferentes
#@njit
def misma_cultura(a, b):
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True

#Calculamos el tamño del mayor cluster
#@njit
def tamaño_mayor_cluster(agentes, vecinos_list, N):
    visitado = [False] * N
    mayor_cluster = 0
    for i in range(N):
        if not visitado[i]:
            cluster_size = 0
            pila = [i]
            visitado[i] = True

            while pila:
                nodo = pila.pop()
                cluster_size += 1
                
                for v in vecinos_list[nodo]:
                    if v<N and not visitado[v] and misma_cultura(agentes[i], agentes[v]):
                        visitado[v] = True
                        pila.append(v)

            if cluster_size > mayor_cluster:
                mayor_cluster = cluster_size

    return mayor_cluster / N 
# Más general que el anterior, ya que no solo devuelve el tamaño del mayor cluster.
def tamaños_clusters(agentes, vecinos_list, N):
    visitado = [False] * N
    tamaños = []

    for i in range(N):
        if not visitado[i]:
            cluster_size = 0
            pila = [i]
            visitado[i] = True

            while pila:
                nodo = pila.pop()
                cluster_size += 1
                
                for v in vecinos_list[nodo]:
                    if v < N and not visitado[v] and misma_cultura(agentes[i], agentes[v]):
                        visitado[v] = True
                        pila.append(v)

            tamaños.append(cluster_size)

    tamaños.sort(reverse=True)

    # Contar la frecuencia de cada tamaño
    contador = Counter(tamaños)

    # Ordenar por tamaño de mayor a menor
    tamaños_ordenados = sorted(contador.keys(), reverse=True)
    frecuencias_ordenadas = [contador[t] for t in tamaños_ordenados]

    #matriz de dos filas que en la primera tiene el tamaño de un cluster y en la segunda las vecs que aparece
    matriz = np.array([tamaños_ordenados, frecuencias_ordenadas])
    return matriz

@njit
def transformarmatriz(agentes, L, f, matriznueva):
    """
    Transforma la matriz de agentes en una matriz de tamaño L x L x f.
    """
    for i in range(L):
        for j in range(L):
            for k in range(f):
                # Asignamos el valor de la matriz original a la nueva matriz
                # La nueva matriz tiene dimensiones L x L x f
                # La matriz original es de tamaño (N+prensas) x f
                # Por lo tanto, necesitamos calcular el índice correspondiente en la matriz original
                # El índice en la matriz original es i * L + j
                # y el índice en la nueva matriz es i, j, k
                matriznueva[i][j][k] = agentes[i*L+j][k]
    return matriznueva


def MatIniPrenExcl(agentes, N, f, q, prensas):
    prensaaleatoria = np.zeros((N + prensas, f), dtype=int)
    valor=0
    # Inicializa los agentes normales
    for i in range(N):
        for j in range(f):
            agentes[i][j] = np.random.randint(0, q)
    # Inicializa los agentes de prensa asegurando que no sean iguales entre sí
    for i in range(q):
        for j in range(f):
            prensaaleatoria[i][j] = i

    for k in range(q*f*prensas):
        i= random.randint(0, q-1)
        j= random.randint(0, f-1)
        valor=prensaaleatoria[i][j]
        ia=random.randint(0, q-1)
        ja=random.randint(0, f-1)
        prensaaleatoria[i][j]= prensaaleatoria[ia][ja]
        prensaaleatoria[ia][ja]= valor

    for i in range(N, N+prensas):
        for j in range(f):
            agentes[i][j] = prensaaleatoria[i][j]



            """while True:
            nuevo = [np.random.randint(0, q) for _ in range(f)]
            es_unico = True
            for k in range(N, i):
                if all(agentes[k][j] == nuevo[j] for j in range(f)):
                    es_unico = False
                    break
            if es_unico:
                for j in range(f):
                    agentes[i][j] = nuevo[j]
                break """

            
"""def FinInteraccionPrensa(agentes, vecinos_list, N,f, prensas, sim_min):
    linksactivos = 0
    for i in range(N+prensas):
        for j in vecinos_list[i]:
            if j<N:
                sim= similarity(i, j, agentes, f)
                if sim<1 and sim>=sim_min:
                    linksactivos = linksactivos + 1
    if linksactivos == 0: #or prensas>1:  
        # Si no queda interacción posible, devuelve True                    
        return True, linksactivos 
    else:           
        if linksactivos<N*prensas:
        #Si encuentra al menos una interacción posible, devuelve False
        return False, linksactivos"""

        
        