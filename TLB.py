from collections import OrderedDict

class TLBEntry:
    def __init__(self, page_number, frame_number):
        self.page_number = page_number
        self.frame_number = frame_number


class TLB:
    def __init__(self, capacidade, algoritmo):
        self.capacidade = capacidade
        self.tabela = OrderedDict()
        self.algoritmo = algoritmo  # LRU ou FIFO (string: "FIFO" ou "LRU")

        self.hits = 0
        self.misses = 0


    def lookup(self, page_number):
        """
        Busca a pagina na TLB.
        Retorna o frame_number em caso de TLB HIT.
        Retorna None em caso de TLB MISS.
        """
        if page_number in self.tabela:          
            self.hits += 1
            
            if self.algoritmo == "LRU":
                self.tabela.move_to_end(page_number)

            return self.tabela[page_number].frame_number
        
        self.misses += 1            
        return None
    

    def update(self, page_number, frame_number):
        """
        Realiza o update da tabela a depender dos parametros de page_number e frame_number.
        OBS: o update ocorre quando?
            1. TLB miss ( a pagina é buscada na PageTable ) => update é feito com page_number que já tem e frame_number retornado pelo PageTable
            2. TLB miss + Page Fault ( lê o frame do BACKING_STORE.bin, adiciona na RAM, atualiza a PageTable e update na TLB )
        """
        if page_number in self.tabela:
            self.tabela[page_number].frame_number = frame_number

            if self.algoritmo == "LRU":
                self.tabela.move_to_end(page_number)
            return

        if len(self.tabela) >= self.capacidade:
            self.tabela.popitem(last=False)     # remove o primeiro do dicionario ordenado

        nova_entrada = TLBEntry(page_number, frame_number)
        self.tabela[page_number] = nova_entrada


    def invalidate(self, page_number):
        """
        Invalida/Remove a page number da tabela.
        """
        if page_number in self.tabela:
            del self.tabela[page_number]
    

    def clear(self):
        """
        Realiza a limpeza da tabela da TLB.
        """
        self.tabela.clear()


    def get_hit_rate(self):
        """
        Retorna a taxa de hit e miss da TLB.
        return hit_rate, miss_rate
        """
        acessos = self.hits + self.misses
        if acessos == 0:
            return 0.0
        
        hit_rate = (self.hits / acessos) * 100
        
        return hit_rate


    def get_tlb_hit_count(self):
        """
        Retorna a quantidade de TLB hit.
        """
        return self.hits

    def show(self, arquivo):
        """
        Mostra e escreve a TLB e suas entradas. 
        """
        arquivo.write("\n************\n")
        arquivo.write("Pagina - Quadro\n")

        for entrada in self.tabela.values():
            arquivo.write(f"{entrada.page_number:>3}   ->   {entrada.frame_number:<3}\n")

        arquivo.write("************\n\n")

            