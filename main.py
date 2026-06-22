import sys
from address import *
from TLB import TLB
from PageTable import PageTable

# Parâmetros lidos do terminal
ADDRESS_FILE    = sys.argv[1]
QUADROS         = int(sys.argv[2])
ALGORITMO_SUB   = sys.argv[3]

CAPACIDADE_MEMORIA_FISICA = 65536
TAMANHO_PAGINA = CAPACIDADE_MEMORIA_FISICA // QUADROS

tlb = TLB(capacidade= 16, algoritmo= ALGORITMO_SUB)
page_table = PageTable()
ram = RAM()


with open("correct.txt", "w") as result:
    with open(ADDRESS_FILE, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            
            if linha == "PageTable":
                page_table.show(result)

            elif linha == "TLB": 
                tlb.show(result)

            else:
                logical_address = int(linha)
                page_number, offset = conversor_logical_address(TAMANHO_PAGINA, logical_address)

                frame_number = tlb.lookup(page_number)

                # TLB Hit!!
                if frame_number is not None:
                    physical_address = montar_physical_address(TAMANHO_PAGINA, frame_number, offset)
                    conteudo = ram[physical_address]
                    # result.write(conteudo e enderecos conforme o padrao)
                    continue

                # TLB Miss
                frame_number = page_table.lookup(page_number)

                # PageTable Hit!!
                if frame_number is not None:
                    tlb.update(page_number, frame_number)
                    physical_address = montar_physical_address(TAMANHO_PAGINA, frame_number, offset)
                    conteudo = ram[physical_address]
                    # result.write(conteudo e enderecos conforme o padrao)
                    continue

                # PageFault
                frame_number = ram.ler_backing_store(page_number, TAMANHO_PAGINA, ALGORITMO_SUB)
                page_table.update()
                tlb.update(page_number, frame_number)
                
                physical_address = montar_physical_address(TAMANHO_PAGINA, frame_number, offset)
                conteudo = ram[physical_address]
                # result.write(conteudo e enderecos conforme o padrao)


    tlb_hit = tlb.get_hit_rate()
    page_fault = page_table.get_page_fault_rate()
    result.write("\n\nTAXA DE TLB HIT: " + tlb_hit + "%\n")
    result.write("TAXA DE PAGE-FAULT: " + page_fault + "%")



#### ------- FLUXO --------- ####

# 1. Ler parâmetros terminal QUADROS e ALGORITMO_SUBS

# 2. Inicializar TLB, PageTable e RAM

# 3. Abrir arquivo address.txt

# 4. Enquanto EOF de address.txt faça
#
#   Ler endereço lógico
#   Separar page_number e offset
#   Lookup em TLB
#
#       Em caso de TLB Hit
#           Receber frame_number
#           Montar endereço = page_number + offset
#           Ler na RAM 
#           FIM!!!!
#       
#       Em caso de TLB Miss
#           Lookup em PageTable
#               Em caso de PageTable Hit
#                   Receber frame_number
#                   Update em TLB
#                   Montar endereço = page_number + offset
#                   Ler na RAM
#                   FIM!!!!
#               Em caso de PageFault
#                   Abrir BACKING_STORE.bin
#                   fseek e fread
#                   Copiar 256 bytes pra RAM
#                   Update PageTable e TLB
#                   FIM!!!!

# 5. Mostrar estatisticas taxa de PageFault e de TLB hit