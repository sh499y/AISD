'''
Sortowanie przez proste wstawianie
'''

def insertion_sort(lista):
    # Zaczynamy od indeksu 1, bo element na pozycji 0 jest juz "posortowany" sam z soba
    for i in range(1, len(lista)):
        # Zapamietujemy aktualny element, ktory chcemy wstawic we wlasciwe miejsce
        key = lista[i]
        # j wskazuje na element tuz przed key - bedziemy porownywac w lewo
        j = i - 1

        # Dopoki nie wyszlismy poza liste (j >= 0)
        # i dopoki element po lewej jest wiekszy od key - przesuwamy go w prawo
        while j >= 0 and key < lista[j]:
            lista[j + 1] = lista[j]  # Przesun element w prawo o jedna pozycje
            j = j - 1  # Przejdz do nastepnego elementu w lewo

        # Wstaw key w znalezione miejsce (tam gdzie petla sie zatrzymala)
        lista[j + 1] = key


if __name__ == '__main__':
    lista = [12, 11, 13, 5, 6]
    # Sortujemy liste (funkcja modyfikuje liste "w miejscu", nic nie zwraca)
    insertion_sort(lista)
    print(lista)
