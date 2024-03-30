
from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import os
import subprocess

directory_path = '.'

def load_requirements(filename='requirements.txt'):
    with open(os.path.join(directory_path, filename), 'r') as file:
        return [line.strip() for line in file.readlines()]

# List of Cython extensions to be compiled
extensions = [
    Extension(name="miksi_ai_sdk.agent", sources=["miksi_ai_sdk/agent.py"]),
    Extension(name="miksi_ai_sdk.api", sources=["miksi_ai_sdk/api.py"]),
    Extension(name="miksi_ai_sdk.master", sources=["miksi_ai_sdk/master.py"]),
    Extension(name="miksi_ai_sdk.pythontool", sources=["miksi_ai_sdk/pythontool.py"]),
    Extension(name="miksi_ai_sdk.sqltool", sources=["miksi_ai_sdk/sqltool.py"]),
    Extension(name="miksi_ai_sdk.utils", sources=["miksi_ai_sdk/utils.py"]),
    # Add other extensions as needed
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
    # It is also common to include package data, which could include compiled .so files,
    # if they were compiled separately and not as part of the build process.
)