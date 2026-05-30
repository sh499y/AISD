"""
Algorytmy z powracaniem - wersja finalna.

Zadanie:
  - generujemy spojne grafy nieskierowane, ktore sa jednoczesnie
    eulerowskie (spojne + wszystkie stopnie parzyste) i hamiltonowskie
    (zawieraja cykl Hamiltona), o nasyceniu 30% (rzadki) i 70% (gesty);
  - algorytm A: znajdowanie cyklu Eulera   (algorytm Hierholzera, O(E)),
  - algorytm B: znajdowanie pierwszego cyklu Hamiltona z powracaniem (backtracking),
  - pomiar czasu obu algorytmow w 15 punktach pomiarowych i dwa wykresy t = f(n)
    (wykres 1 -> nasycenie 30%, wykres 2 -> nasycenie 70%).

Generator grafu pochodzi z graph_generator.py (import ponizej).
"""

import sys
import time

import matplotlib.pyplot as plt

from graph_generator import generate_graph, degree, edge_count, is_connected


# ============================================================
#  ALGORYTM A - cykl Eulera (algorytm Hierholzera)
# ============================================================

def euler_cycle(adj, n):
    """
    Zwraca cykl Eulera jako liste wierzcholkow [v0, v1, ..., v0].
    Zaklada graf spojny o wszystkich stopniach parzystych (eulerowski).
    Dziala na kopii macierzy - krawedzie sa usuwane w trakcie.
    Zlozonosc: O(n * E) przy reprezentacji macierzowej.
    """
    A = [row[:] for row in adj]          # kopia macierzy (nie niszczymy oryginalu)
    nxt = [0] * n                        # wskaznik od ktorego sasiada zaczac szukanie
    stack = [0]
    cycle = []

    while stack:
        v = stack[-1]
        # szukamy nieuzytej krawedzi wychodzacej z v
        u = nxt[v]
        while u < n and A[v][u] == 0:
            u += 1
        nxt[v] = u
        if u == n:                       # brak krawedzi -> zamykamy fragment
            cycle.append(stack.pop())
        else:
            A[v][u] = A[u][v] = 0         # zuzywamy krawedz v-u
            stack.append(u)

    cycle.reverse()
    return cycle


# ============================================================
#  ALGORYTM B - pierwszy cykl Hamiltona (backtracking)
# ============================================================

def hamilton_cycle(adj, n):
    """
    Znajduje PIERWSZY cykl Hamiltona metoda z powracaniem.
    Zwraca liste [v0, v1, ..., v0] albo None, jesli cyklu nie ma.
    Zlozonosc: wykladnicza w najgorszym przypadku.
    """
    visited = [False] * n
    path = [0]
    visited[0] = True

    def backtrack(v):
        if len(path) == n:               # odwiedzilismy wszystkie wierzcholki
            return adj[v][0] == 1         # czy mozemy domknac cykl do startu?
        for u in range(n):
            if adj[v][u] and not visited[u]:
                visited[u] = True
                path.append(u)
                if backtrack(u):
                    return True
                path.pop()
                visited[u] = False
        return False

    if backtrack(0):
        return path + [0]
    return None


# ============================================================
#  POMIAR CZASU
# ============================================================

def time_algorithm(func, adj, n, repeats):
    """Uruchamia func(adj, n) `repeats` razy i zwraca najlepszy (najmniejszy) czas [s]."""
    best = float("inf")
    for _ in range(repeats):
        t0 = time.perf_counter()
        func(adj, n)
        dt = time.perf_counter() - t0
        if dt < best:
            best = dt
    return best


def make_graph(n, saturation, base_seed):
    """
    Generuje graf, probujac kolejnych seedow - generator bywa kapryśny
    dla malych/rzadkich przypadkow i czasem nie domyka naprawy parzystosci.
    """
    seed = base_seed
    for _ in range(100):
        try:
            return generate_graph(n, saturation, seed=seed)
        except RuntimeError:
            seed += 1000
    raise RuntimeError(f"Nie udalo sie wygenerowac grafu dla n={n}, sat={saturation}.")


def measure(n_values, saturation, euler_repeats=5, graphs_per_n=3):
    """
    Dla kazdego n generuje `graphs_per_n` grafow o zadanym nasyceniu,
    mierzy czas algorytmu A i B i zwraca usrednione czasy [ms].
    """
    euler_ms, hamilton_ms = [], []
    for n in n_values:
        e_acc, h_acc = 0.0, 0.0
        for s in range(graphs_per_n):
            adj = make_graph(n, saturation, base_seed=100 + s)
            e_acc += time_algorithm(euler_cycle, adj, n, euler_repeats)
            h_acc += time_algorithm(hamilton_cycle, adj, n, 1)   # B - jednokrotnie (drogie)
        euler_ms.append(1000.0 * e_acc / graphs_per_n)
        hamilton_ms.append(1000.0 * h_acc / graphs_per_n)
        print(f"  n={n:3d} | A (Euler)={euler_ms[-1]:9.4f} ms"
              f" | B (Hamilton)={hamilton_ms[-1]:11.4f} ms")
    return euler_ms, hamilton_ms


# ============================================================
#  WYKRESY
# ============================================================

def plot_chart(n_values, euler_ms, hamilton_ms, saturation, filename):
    plt.figure(figsize=(9, 6))
    plt.plot(n_values, euler_ms, "o-", color="tab:blue",
             label="Algorytm A - cykl Eulera (Hierholzer)")
    plt.plot(n_values, hamilton_ms, "s-", color="tab:red",
             label="Algorytm B - cykl Hamiltona (backtracking)")
    plt.xlabel("liczba wierzcholkow n")
    plt.ylabel("czas dzialania t [ms]")
    plt.title(f"t = f(n) dla nasycenia {saturation:.0%}")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=120)
    print(f"  zapisano wykres: {filename}")
    plt.close()


# ============================================================
#  MAIN
# ============================================================

if __name__ == "__main__":
    sys.setrecursionlimit(10000)

    # 15 punktow pomiarowych - ten sam, bezpieczny zakres n dla obu nasycen.
    # Pomijamy n=5 (niegenerowalne przy 70%) oraz n=9 (niegenerowalne przy 30%) -
    # dla tak malej liczby krawedzi generator nie domyka warunku parzystosci stopni.
    # Gorna granica n=20: backtracking Hamiltona przy 30% jest jeszcze szybki,
    # przy n>=22 czas potrafi gwaltownie rosnac (charakter wykladniczy).
    N_VALUES = [4, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]   # 15 punktow

    print("Nasycenie 30% (graf rzadki):")
    e30, h30 = measure(N_VALUES, 0.30)
    print("\nNasycenie 70% (graf gesty):")
    e70, h70 = measure(N_VALUES, 0.70)

    print()
    plot_chart(N_VALUES, e30, h30, 0.30, "wykres_30.png")
    plot_chart(N_VALUES, e70, h70, 0.70, "wykres_70.png")
    print("\nGotowe.")