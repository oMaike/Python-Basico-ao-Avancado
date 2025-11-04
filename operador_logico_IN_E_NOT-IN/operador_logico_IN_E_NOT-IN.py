#operador in e not in 
# String são iteráveis
# 0 1 2 3 4 
# m a i k e 
# -6-5-4-3-2-1

nome = 'Maike'

#print (nome[3])
#print(nome[2])

#print ('a' in nome)
#print (10 * '-')
#print ('Mai' not in nome)
#print ('mai')
#print ('z' in nome)

nome = input ('Digite seu nome ')
encontrar = input('Digite o que deseja encontrar ')

if encontrar in nome:
    print(f'{encontrar} esta em {nome}')
else:
    print (f'{encontrar} nao esta em {nome}')

    
