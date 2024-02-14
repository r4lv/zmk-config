#!/bin/bash
# flags: --fast, to skip init/update of zephyr and modules


if [ "$BUILD_INSIDE_DOCKER_CONTAINER" == "please" ]; then
    set -e

    cd /workspaces/zmk/app
    git config --global --add safe.directory '*'

    if [ "$1" != "--fast" ]; then
        west init -l /workspaces/zmk/app || true
        west update
        west zephyr-export
    fi

    west build /workspaces/zmk/app -d build/left  -b nice_nano_v2 -- -DSHIELD=corne_left  -DZMK_CONFIG=/workspaces/zmk-config/config
    west build /workspaces/zmk/app -d build/right -b nice_nano_v2 -- -DSHIELD=corne_right -DZMK_CONFIG=/workspaces/zmk-config/config

    mkdir -p /workspaces/zmk-config/firmware
    cp build/left/zephyr/zmk.uf2  /workspaces/zmk-config/firmware/left.uf2
    cp build/right/zephyr/zmk.uf2  /workspaces/zmk-config/firmware/right.uf2

    echo "successfully generated zmk-config/firmware/{left,right}.uf2"
else
    if [ ! -d "../zmk" ]; then
        echo "ZMK firmware repo not found"
        exit 1
    fi
    args=(
        --mount "type=bind,source=${PWD}/../zmk,target=/workspaces/zmk,consistency=cached"
        --mount "type=bind,source=${PWD},target=/workspaces/zmk-config"
        -e WORKSPACE_DIR=/workspaces/zmk
        -e BUILD_INSIDE_DOCKER_CONTAINER=please
        --entrypoint /bin/sh
        -t  # attach tty -> colours in output
        -i  # interactive (allow ctrl-c to stop container)
        docker.io/zmkfirmware/zmk-dev-arm:3.5  # same as zmk/.devcontainer/Dockerfile
        -c "/workspaces/zmk-config/build.sh $@"
    )
    docker run "${args[@]}" 
fi
