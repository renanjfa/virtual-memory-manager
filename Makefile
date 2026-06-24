PYTHON = python3
MAIN = main.py

.PHONY: all clean

all: simulador

simulador:
	@echo '#!/bin/bash' > simulador
	@echo '$(PYTHON) $(MAIN) "$$@"' >> simulador
	@chmod +x simulador
	@echo "Executável criado: ./simulador"
	@echo "Executar como: ./simulador <ADDRESS.TXT> <QUADROS> <ALGORTIMO_SUB>"

clean:
	rm -f simulador
	rm -rf __pycache__
	rm -f *.pyc
	rm -f output.txt
	@echo "Ficheiros temporários removidos."