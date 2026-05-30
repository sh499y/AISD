def merge(lewa,prawa):
    wynik = []
    i = 0
    j = 0

    while i < len(lewa) and j < len(prawa):
        if lewa[i] <= prawa[j]:
            wynik.append(lewa[i])
            i += 1
        else:
            wynik.append(prawa[j])
            j += 1
    wynik += lewa[i:]
    wynik += prawa[j:]
    return wynik



def mergesort(lista):
    #Dzieli na dwa dopoki rozmiar list nie wynosi 2
    if len(lista) <= 1:
        return lista

    mid = len(lista) // 2
    lewa = mergesort(lista[:mid])
    prawa = mergesort(lista[mid:])


    return merge(lewa,prawa)

if __name__ == '__main__':
    lista = [2,8,5,3,9,4,1,7]

    print(mergesort(lista))