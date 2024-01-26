_default:
	just --list

build:
	just generate-mapping
	./build.sh

build-fast:
	just generate-mapping
	./build.sh --fast

generate-mapping:
	python de-mac/generate_de_key_mapping.py  # generates de-mac/keys_de.h

draw:
	just generate-mapping
	bunx sass@1.54.0 --no-source-map keymap-drawer/style.scss keymap-drawer/style.gen.css
	python keymap-drawer/generate_drawer_config.py
	keymap -c keymap-drawer/config.gen.yaml parse -z config/corne.keymap > keymap-drawer/corne.gen.yaml
	keymap -c keymap-drawer/config.gen.yaml draw keymap-drawer/corne.gen.yaml | sed 's/tabler:/tabler__/g' > keymap-drawer/corne.svg
	resvg --background white -w 2000 keymap-drawer/corne.svg keymap-drawer/corne.png

draw-watch:
	ls config/* keymap-drawer/*template* keymap-drawer/style.scss | entr just draw
