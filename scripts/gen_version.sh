#!/usr/bin/env bash

version=$(git describe --exact-match --tags HEAD 2>/dev/null)

if [[ -z "$version" ]]; then
    version=$(git describe --tags --always)
    git_hash=$(git rev-parse --verify --short HEAD)
    if [[ "${version}" == "${git_hash}" ]]; then
        version="v0.0.0_dev$(git rev-list --count HEAD).sha.${git_hash}"
    else
        previous_version=$(git describe --abbrev=0 --tags)
        distance=$(git rev-list --count HEAD..."${previous_version}")
        version="${previous_version}_dev${distance}.sha.${git_hash}"
    fi
fi

echo "$version"
