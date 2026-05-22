import random
import time

# ustawienie tego samego seed sprawia ze kazdy algorytm ma taka sama szanse
SEED = 0
ilsoc = [500, 1000, 2000, 3000, 4000, 5000, 30000, 50000]


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
def selection_sort(lista, dlugosc):
    for i in range(dlugosc - 1):
        m_index = i

        for j in range(i+1, dlugosc):
            if lista[j] < lista[m_index]:
                m_index = j

        lista[i], lista[m_index] = lista[m_index], lista[i]


@mierz_czasu
def insertion_sort(lista):
    for i in range(1, len(lista)):
        key = lista[i]
        j = i - 1

        while j >= 0 and key < lista[j]:
            lista[j + 1] = lista[j]
            j = j - 1

        lista[j + 1] = key


@mierz_czasu
def bubble_sort(lista):
    n = len(lista)

    #Przejdz przez akzdy element listy
    for i in range(n):
        swapped = False

        for j in range(0, n-i-1):
            if lista[j] > lista[j+1]:
                lista[j], lista[j+1] = lista[j+1], lista[j]
                swapped = True
        if(swapped == False):
            break

if __name__ == '__main__':



    for i in range(3):

        match i:
            case 0:
                print("===Selection Sort===")
                for k in range(len(ilsoc)):
                    random.seed(SEED)
                    lista = [random.random() for _ in range(ilsoc[k])]
                    selection_sort(lista, len(lista))
            case 1:
                print("===Insertion Sort===")
                for k in range(len(ilsoc)):
                    random.seed(SEED)
                    lista = [random.random() for _ in range(ilsoc[k])]
                    insertion_sort(lista)
            case 2:
                print("===Bubble Sort===")
                for k in range(len(ilsoc)):
                    random.seed(SEED)
                    lista = [random.random() for _ in range(ilsoc[k])]
                    bubble_sort(lista)