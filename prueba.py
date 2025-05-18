import numpy as np

def square_lattice(N):
    """
    Calcula la matriz de adyacencia de una lattice cuadrada con condiciones de contorno periódicas.
    
    Args:
        N (int): Dimensión de la lattice (N x N).
    
    Returns:
        np.ndarray: Matriz de adyacencia de tamaño (N^2 x N^2).
    """ 
    size = N * N
    adjacency_matrix = np.zeros((size, size), dtype=int)
    for i in range(N):
        for j in range(N):
            current = i * N + j
            # Vecino de arriba (con contorno periódico)
            up = ((i - 1) % N) * N + j
            adjacency_matrix[current, up] = 1
            # Vecino de abajo (con contorno periódico)
            down = ((i + 1) % N) * N + j
            adjacency_matrix[current, down] = 1
            # Vecino de la izquierda (con contorno periódico)
            left = i * N + (j - 1) % N
            adjacency_matrix[current, left] = 1
            # Vecino de la derecha (con contorno periódico)
            right = i * N + (j + 1) % N
            adjacency_matrix[current, right] = 1

    return adjacency_matrix
N=2    
matrix= square_lattice
print(matrix(N))