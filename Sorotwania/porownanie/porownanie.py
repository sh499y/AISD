import random
import time

#Wraper do mierzenia czasu
def mierz_czasu(funkcja):
    def wrapper(*args, **kwargs):
        start = time.time()
        wynik = funkcja(*args, **kwargs)
        koniec = time.time()
        print(f"{funkcja.__name__} zajelo: {koniec - start:.4f}s")
        return wynik

    return wrapper

@mierz_czasu
def insertion_sort(lista):
    for i in range(1, len(lista)):
        key = lista[i]
        j = i - 1

        while j >= 0 and key < lista[j]:
            lista[j + 1] = lista[j]
            j = j - 1

        lista[j + 1] = key


if __name__ == '__main__':
    #ustawienie tego samego seed sprawia ze kazdy algorytm ma taka sama szanse
    SEED = 0
    random.seed(SEED)

    ilsoc = [500, 1000, 2000, 3000, 4000, 5000, 30000, 50000]

    for i in range(0, len(ilsoc)):
        lista = [random.random() for _ in range(ilsoc[i])]
        insertion_sort(lista)
    #print(lista)