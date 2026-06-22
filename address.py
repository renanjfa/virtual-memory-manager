import math

def conversor_logical_address(tam_pagina, logical_address):
    """
    Retorna o page_number e offset relativo ao endereco logico passado.
    """
    BITS_OFFSET = int(math.log2(tam_pagina))
    MASK_OFFSET = tam_pagina

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