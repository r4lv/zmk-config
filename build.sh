#!/bin/bash
if [ -z "$1" ]; then
    # shellcheck disable=SC2054
    args=(
        --mount "type=bind,source=${PWD}/../zmk,target=/workspaces/zmk,consistency=cached"
        --mount type=volume,source=zmk-root-user,target=/root
        --mount type=volume,source=zmk-config,target=/workspaces/zmk-config
        --mount type=volume,source=zmk-zephyr,target=/workspaces/zmk/zephyr
        --mount type=volume,source=zmk-zephyr-modules,target=/workspaces/zmk/modules
        --mount type=volume,source=zmk-zephyr-tools,target=/workspaces/zmk/tools
        -e WORKSPACE_DIR=/workspaces/zmk
        --entrypoint /bin/sh
        -t  # attach tty -> colours in output
        -i  # interactive (allow ctrl-c to stop container)
        docker.io/zmkfirmware/zmk-dev-arm:3.2  # same as zmk/.devcontainer/Dockerfile
        -c "/workspaces/zmk-config/build.sh inside_docker"
    )

    docker run "${args[@]}"
elif [ "$1" = "inside_docker" ]; then
    set -e

    cd /workspaces/zmk/app

    west init -l /workspaces/zmk/app || true
    west update
    west zephyr-export

    west build /workspaces/zmk/app -d build/left  -b nice_nano_v2 -- -DSHIELD=corne_left  -DZMK_CONFIG=/workspaces/zmk-config/config
    west build /workspaces/zmk/app -d build/right -b nice_nano_v2 -- -DSHIELD=corne_right -DZMK_CONFIG=/workspaces/zmk-config/config

    mkdir -p /workspaces/zmk-config/firmware
    cp build/left/zephyr/zmk.uf2  /workspaces/zmk-config/firmware/left.uf2
    cp build/right/zephyr/zmk.uf2  /workspaces/zmk-config/firmware/right.uf2

    echo "successfully generated zmk-config/firmware/{left,right}.uf2"
fi

