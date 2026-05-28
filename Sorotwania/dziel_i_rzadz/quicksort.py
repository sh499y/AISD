def divide(lista, high):
    if len(lista) == 1:
        return 0
    else:
        pivot = high
        for i in lista[:-1]:
            if i <= pivot:
                mniejsze.append(i)
            else:
                wieksze.append(i)

if __name__ == '__main__':

    lista = [10, 7, 8, 9, 1, 5]
    high = lista[-1]
    mniejsze = []
    wieksze = []
