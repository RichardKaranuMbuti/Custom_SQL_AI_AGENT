#!/bin/bash

# Compile wheels
for PYBIN in /opt/python/cp3{6,7,8,9}*/bin; do
    "${PYBIN}/pip" wheel /io/ -w /io/dist/
done

# Bundle external shared libraries into the wheels
for whl in /io/dist/*.whl; do
    auditwheel repair "$whl" -w /io/dist/
done

# Set permissions to allow uploading to PyPI
chmod 666 /io/dist/*
