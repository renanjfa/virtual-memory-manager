import math

def conversor_logical_address(tam_pagina, logical_address):
    """
    Retorna o page_number e offset relativo ao endereco logico passado.
    """
    BITS_OFFSET = int(math.log2(tam_pagina))
    MASK_OFFSET = tam_pagina - 1

    page_number = logical_address >> BITS_OFFSET
    offset = logical_address & MASK_OFFSET

    return page_number, offset


def montar_physical_address(tam_pagina, frame_number, offset):
    """
    Retorna o endereco fisico na RAM montado a partir do frame_number e offset
    """
    BITS_OFFSET = int(math.log2(tam_pagina))
    physical_address = (frame_number << BITS_OFFSET) | offset
    return physical_address


def registrar_endereco_conteudo(arquivo, logical_address, physical_address, conteudo):
    """
    Escreve no arquivo passado por parametro os enderecos logicos e fisicos, alem do conteudo na memoria.
    """
    arquivo.write(f"Endereco Virtual: {logical_address}  Endereco Fisico: {physical_address}  Conteudo: {conteudo}\n")