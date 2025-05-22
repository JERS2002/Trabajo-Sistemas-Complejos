import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def graf_Smax_vs_q(q_values, par_orden_medio, par_orden_std, f, M, L,p,h):
    carpeta = "Smax_vs_q_graficas/"
    plt.figure(figsize=(10, 6))
    plt.errorbar(q_values, par_orden_medio , yerr= par_orden_std, fmt='o-', capsize=4, label=f'N = {L}$^2$')
    plt.xlabel("q")
    plt.ylabel("S_${max}$/N")
    if p>0:
        plt.title(f"Modelo de Axelrod (F = {f}, M = {M}, P = {p}, h = {h})")
    else:
        plt.title(f"Modelo de Axelrod (F = {f}, M = {M}, P = {p})")
    plt.grid(True)
    plt.legend()
    if p>0:
        plt.savefig(carpeta + f"Axelrod_F{f}_M{M}_L{L}_P{p}_h{h}.png", dpi=300)
    else:
        plt.savefig(carpeta + f"Axelrod_F{f}_M{M}_L{L}_P{p}.png", dpi=300)
    plt.show()

"""def graf_Smax_std_vs_q(q_values, par_orden_std, f, M, L,p,h):
    carpeta = "Smax_std_vs_q_graficas/"
    plt.figure(figsize=(10, 6))
    plt.plot(q_values, par_orden_std , 'o-', label=f'N = {L}$^2$')
    plt.xlabel("q")
    plt.ylabel("$\\frac{\sigma(S_{max})}{N}$")
    if p>0:
        plt.title(f"Modelo de Axelrod (F = {f}, M = {M}, P = {p}, h = {h})")
    else:
        plt.title(f"Modelo de Axelrod (F = {f}, M = {M}, P = {p})")
    plt.grid(True)
    plt.legend()
    if p>0:
        plt.savefig(carpeta + f"std_Axelrod_F{f}_M{M}_L{L}_P{p}_h{h}.png", dpi=300)
    else:
        plt.savefig(carpeta + f"std_Axelrod_F{f}_M{M}_L{L}_P{p}.png", dpi=300)
"""
def links_activos_vs_tiempo(link_list):
    tiempos = list(range(len(link_list)))
    plt.figure(figsize=(8, 5))
    plt.plot(tiempos, link_list, marker='o', linestyle='-', color='blue')
    plt.xlabel('Tiempo')
    plt.ylabel('Número de links activos')
    plt.title('Evolución de los links activos en el tiempo')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("links_activos_vs_tiempo.png", dpi=300)
    plt.show()
    

def animar_matriz_vectores(matrices, q):
    intervalo = 20
    max_val = q - 1  # Valor máximo posible para cada canal
    matrices_rgb = []
    for mat in matrices:
        mat_norm = mat.astype(float) / max_val
        mat_norm = np.clip(mat_norm, 0, 1)  # Asegura que los valores estén en [0,1]
        matrices_rgb.append(mat_norm)
    
    fig, ax = plt.subplots()
    im = ax.imshow(matrices_rgb[0], interpolation='nearest')
    ax.axis('off')

    def actualizar(frame):
        im.set_array(matrices_rgb[frame])
        return [im]

    ani = animation.FuncAnimation(
        fig, actualizar, frames=len(matrices_rgb), interval=intervalo, blit=True, repeat=False
    )
    ani.save('animacion.gif', writer='pillow')
    plt.show()
    return ani  # Mantén la referencia

# filepath: vsls:/graficas.py
'''
def animar_matriz_vectores(matrices):

    #matrices: lista de matrices 3D (shape: filas x columnas x f), donde f=3 (R,G,B)
    #intervalo: tiempo entre frames en ms
    intervalo=200
    # Normaliza los valores a [0,1] para RGB
    matrices_rgb = []
    for mat in matrices:
        # Normaliza cada canal por separado si quieres, o todo junto
        mat_norm = mat.astype(float)
        for c in range(mat.shape[2]):
            max_val = np.max(mat[:,:,c])
            if max_val > 0:
                mat_norm[:,:,c] /= max_val
        matrices_rgb.append(mat_norm)
    
    fig, ax = plt.subplots()
    im = ax.imshow(matrices_rgb[0], interpolation='nearest')
    ax.axis('off')

    def actualizar(frame):
        im.set_array(matrices_rgb[frame])
        return [im]

    ani = animation.FuncAnimation(
        fig, actualizar, frames=len(matrices_rgb), interval=intervalo, blit=True, repeat=False
    )

    ani.save('animacion.gif', writer='pillow')
    plt.show()  

    def animar_matriz_vectores(matrices,):
    intervalo = 200
    matrices_rgb = []
    for mat in matrices:
        mat_norm = mat.astype(float)
        for c in range(mat.shape[2]):
            max_val = np.max(mat[:,:,c])
            if max_val > 0:
                mat_norm[:,:,c] /= max_val
        matrices_rgb.append(mat_norm)
    
    fig, ax = plt.subplots()
    im = ax.imshow(matrices_rgb[0], interpolation='nearest')
    ax.axis('off')

    def actualizar(frame):
        im.set_array(matrices_rgb[frame])
        return [im]

    ani = animation.FuncAnimation(
        fig, actualizar, frames=len(matrices_rgb), interval=intervalo, blit=True, repeat=False
    )
    # Guarda el gif ANTES de mostrar
    ani.save('animacion.gif', writer='pillow')
    plt.show()
    return ani  # Mantén la referencia

    '''
