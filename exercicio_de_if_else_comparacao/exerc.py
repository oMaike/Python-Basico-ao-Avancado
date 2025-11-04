primeiro_valor = input ('Digite um valor: ')
segundo_valor = input ('Digite um valor: ')

if primeiro_valor > segundo_valor:
    print("primeiro valor é maior que o segundo valor")
elif primeiro_valor < segundo_valor:
    print ("Primeiro valor é maior que  segundo valor")
elif segundo_valor > primeiro_valor:
    print("segundo valor é maior que o primeiro valor")
elif segundo_valor < primeiro_valor:
    print("segundo valor é menor que o primeiro valor")
elif primeiro_valor == segundo_valor:
    print("primeiro valor eh igual ao segundo valor")
elif segundo_valor == primeiro_valor:
    print("segundo valor é igual ao primeiro valor")
else:
    print("digite algum numero")
