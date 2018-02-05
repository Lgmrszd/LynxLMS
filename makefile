build:
	python3 -m PyInstaller main.py

run:
	python3 main.py

clean:
	rm -r build/*
	rm -r dist/*

all: build
