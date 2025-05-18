import numpy as np
import matplotlib.pyplot as plt

def graf_Smax_vs_q(q_values, par_orden_medio, par_orden_std, f, M, L,p,h):
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
        plt.savefig(f"Axelrod_F{f}_M{M}_L{L}_P{p}_h{h}.png", dpi=300)
    else:
        plt.savefig(f"Axelrod_F{f}_M{M}_L{L}_P{p}.png", dpi=300)
    plt.show()