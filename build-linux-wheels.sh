#!/bin/bash

# Install dependencies inside the Docker container
yum install -y python3 python3-pip

# Install wheel and setuptools
pip3 install wheel setuptools

# Check if Cython is installed, and if not, install it
if ! pip3 show Cython &> /dev/null; then
    pip3 install Cython
fi

# Build the wheels
for PYBIN in /opt/python/cp3{6,7,8,9,10}*/bin; do
    "${PYBIN}/python" -m pip install -r /io/requirements.txt
    "${PYBIN}/pip" wheel /io/ -w /io/wheelhouse/
done

# Bundle the wheel files
for whl in /io/wheelhouse/*.whl; do
    auditwheel repair "$whl" --plat manylinux2014_x86_64 -w /io/wheelhouse/
done

# Install the repaired wheels using pip
pip3 install /io/wheelhouse/*.whl
