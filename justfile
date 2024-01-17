_default:
	just --list

build:
	just generate-mapping
	./build-mac.sh

generate-mapping:
	python de-keys/generate_de_key_mapping.py  # generates config/keys_de.h

draw:
	just generate-mapping
	bunx sass --no-source-map keymap-drawer/style.scss keymap-drawer/style.css
	python keymap-drawer/generate_config.py
	keymap -c keymap-drawer/config.gen.yaml parse -z config/corne.keymap > keymap-drawer/corne.gen.yaml
	keymap -c keymap-drawer/config.gen.yaml draw keymap-drawer/corne.gen.yaml > keymap-drawer/corne.svg
	resvg --background white -w 2000 keymap-drawer/corne.svg keymap-drawer/corne.png

draw-watch:
	ls config/* keymap-drawer/config.template.yaml | entr just draw
