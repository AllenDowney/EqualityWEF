# Makefile for building and deploying JupyterBook

.PHONY: help build clean deploy

help:
	@echo "Available commands:"
	@echo "  make build    - Build the JupyterBook"
	@echo "  make clean    - Clean build artifacts"
	@echo "  make deploy   - Build and deploy to GitHub Pages"
	@echo "  make serve    - Build and serve locally"

build:
	jupyter book build --html --strict

clean:
	rm -rf _build

deploy: build
	ghp-import -n -p -f _build/html

serve: build
	cd _build/html && python -m http.server 8000

