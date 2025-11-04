def saudacao(nome):
    return f"Olá, {nome}! Bem-vindo!"

def calcular_area(largura, altura=1): 
    return largura * altura

nome = input("Digite seu nome: ")
mensagem = saudacao(nome)

largura = float(input("Digite a largura: "))
altura = float(input("Digite a altura: "))

area = calcular_area(largura, altura)

print(mensagem)
print(f"Área {area} metros")
