nome = input ('Digite seu nome: ' )
idade = input('Digite sua idade: ')

if nome and idade:
    # nome 
    print(f"Seu nome é {nome}")
    # nome invertido
    print(f"Seu nome invertido é {nome[::-1]}")

    if ' ' in nome:
        print("seu nome tem espaços")
    else:
        print("Seu nome não tem espaços")
    print(f"Seu nome tem {len(nome)} letras")
    print(f"A primeira letra do seu nome é {nome[0]}")
    print(f"A última letra do seu nome é {nome[-1]}")   
else:
    print ("Desculpe, vc deixou sua idade vazia! ")
