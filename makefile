build:
	python3 -m PyInstaller main.py
	mkdir dist/main/data
	cp data/* dist/main/data/

run:
	python3 main.py

clean:
	rm -r build/*
	rm -r dist/*

.PHONY: build
