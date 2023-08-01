# Simulador de alocação sequencial de arquivos
BLOCK_SIZE = 8


class Arquivo:
    def __init__(self, nomeArq, tamArq):
        self.nomeArq = nomeArq
        self.tamArq = tamArq

        if tamArq % 8 > 0:
            self.tamBloco = (tamArq // 8) + 1
        else:
            self.tamBloco = tamArq // 8

        self.blocoI = None
        self.blocoF = None


class Gerenciador:
    def __init__(self):
        # Array disco representa os 256 blocos de 8 bytes do disco
        # Lista com o nome dos arquivos adicionados
        self.disco = [None] * 256
        self.lista_arquivos = []

    def adicionar(self):
        nome = input("Informe o nome do arquivo: ")

        for arquivo in self.lista_arquivos:
            if arquivo.nomeArq == nome:
                print("\nUM ARQUIVO COM ESSE NOME JÁ EXISTE! ESCOLHA OUTRO.")
                return

        tamanho = int(input("Informe o tamanho do arquivo em bytes: "))
        if tamanho <= 0:
            print("\nTAMANHO DE ARQUIVO NÃO VÁLIDO.")

        novo_arquivo = Arquivo(nome, tamanho)
        blocos_necessarios = novo_arquivo.tamBloco
        count = 0

        # Iteração pra saber os blocos iniciais e finais do arquivo
        for i in range(256):
            if self.disco[i] == None:
                count += 1

            if self.disco[i] != None:
                count = 0
                pass

            if count == blocos_necessarios:
                novo_arquivo.blocoF = i
                novo_arquivo.blocoI = i - (blocos_necessarios - 1)
                break

        # Iteração para adicionar o nome do arquivo nos blocos correspondentes do disco
        if novo_arquivo.blocoI != None and novo_arquivo.blocoF != None:
            for i in range(novo_arquivo.blocoI, novo_arquivo.blocoF + 1):
                self.disco[i] = novo_arquivo.nomeArq
            self.lista_arquivos.append(novo_arquivo)
            print(f"\nO ARQUIVO {novo_arquivo.nomeArq} FOI ADICIONADO AO DISCO")
        else:
            print("\nNÃO HÁ ESPAÇO SUFICIENTE")

    def remover(self):
        nome = input("Informe o nome do arquivo: ")
        encontrado = False

        for arquivo in self.lista_arquivos:
            if arquivo.nomeArq == nome:
                for i in range(arquivo.blocoI, arquivo.blocoF + 1):
                    self.disco[i] = None
                self.lista_arquivos.remove(arquivo)
                encontrado = True
                print(f"\nARQUIVO {nome} FOI REMOVIDO!")
                break
        if encontrado == False:
            print(f"\nARQUIVO {nome} NÃO ENCONTRADO!")

    def desfragmentar(self):
        arquivos_ordenados = sorted(self.lista_arquivos, key=lambda x: x.blocoI)
        self.lista_arquivos = arquivos_ordenados

        bloco_atual = 0
        for arquivo in self.lista_arquivos:
            bloco_final = bloco_atual + arquivo.tamArq // BLOCK_SIZE - 1
            if bloco_final >= 256:
                print("\nNÃO HÁ ESPAÇO SUFICIENTE PARA DESFRAGMENTAR TODOS OS ARQUIVOS")
                return
            arquivo.blocoI = bloco_atual
            arquivo.blocoF = bloco_final
            for i in range(bloco_atual, bloco_final + 1):
                self.disco[i] = arquivo.nomeArq
            bloco_atual = bloco_final + 1

        for i in range(bloco_atual, 256):
            self.disco[i] = None

        print("\nDESFRAGMENTAÇÃO CONCLUÍDA")

    def exibir_arquivo(self):
        nome = input("Informe o nome do arquivo: ")
        encontrado = False

        for arquivo in self.lista_arquivos:
            if arquivo.nomeArq == nome:
                print(
                    f"\nNome: {arquivo.nomeArq}\nTamanho: {arquivo.tamArq} bytes\nBlocos: {arquivo.blocoI} - {arquivo.blocoF}\n"
                )
                encontrado = True
                break
        if encontrado == False:
            print(f"\nARQUIVO {nome} NÃO ENCONTRADO!")

    def exibir_disco(self):
        for i in range(256):
            if self.disco[i] == None:
                print(None, end=" ")
            else:
                print(f"[{self.disco[i]}]", end=" ")

            if (i + 1) % 16 == 0:
                print()

    def menu(self):
        while True:
            print("\nO QUE DESEJA FAZER?")
            print("1 - Adicionar um novo arquivo")
            print("2 - Remover um arquivo")
            print("3 - Informações de um arquivo")
            print("4 - Exibir todos os blocos")
            print("5 - defragmentar o disco")
            print("0 - Sair do programa")

            escolha = int(input("\nSUA ESCOLHA: "))

            if escolha == 1:
                print("")
                self.adicionar()
            elif escolha == 2:
                print("")
                self.remover()
            elif escolha == 3:
                print("")
                self.exibir_arquivo()
            elif escolha == 4:
                print("")
                self.exibir_disco()
            elif escolha == 5:
                print("")
                self.desfragmentar()
            elif escolha == 0:
                print("\nFIM DO PROGRAMA")
                input()
                exit()
            else:
                print("\nOPÇÃO INVÁLIDA!")


gerenciador = Gerenciador()
gerenciador.menu()
