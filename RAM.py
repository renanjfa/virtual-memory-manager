class RAM:
    def __init__(self, quantidade_quadros):
        self.total_quadros = quantidade_quadros
        self.tamanho_memoria_total = 65536
        
        # Inicializa a memória física linear preenchida por zeros
        self.memoria = bytearray(self.tamanho_memoria_total)
        
        # Array para saber qual página lógica está ocupando cada quadro físico
        # Índice = Número do Quadro | Conteúdo = Número da Página (-1 = Vazio)
        self.quadros_ocupados = [-1] * self.total_quadros
        
        # Estruturas auxiliares para substituição
        self.fila_fifo = []               # Guarda a ordem de carregamento dos frames
        self.historico_lru = []           # Rastreia o uso recente para a política LRU

    def __getitem__(self, physical_address):
        """Permite a sintaxe 'conteudo = ram[physical_address]' no fluxo main."""
        if 0 <= physical_address < self.tamanho_memoria_total:
            # Retorna o valor numérico puro armazenado no byte
            return self.memoria[physical_address]
        raise IndexError("Endereço físico fora dos limites da RAM.")

    def registrar_acesso(self, frame_number):
        """Sinaliza que um frame foi usado (essencial para o algoritmo LRU)."""
        if frame_number in self.historico_lru:
            self.historico_lru.remove(frame_number)
        self.historico_lru.append(frame_number)

    def ler_backing_store(self, page_number, tamanho_pagina, algoritmo, page_table, tlb):
        """
        Trata o Page Fault: Lê do disco, decide onde alocar (usando FIFO/LRU)
        e atualiza as estruturas externas em caso de expulsão.
        """
        # 1. Escolher qual frame físico receberá a página
        frame_escolhido = -1
        
        # Caso A: Ainda existe algum quadro totalmente livre na RAM?
        if -1 in self.quadros_ocupados:
            frame_escolhido = self.quadros_ocupados.index(-1)
            
            # Registra o preenchimento desse novo quadro
            self.quadros_ocupados[frame_escolhido] = page_number
            self.fila_fifo.append(frame_escolhido)
            
        # Caso B: RAM LOTADA! Executar algoritmo de substituição
        else:
            if algoritmo.upper() == "FIFO":
                # Remove o quadro mais antigo da fila
                frame_escolhido = self.fila_fifo.pop(0)
                
            elif algoritmo.upper() == "LRU":
                # O frame menos recentemente usado está no início da lista de histórico
                frame_escolhido = self.historico_lru.pop(0)
            else:
                # Fallback padrão (FIFO) caso passe string inválida
                frame_escolhido = self.fila_fifo.pop(0)

            # Identifica a página "vítima" que residia no quadro escolhido
            pagina_expulsa = self.quadros_ocupados[frame_escolhido]
            
            # CRITICAL STEP: Invalida a página antiga na Page Table e na TLB
            page_table.invalidate(pagina_expulsa)
            tlb.invalidate(pagina_expulsa)  # Certifique-se que sua classe TLB possui o método invalidate()
            
            # O quadro agora passa a pertencer à nova página
            self.quadros_ocupados[frame_escolhido] = page_number
            if algoritmo.upper() == "FIFO":
                self.fila_fifo.append(frame_escolhido)

        # Atualiza o histórico de uso do frame escolhido
        self.registrar_acesso(frame_escolhido)

        # 2. Ler do arquivo binário e jogar no espaço do frame escolhido na RAM
        with open("BACKING_STORE.bin", "rb") as disk:
            # Posiciona o cursor no início da página lógica no disco
            disk.seek(page_number * tamanho_pagina)
            dados_pagina = disk.read(tamanho_pagina)
            
            # Calcula o intervalo linear de bytes correspondente ao frame escolhido na RAM
            inicio_ram = frame_escolhido * tamanho_pagina
            fim_ram = inicio_ram + tamanho_pagina
            
            # Copia os dados lidos do disco diretamente na partição da RAM
            self.memoria[inicio_ram:fim_ram] = dados_pagina

        return frame_escolhido