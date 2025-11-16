"""

introducao ao try/except

try ->  tentar executar o codigo 
except -> ocorreu algum erro ao tentar executar

"""
# print(1234)
# print(456)
# float('a')

numero_str = input("Vou dobrar o numero que vc digitar: ")

try:
    print('STR:', numero_str)
    numero_float = float(numero_str) #casting para float 
    print(f'O dobro de {numero_str} é {numero_float * 2}')
    print('FLOAT: ', numero_float)
except:
    print('Isso nao eh um numero')

# if numero_str.isdigit():
#     numero_float = float(numero_str) #casting para float 
#     print(f'O dobro de {numero_str} é {numero_float * 2}')
# else:
#     print('Isso nao eh um numero')