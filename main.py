import sys
from address import *
from TLB import TLB
from PageTable import PageTable
from RAM import RAM

ADDRESS_FILE    = sys.argv[1]
QUADROS         = int(sys.argv[2])
ALGORITMO_SUB   = sys.argv[3]

TAMANHO_PAGINA              = 256
CAPACIDADE_MEMORIA_FISICA   = QUADROS * TAMANHO_PAGINA
PATH_SAIDA                  = "saida/correct.txt"

tlb         = TLB(16, ALGORITMO_SUB)
page_table  = PageTable(256)       
ram         = RAM(QUADROS, CAPACIDADE_MEMORIA_FISICA, ALGORITMO_SUB)

total_enderecos = 0

with open(PATH_SAIDA, "w") as result:
    with open(ADDRESS_FILE, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            
            if linha == "PageTable":
                page_table.show(result)

            elif linha == "TLB": 
                tlb.show(result)

            else:
                total_enderecos += 1

                logical_address = int(linha)
                page_number, offset = conversor_logical_address(TAMANHO_PAGINA, logical_address)
                print(
                    f"logical={logical_address}, "
                    f"page={page_number}, "
                    f"offset={offset}"
                )

                frame_number = tlb.lookup(page_number)

                # TLB Hit!!

                if frame_number is not None:
                    if ALGORITMO_SUB == "LRU": ram.registrar_acesso(frame_number)

                    physical_address = montar_physical_address(TAMANHO_PAGINA, frame_number, offset)
                    conteudo = ram.get_conteudo(physical_address)
                    registrar_endereco_conteudo(result, logical_address, physical_address, conteudo)
                    continue

                # TLB Miss -> lookup em PageTable

                frame_number = page_table.lookup(page_number)

                # PageTable Hit!!

                if frame_number is not None:
                    if ALGORITMO_SUB == "LRU": ram.registrar_acesso(frame_number)

                    tlb.update(page_number, frame_number)
                    physical_address = montar_physical_address(TAMANHO_PAGINA, frame_number, offset)
                    conteudo = ram.get_conteudo(physical_address)
                    registrar_endereco_conteudo(result, logical_address, physical_address, conteudo)
                    continue

                # PageFault -> ler no BACKING_STORE.bin

                frame_number = ram.ler_backing_store(page_number, TAMANHO_PAGINA, page_table, tlb)
                
                physical_address = montar_physical_address(TAMANHO_PAGINA, frame_number, offset)
                conteudo = ram.get_conteudo(physical_address)
                registrar_endereco_conteudo(result, logical_address, physical_address, conteudo)


    mostrar_taxas(result, tlb, page_table, total_enderecos)



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