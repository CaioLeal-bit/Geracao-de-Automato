from collections import defaultdict

EPSILON = 'ε'

class Automato:
    def __init__(self, estados, alfabeto, transicoes, inicial, estados_aceitacao):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.inicial = inicial
        self.estados_aceitacao = estados_aceitacao

    @classmethod
    def construir_de_entrada(cls):
        # Ler alfabeto
        alfabeto = input("DIGITE OS SÍMBOLOS TERMINAIS (espaçados): ").split()

        # Ler não-terminais (estados)
        nao_terminais = input("DIGITE OS ESTADOS NÃO TERMINAIS (espaçados): ").split()
        inicial = input("DIGITE O ESTADO INICIAL: ").strip()

        # Construir produções
        print("\nDIGITE AS PRODUÇÕES (formato: A -> aB | b | vazio):")
        producoes = {}
        for nt in nao_terminais:
            regras_input = input(f"{nt} -> ")
            regras = [r.strip() for r in regras_input.split('|')]
            producoes[nt] = []
            for regra in regras:
                if regra.lower() == 'vazio':
                    producoes[nt].append((EPSILON, None))
                elif regra:
                    simbolo = regra[0]
                    prox = regra[1:] if len(regra) > 1 else None
                    producoes[nt].append((simbolo, prox))

        # Estados e transições
        estados = set(nao_terminais) | {'F'}
        transicoes = defaultdict(lambda: defaultdict(set))
        estados_aceitacao = set()

        for nt, regras in producoes.items():
            for simbolo, prox in regras:
                if simbolo == EPSILON:
                    estados_aceitacao.add(nt)
                else:
                    destino = prox if prox is not None else 'F'
                    transicoes[nt][simbolo].add(destino)

        estados_aceitacao.add('F')

        return cls(estados, alfabeto, transicoes, inicial, estados_aceitacao)

    def exibir(self):
        print("\n" + "#" * 50)
        print("Representação do Autômato:")

        # Formato L=({Não terminais}, {Terminais}, Transições, Estado inicial, {Estado Final})
        nao_terminais = ", ".join(sorted([estado for estado in self.estados if estado != 'F']))
        terminais = ", ".join(sorted(self.alfabeto))
        estados_finais = ", ".join(sorted(self.estados_aceitacao))

        print(f"L=({{{nao_terminais}}}, {{{terminais}}}, δ, {self.inicial}, {{{estados_finais}}})")

        # Mostrar todas as transições
        print("\nTransições:")
        for origem in sorted(self.transicoes):
            for simbolo, destinos in sorted(self.transicoes[origem].items()):
                simbolo_exibir = simbolo if simbolo != EPSILON else EPSILON
                for destino in sorted(destinos):
                    print(f"  δ({origem}, {simbolo_exibir}) -> {destino}")

        # Mostrar transições ε para aceitação direta
        for estado in sorted(self.estados_aceitacao):
            if estado != 'F' and EPSILON not in self.transicoes.get(estado, {}):
                print(f"  δ({estado}, {EPSILON}) -> ACEITA")

    def testar_palavra(self, palavra):
        atuais = {self.inicial}
        for simbolo in palavra:
            if simbolo not in self.alfabeto:
                return False
            proximos = set()
            for estado in atuais:
                destinos = self.transicoes[estado].get(simbolo, set())
                proximos |= destinos
            atuais = proximos
            if not atuais:
                return False
        return bool(atuais & self.estados_aceitacao)

def main():
    automato = Automato.construir_de_entrada()
    while True:
        print("\n" + "#" * 50)
        print("1 - AUTÔMATO")
        print("2 - TESTAR PALAVRA")
        print("3 - ENCERRAR")
        opcao = input("Escolha: ").strip()

        if opcao == '1':
            automato.exibir()
        elif opcao == '2':
            palavra = input("Escreva a palavra a ser testada: ")
            if automato.testar_palavra(palavra):
                print(f"'{palavra}' → A PALAVRA É ACEITA PELO AUTÔMATO!")
            else:
                print(f"'{palavra}' → A PALAVRA NÃO É ACEITA PELO AUTÔMATO!")
        elif opcao == '3':
            break
        else:
            print("Opção inválida!")

if __name__ == '__main__':
    main()


#Exemplo de Autômato:
# Estados: S B
# Alfabeto: 0 1
# Transições:
#S -> 0B
#B -> 0B | 1S | 0