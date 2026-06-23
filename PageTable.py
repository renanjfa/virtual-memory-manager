class PageTable:
    def __init__(self, num_quadros):
        # O número de entradas na tabela de páginas é proporcional ao mapeamento
        # Assumindo espaço de endereçamento de 16-bits (65536 bytes)
        self.total_paginas = num_quadros 
        
        # Inicializa mapeamento: página -> frame. -1 significa não mapeado (Inválido)
        self.tabela = [-1] * self.total_paginas
        
        # Métricas para estatísticas
        self.total_acessos = 0
        self.page_faults = 0

    def lookup(self, page_number):
        """Busca o frame associado à página lida."""
        self.total_acessos += 1
        
        # Garante que a página requisitada está no escopo válido
        if page_number < 0 or page_number >= self.total_paginas:
            return None
            
        frame = self.tabela[page_number]
        
        if frame == -1:
            self.page_faults += 1
            return None # Page Fault!
            
        return frame

    def update(self, page_number, frame_number):
        """Mapeia uma página lógica para um quadro físico na RAM."""
        if 0 <= page_number < self.total_paginas:
            self.tabela[page_number] = frame_number

    def invalidate(self, page_number):
        """Remove o mapeamento de uma página (usado quando ela é expulsa da RAM)."""
        if 0 <= page_number < self.total_paginas:
            self.tabela[page_number] = -1

    def get_page_fault_rate(self):
        """Calcula e retorna a taxa de page fault em string formatada."""
        if self.total_acessos == 0:
            return "0.0"
        taxa = (self.page_faults / self.total_acessos) * 100
        return f"{taxa:.2f}"

    def show(self, arquivo_write):
        """Escreve o estado atual da Page Table no arquivo especificado."""
        arquivo_write.write("============ PAGE TABLE ============\n")
        arquivo_write.write("Página -> Quadro\n")
        for pagina, quadro in enumerate(self.tabela):
            if quadro != -1:
                arquivo_write.write(f"  {pagina}   ->   {quadro}\n")
        arquivo_write.write("====================================\n")