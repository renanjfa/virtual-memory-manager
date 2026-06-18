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