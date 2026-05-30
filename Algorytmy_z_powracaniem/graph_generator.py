import random

'''
Wyjasnianie syntax output:
  - n = liczba wierzchołków (nodes)
  - m = liczba krawędzi (edges) — obliczana przez edge_count() w linii 91 

'''

def generate_graph(n, saturation, seed=1):
    """
    Generuje spojny graf nieskierowany, ktory jest jednoczesnie:
      - eulerowski  (spojny + wszystkie stopnie parzyste),
      - hamiltonowski (zawiera cykl Hamiltona),
    o zadanym wspolczynniku nasycenia krawedziami.

    Reprezentacja: macierz sasiedztwa (lista list, wartosci 0/1).
    Zwraca: adj  (adj[u][v] == 1  <=>  istnieje krawedz u-v
    """
    rng = random.Random(seed)
    max_edges = n * (n - 1) // 2
    target = round(saturation * max_edges)
    target = max(target, n)          # co najmniej krawedzie cyklu Hamiltona
    target = min(target, max_edges)

    for _ in range(200):             # kilka prob na wypadek utkniecia naprawy parzystosci
        adj = [[0] * n for _ in range(n)]
        ring = set()

        # 1) Cykl Hamiltona = pierscien po losowej permutacji wierzcholkow
        order = list(range(n))
        rng.shuffle(order)
        for i in range(n):
            u, v = order[i], order[(i + 1) % n]
            adj[u][v] = adj[v][u] = 1
            ring.add(frozenset((u, v)))
        edges = n

        # 2) Dorzucamy losowe krawedzie az do docelowej liczby
        possible = [(u, v) for u in range(n) for v in range(u + 1, n) if adj[u][v] == 0]
        rng.shuffle(possible)
        for (u, v) in possible:
            if edges >= target:
                break
            adj[u][v] = adj[v][u] = 1
            edges += 1

        # 3) Naprawa parzystosci stopni (bez ruszania pierscienia)
        if _make_all_even(adj, n, ring):
            return adj

    raise RuntimeError("Nie udalo sie wygenerowac grafu - sprobuj innego seeda lub n.")


def _make_all_even(adj, n, ring):
    """
    Doprowadza wszystkie stopnie do parzystych bez zmiany liczby krawedzi
    i bez ruszania krawedzi pierscienia (cykl Hamiltona + spojnosc zachowane).
    Dla pary nieparzystych u, w: przenosimy krawedz u-x na w-x.
    """
    def odd():
        return [v for v in range(n) if degree(adj, v) % 2 == 1]

    pending = odd()
    while pending:
        u, w = pending[0], pending[1]
        moved = False
        for a, b in ((u, w), (w, u)):           # probujemy w obie strony
            for x in range(n):
                if (adj[a][x] == 1 and x != b
                        and frozenset((a, x)) not in ring
                        and adj[b][x] == 0):
                    adj[a][x] = adj[x][a] = 0    # usun a-x
                    adj[b][x] = adj[x][b] = 1    # dodaj b-x
                    moved = True
                    break
            if moved:
                break
        if not moved:
            return False                          # utkniecie -> ponawiamy generacje
        pending = odd()
    return True


# ---------- funkcje pomocnicze / weryfikacja ----------

def degree(adj, v):
    return sum(adj[v])


def edge_count(adj, n):
    return sum(degree(adj, v) for v in range(n)) // 2


def is_connected(adj, n):
    seen = [False] * n
    stack = [0]
    seen[0] = True
    cnt = 1
    while stack:
        v = stack.pop()
        for u in range(n):
            if adj[v][u] and not seen[u]:
                seen[u] = True
                cnt += 1
                stack.append(u)
    return cnt == n


def verify(adj, n):
    """Sprawdza warunek eulerowski. Hamiltonowskosc jest gwarantowana
    konstrukcyjnie (pierscien), wiec jej nie testujemy (to problem NP-trudny)."""
    conn = is_connected(adj, n)
    all_even = all(degree(adj, v) % 2 == 0 for v in range(n))
    m = edge_count(adj, n)
    sat = m / (n * (n - 1) // 2)
    print(f"n={n:3d} | m={m:4d} | nasycenie={sat:5.1%} | spojny={conn} "
          f"| stopnie parzyste={all_even} | EULEROWSKI={conn and all_even}")
    return conn and all_even


if __name__ == "__main__":
    for n in (8, 15, 30, 60):
        for sat in (0.30, 0.70):
            g = generate_graph(n, sat, seed=42)
            verify(g, n)
        print()