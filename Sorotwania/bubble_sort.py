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
    lista = [64, 34, 25, 12, 22, 11, 90]
    bubble_sort(lista)
    print(lista)