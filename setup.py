from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import os
from glob import glob

directory_path = os.path.abspath(os.path.dirname(__file__))

def load_requirements(filename='requirements.txt'):
    with open(os.path.join(directory_path, filename), 'r') as file:
        return [line.strip() for line in file.readlines()]

# Grab all .py files to compile them into Cython extensions
module_pyfiles = glob(os.path.join(directory_path, 'miksi_ai_sdk', '*.py'))

# Create Extensions for Cython to compile
extensions = [
    Extension(name=os.path.splitext(os.path.relpath(pyfile, directory_path))[0].replace(os.path.sep, '.'),
              sources=[pyfile]) for pyfile in module_pyfiles
]

# Use cythonize on the extensions
compiled_extensions = cythonize(extensions, compiler_directives={'language_level': "3"})

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
    python_requires='>=3.6',
    ext_modules=compiled_extensions,
)
