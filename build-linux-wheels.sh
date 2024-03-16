#!/bin/bash

# Install dependencies inside the Docker container
yum install -y python3 python3-pip

# Install wheel and setuptools
pip3 install wheel setuptools

# Install Cython
pip3 install Cython

# Build the wheels
for PYBIN in /opt/python/cp3{6,7,8,9,10}*/bin; do
    "${PYBIN}/python" -m pip install -r /io/requirements.txt
    "${PYBIN}/pip" wheel /io/ -w /io/wheelhouse/
done

# Bundle the wheel files
for whl in $(find /io/wheelhouse -name "*.whl"); do
    auditwheel repair "$whl" --plat manylinux2014_x86_64 -w /io/dist/
done

# Install the repaired wheels using pip
pip3 install /io/dist/*.whl
