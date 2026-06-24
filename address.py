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
    Retorna o endereco fisico na RAM montado a partir do frame_number e offset.
    """
    BITS_OFFSET = int(math.log2(tam_pagina))
    physical_address = (frame_number << BITS_OFFSET) | offset
    return physical_address


def registrar_endereco_conteudo(arquivo, logical_address, physical_address, conteudo):
    """
    Escreve no arquivo passado por parametro os enderecos logicos e fisicos, alem do conteudo na memoria.
    """
    arquivo.write(f"Endereco Virtual: {logical_address}  Endereco Fisico: {physical_address}  Conteudo: {conteudo}\n")


def mostrar_taxas(arquivo, tlb, page_table, total_enderecos):
    """
    Escreve as estatisticas e taxas no arquivo result (correct.txt).
    """
    tlb_hit_rate = tlb.get_hit_rate()
    tlb_hits = tlb.get_tlb_hit_count()
    page_faults = page_table.get_page_fault_count()

    page_fault_rate = (page_faults / total_enderecos) * 100

    arquivo.write(f"\n\n\n\n====================================================")
    arquivo.write(      f"\n============== ESTATISTICAS SIMULADOR ==============")
    arquivo.write(      f"\n====================================================\n\n")

    arquivo.write(f"TOTAL DE ACESSOS/ENDERECOS: {total_enderecos}\n\n")

    arquivo.write(f"QUANTIDADE DE TLB HIT:      {tlb_hits}\n")
    arquivo.write(f"TAXA DE TLB HIT:            {tlb_hits} / {total_enderecos} = {tlb_hit_rate:.2f}%\n\n")
    
    arquivo.write(f"QUANTIDADE DE PAGE FAULT:   {page_faults}\n")
    arquivo.write(f"TAXA DE PAGE-FAULT:         {page_faults} / {total_enderecos} = {page_fault_rate:.2f}%")