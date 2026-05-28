def divide(lista):
    if len(lista) <= 1:
        return lista

    pivot = lista[-1] #Ostatni element z listy jest zawzze moim pivotem
    mniejsze = []
    wieksze = []

    #porownywanie
    for i in lista[:-1]: #o jeden element mniej zeby nie brac pivot
        if i <= pivot:
            mniejsze.append(i)
        else:
            wieksze.append(i)

    return divide(mniejsze) + [pivot] + divide(wieksze)



if __name__ == '__main__':

    lista = [10, 7, 8, 9, 1, 5]
    print(divide(lista))
