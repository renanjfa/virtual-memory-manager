class PageTable:
    def __init__(self, num_quadros):
        # O número de entradas na tabela de páginas é proporcional ao mapeamento
        # Assumindo espaço de endereçamento de 16-bits (65536 bytes)
        self.total_paginas = num_quadros 
        
        # Inicializa mapeamento: página -> frame. -1 significa não mapeado (Inválido)
        self.tabela = [-1] * self.total_paginas
        
        self.page_faults = 0


    def lookup(self, page_number):
        """
        Busca o frame associado à página lida.
        """
        
        if page_number < 0 or page_number >= self.total_paginas:
            return None
            
        frame = self.tabela[page_number]
        
        if frame == -1:
            self.page_faults += 1
            return None # Page Fault!
            
        return frame


    def update(self, page_number, frame_number):
        """
        Mapeia o page number para um frame na RAM.
        """
        if 0 <= page_number < self.total_paginas:
            self.tabela[page_number] = frame_number


    def invalidate(self, page_number):
        """
        Remove o mapeamento de uma página, usado quando ela é expulsa da RAM.
        """
        if 0 <= page_number < self.total_paginas:
            self.tabela[page_number] = -1


    def get_page_fault_count(self):
        """
        Calcula e retorna a quantidade de page faults na page table.
        """
        return self.page_faults


    def show(self, arquivo):
        """
        Escreve o estado atual da Page Table no arquivo especificado.
        """
        arquivo.write("\n###########\n")
        arquivo.write("Pagina - Quadro\n")

        for pagina, quadro in enumerate(self.tabela):
            if quadro != -1:
                arquivo.write(f"  {pagina:>2}   ->   {quadro:>2}\n")

        arquivo.write("###########\n\n")