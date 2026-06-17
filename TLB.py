from collections import OrderedDict

class TLBEntry:
    def __init__(self, page_number, frame_number):
        self.page_number = page_number
        self.frame_number = frame_number


class TLB:
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.tabela = OrderedDict()

        self.hits = 0
        self.misses = 0


    def lookup(self, page_number):
        """
        Busca a pagina na TLB.
        Retorna o frame_number em caso de TLB HIT.
        Retorna None em caso de TLB MISS.
        """
        if page_number in self.tabela:          #    hit !!
            self.hits += 1
            # algoritmo para LRU se precisar
            return self.tabela[page_number]
        
        self.misses += 1            #   miss !!
        return None
    

    def update(self, page_number, frame_number):
        """
        Realiza o update da tabela a depender dos parametros de page_number e frame_number.
        """
        if page_number in self.tabela:
            # algortimo para LRU ou FIFO se precisar
            self.tabela[page_number] = frame_number
            return
        
        if len(self.table) >= self.capacidade:
            # algoritmo de substituicao
            return

        self.tabela[page_number] = frame_number
    

    def clear(self):
        """
        Realiza a limpeza da tabela da TLB.
        """
        self.tabela.clear()


    def get_hit_miss_rate(self):
        """
        Retorna a taxa de hit e miss da TLB.
        return hit_rate, miss_rate
        """
        acessos = self.hits + self.misses
        if acessos == 0:
            return 0.0
        
        hit_rate = (self.hits / acessos) * 100
        miss_rate = (self.misses / acessos) * 100
        
        return hit_rate, miss_rate
            