'''
Złożoność czasowa wynosi zawsze O(n²)
niezależnie od danych wejściowych. Algorytm zawsze wykonuje
tyle samo porównań, bo dla każdego elementu przeszukuje cały pozostały fragment tablicy.
'''



def selection_sort(lista, dlugosc):
    for i in range(dlugosc - 1):
        m_index = i

        for j in range(i+1, dlugosc):
            if lista[j] < lista[m_index]:
                m_index = j
        #Najmniejszy element z listy i potem szuka kolejnego
        #return lista[m_index]


        '''
        To jest jednoczesna zamiana wartości (swap) dwóch elementów listy.
        
          W Pythonie to samo robisz w jednej linii, bo Python najpierw oblicza całą prawą stronę, a dopiero potem przypisuje wartości po lewej. Dzięki temu nic się nie nadpisze "za wcześnie".                                                                                                                          
                                                                                                                                                                                                                                                                                                                   
            Przykład:                                                                                                                                                                                                                                                                                                      
            lista = [7, 3, 5]                                                                                                                                                                                                                                                                                                
            i = 0        # lista[0] = 7
            m_index = 1  # lista[1] = 3                                                                                                                                                                                                                                                                                      
             
            lista[i], lista[m_index] = lista[m_index], lista[i]                                                                                                                                                                                                                                                              
            # → lista = [3, 7, 5]

        '''
        lista[i],  lista[m_index] = lista[m_index],  lista[i]





if __name__ == '__main__':
    lista = [-2, 45, 0, 11, -9, 88, -97, -202, 747]
    dlugosc = len(lista)
    selection_sort(lista, dlugosc)
    #print(selection_sort(lista, dlugosc))
    print(lista)