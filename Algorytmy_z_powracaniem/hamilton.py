"""
Algorytmy z powracaniem - zliczanie WSZYSTKICH cykli Hamiltona.

Zadanie:
  - tworzymy hamiltonowski graf nieskierowany o nasyceniu krawedziami 50%,
  - algorytmem B (przeszukanie wszystkich mozliwych sciezek z powracaniem)
    znajdujemy WSZYSTKIE cykle Hamiltona w grafie,
  - czas dzialania przedstawiamy na wykresie t = f(n).

Pseudokod algorytmu B (poszukiwanie cyklu Hamiltona):
    Hamilton(v)
    {
        V.Add(v);
        dla kazdego nieodwiedzonego sasiada w wierzcholka v
            Hamilton(w);
        if V zawiera wszystkie wierzcholki i istnieje krawedz z v do zrodla
            cykl znaleziony
        else
            V.Remove(v);
    }
W wersji "wszystkie cykle" nie przerywamy po pierwszym trafieniu - przegladamy
caly drzewo przeszukiwan i zliczamy kazdy domkniety cykl.
"""

import random
import sys
import time

import matplotlib.pyplot as plt


# ============================================================
#  GENERATOR hamiltonowskiego grafu nieskierowanego
# ============================================================

def generate_hamiltonian_graph(n, saturation, seed=1):
    """
    Buduje spojny graf nieskierowany zawierajacy cykl Hamiltona,
    o zadanym wspolczynniku nasycenia krawedziami.

    Konstrukcja:
      1) losowy cykl Hamiltona (pierscien po permutacji wierzcholkow)
         -> gwarantuje hamiltonowskosc i spojnosc,
      2) dorzucenie losowych krawedzi az do docelowej liczby (nasycenie).

    Reprezentacja: macierz sasiedztwa (lista list 0/1).
    """
    rng = random.Random(seed)
    adj = [[0] * n for _ in range(n)]

    # 1) cykl Hamiltona = pierscien po losowej permutacji
    order = list(range(n))
    rng.shuffle(order)
    for i in range(n):
        u, v = order[i], order[(i + 1) % n]
        adj[u][v] = adj[v][u] = 1
    edges = n

    # 2) dorzucamy losowe krawedzie do osiagniecia nasycenia
    max_edges = n * (n - 1) // 2
    target = round(saturation * max_edges)
    target = max(target, n)            # co najmniej krawedzie pierscienia
    target = min(target, max_edges)

    possible = [(u, v) for u in range(n) for v in range(u + 1, n) if adj[u][v] == 0]
    rng.shuffle(possible)
    for (u, v) in possible:
        if edges >= target:
            break
        adj[u][v] = adj[v][u] = 1
        edges += 1

    return adj


# ============================================================
#  ALGORYTM B - zliczanie WSZYSTKICH cykli Hamiltona
# ============================================================

def count_hamilton_cycles(adj, n):
    """
    Zwraca liczbe wszystkich cykli Hamiltona znalezionych z powracaniem.
    Start ustalony na wierzcholku 0; kazdy cykl nieskierowany jest liczony
    dwukrotnie (raz w kazda strone) - distinct = wynik // 2.
    """
    start = 0
    visited = [False] * n
    count = 0

    def hamilton(v, depth):
        nonlocal count
        visited[v] = True
        if depth == n:                       # odwiedzono wszystkie wierzcholki
            if adj[v][start] == 1:           # czy domyka sie do zrodla?
                count += 1
        else:
            for w in range(n):
                if adj[v][w] and not visited[w]:
                    hamilton(w, depth + 1)
        visited[v] = False                   # powrot (backtracking)

    hamilton(start, 1)
    return count


# ============================================================
#  POMIAR CZASU
# ============================================================

def measure(n_values, saturation, graphs_per_n=3):
    """
    Dla kazdego n generuje `graphs_per_n` grafow o zadanym nasyceniu,
    zlicza wszystkie cykle Hamiltona i zwraca usredniony czas [ms]
    oraz srednia liczbe znalezionych cykli (distinct).
    """
    times_ms, cycle_counts = [], []
    for n in n_values:
        t_acc, c_acc = 0.0, 0
        for s in range(graphs_per_n):
            adj = generate_hamiltonian_graph(n, saturation, seed=100 + s)
            t0 = time.perf_counter()
            cnt = count_hamilton_cycles(adj, n)
            t_acc += time.perf_counter() - t0
            c_acc += cnt // 2                # distinct cykle nieskierowane
        times_ms.append(1000.0 * t_acc / graphs_per_n)
        cycle_counts.append(c_acc / graphs_per_n)
        print(f"  n={n:3d} | czas={times_ms[-1]:10.4f} ms"
              f" | srednio cykli Hamiltona={cycle_counts[-1]:.1f}")
    return times_ms, cycle_counts


# ============================================================
#  WYKRES
# ============================================================

def plot_chart(n_values, times_ms, saturation, filename):
    plt.figure(figsize=(9, 6))
    plt.plot(n_values, times_ms, "s-", color="tab:red",
             label="Algorytm B - zliczanie wszystkich cykli Hamiltona")
    plt.xlabel("liczba wierzcholkow n")
    plt.ylabel("czas dzialania t [ms]")
    plt.title(f"t = f(n) - wszystkie cykle Hamiltona, nasycenie {saturation:.0%}")
    plt.grid(True, linestyle="--", alpha=0.5)
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

    SATURATION = 0.50

    # Punkty pomiarowe. Zliczanie WSZYSTKICH cykli przeglada cale drzewo
    # przeszukiwan (brak wczesnego wyjscia), wiec czas rosnie wykladniczo
    # bardzo szybko: n=14 ~2 s, n=15 ~11 s, n>=16 sie nie konczy w sensownym
    # czasie. Dlatego gorny zakres ograniczamy do n=14.
    N_VALUES = list(range(3, 15))      # 3, 4, ..., 14  -> 12 punktow

    print(f"Nasycenie {SATURATION:.0%} - zliczanie wszystkich cykli Hamiltona:")
    times, counts = measure(N_VALUES, SATURATION)

    print()
    plot_chart(N_VALUES, times, SATURATION, "hamilton_wszystkie.png")
    print("\nGotowe.")