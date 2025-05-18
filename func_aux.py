import numpy as np
import random
#from numba import njit

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
    vecinos_list = []
    for i in range(N):
        vecinos = list(map(int, np.nonzero(adj_matrix[i])[0]))  # fuerza int
        vecinos += list(range(N, N + p)) 
        vecinos_list.append(vecinos)
    return vecinos_list

#Inicializa al azar la matriz de agentes
#@njit
def MatrizInicial(agentes, N, f, q, prensas):
    for i in range(N+prensas):
         for j in range(f):
            agentes[i][j] = np.random.randint(0,q)
    

#Calcula la fracción de rasgos compartidos entre agentes i y j 
#@njit
def similarity(i, j, agentes,f):
    sim = 0
    for k in range(f):
        if agentes[i, k] == agentes[j, k]:
            sim += 1
    return sim / f

#Comprueba si ha finalizado la interacción
#@njit
def FinInteraccion(agentes, vecinos_list, N,f, prensas, sim_min):
    for i in range(N):
        for j in vecinos_list[i]:
            if j<N:
                sim= similarity(i, j, agentes, f)
                if sim<1 and sim>=sim_min:
                    return False #Si encuentra al menos una interacción posible, devuelve False
    # Si no queda interacción posible, devuelve True                    
    return True      

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
