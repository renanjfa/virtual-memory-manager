import sys

class RAM:
    def __init__(self, quantidade_quadros, capacidade, algoritmo):
        self.total_quadros = quantidade_quadros
        self.tamanho_memoria_total = capacidade
        self.algoritmo = algoritmo
        
        self.memoria = bytearray(self.tamanho_memoria_total)
        
        # Array para saber qual página lógica está ocupando cada quadro físico
        # Índice = Número do Quadro | Conteúdo = Número da Página (-1 = Vazio)
        self.quadros_ocupados = [-1] * self.total_quadros
        
        self.fila_fifo = []               
        self.historico_lru = []          


    def get_conteudo(self, physical_address):
        """
        Permite a sintaxe 'conteudo = ram[physical_address]' no fluxo main.
        """
        if 0 <= physical_address < self.tamanho_memoria_total:
            # Retorna o valor numérico puro armazenado no byte
            return self.memoria[physical_address]
        raise IndexError("Endereço físico fora dos limites da RAM.")

    def registrar_acesso(self, frame_number):
        """
        Sinaliza que um frame foi usado (essencial para o algoritmo LRU).
        """
        if frame_number in self.historico_lru:
            self.historico_lru.remove(frame_number)
        self.historico_lru.append(frame_number)

    def ler_backing_store(self, page_number, tamanho_pagina, page_table, tlb):
        """
        Trata o Page Fault: Lê do disco, decide onde alocar (usando FIFO/LRU)
        e atualiza as estruturas externas em caso de expulsão.
        """
        # 1. Escolher qual frame físico receberá a página
        frame_escolhido = -1
        
        # Caso A: Ainda existe algum quadro totalmente livre na RAM?
        if -1 in self.quadros_ocupados:
            frame_escolhido = self.quadros_ocupados.index(-1)
            
            self.quadros_ocupados[frame_escolhido] = page_number
            self.fila_fifo.append(frame_escolhido)
            
        # Caso B: RAM LOTADA! Executar algoritmo de substituição
        else:
            alg = self.algoritmo.upper()

            if alg == "FIFO":
                frame_escolhido = self.fila_fifo.pop(0)
                
            elif alg == "LRU":
                frame_escolhido = self.historico_lru.pop(0)

            else:
                print("ALGORITMO DADO NAO EH CONHECIDO PELO SISTEMA!! TENTE NOVAMENTE COM LRU ou FIFO!!")
                sys.exit()

            pagina_expulsa = self.quadros_ocupados[frame_escolhido]
            
            page_table.invalidate(pagina_expulsa)
            tlb.invalidate(pagina_expulsa)  
            
            self.quadros_ocupados[frame_escolhido] = page_number
            if alg == "FIFO":
                self.fila_fifo.append(frame_escolhido)

        # Atualiza o histórico de uso do frame escolhido
        self.registrar_acesso(frame_escolhido)

        # 2. Ler do arquivo binário e jogar no espaço do frame escolhido na RAM
        with open("BACKING_STORE/BACKING_STORE.bin", "rb") as disk:
            # Posiciona o cursor no início da página lógica no disco
            disk.seek(page_number * tamanho_pagina)
            dados_pagina = disk.read(tamanho_pagina)
            
            # Calcula o intervalo linear de bytes correspondente ao frame escolhido na RAM
            inicio_ram = frame_escolhido * tamanho_pagina
            fim_ram = inicio_ram + tamanho_pagina
            
            # Copia os dados lidos do disco diretamente na partição da RAM
            self.memoria[inicio_ram:fim_ram] = dados_pagina

        page_table.update(page_number, frame_escolhido)
        tlb.update(page_number, frame_escolhido)

        return frame_escolhido