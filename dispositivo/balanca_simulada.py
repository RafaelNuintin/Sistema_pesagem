class BalancaSimulada:

    def __init__(self, peso):
        self.peso = peso

    def ler_peso(self):
        return self.peso
    
balanca = BalancaSimulada(12.47)

peso = balanca.ler_peso()

print(peso)