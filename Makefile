PYTHON = python3
MAIN = main.py
ADDRESS ?=
FRAMES  ?=
ALGO    ?= 

.PHONY: all run clean

all: run

run:
	$(PYTHON) $(MAIN) $(ADDRESS) $(FRAMES) $(ALGO)

clean:
	rm -rf __pycache__
	rm -f *.pyc
	rm -f output.txt
	@echo "Ficheiros temporários removidos."