from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import os
from glob import glob

# Determine the directory in which this setup file resides.
directory_path = os.path.abspath(os.path.dirname(__file__))

def load_requirements(filename='requirements.txt'):
    with open(os.path.join(directory_path, filename), 'r') as file:
        requirements = [line.strip() for line in file.readlines()]
    return requirements

# Automatically compile all .py files in the miksi_ai_sdk directory.
cython_modules = glob('miksi_ai_sdk/*.py')
extensions = [
    Extension(
        name=os.path.splitext(os.path.basename(py_file))[0],
        sources=[py_file]
    ) for py_file in cython_modules
]

setup(
    name="miksi-ai-sdk",
    version="0.0.18",
    author="RichardKaranuMbuti",
    author_email="officialforrichardk@gmail.com",
    description="Miksi-AI empowers your BI",
    long_description=open(os.path.join(directory_path, 'docs.md')).read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Miksi-io/Custom-Agent",
    packages=find_packages(),
    install_requires=load_requirements(),
    python_requires='>=3.7, <4',
    ext_modules=cythonize(extensions, compiler_directives={'language_level' : "3"}),
)
