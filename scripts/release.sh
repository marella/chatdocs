#!/usr/bin/env sh

set -eu
cd "$(dirname "$0")"
cd ..

if [ -n "$(git status --porcelain)" ]; then
    echo "Project has uncommitted changes."
    exit 1
fi

trap clean EXIT

clean() {
    rm -r build dist *.egg-info || true
}

clean
python3 setup.py sdist bdist_wheel
twine upload dist/*
