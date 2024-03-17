#!/bin/bash
set -e -x

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    if [[ ${PYBIN} == *"cp38"* ]]; then  # Adjust according to your needs
        "${PYBIN}/pip" install -U pip setuptools wheel Cython
        "${PYBIN}/pip" wheel /github/workspace/ --no-deps -w wheelhouse/
    fi
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" -w /github/workspace/dist/
done

# Fix permissions of the wheels so the host can clean them up
chmod -R a+rwX /github/workspace/dist/