CAPACIDADE_RAM = 65536
TAMANHO_PAGINA = 512  # Altere para o tamanho da página do seu teste atual
TOTAL_PAGINAS = CAPACIDADE_RAM // TAMANHO_PAGINA

with open("BACKING_STORE.bin", "wb") as f:
    for page_num in range(TOTAL_PAGINAS):
        # Cria um bloco de bytes onde cada byte contém o número da página atual
        # Ex: Na página 5, todos os 512 bytes terão o valor numérico 5
        bloco_de_bytes = bytes([page_num % 256] * TAMANHO_PAGINA)
        f.write(bloco_de_bytes)

print(f"Novo BACKING_STORE.bin gerado com sucesso!")
print(f"Cada bloco de {TAMANHO_PAGINA} bytes contém o número da sua respectiva página.")