from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import os
import glob

# Directory containing your package
directory_path = os.path.dirname(os.path.abspath(__file__))
package_path = os.path.join(directory_path, 'miksi_ai_sdk')

# Function to read the list of requirements from requirements.txt
def load_requirements(filename='requirements.txt'):
    with open(os.path.join(directory_path, filename), 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to get all .py files for compilation
def find_py_files(directory):
    py_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                module_name = os.path.relpath(os.path.join(root, file), directory).replace(os.path.sep, '.')[:-3]
                py_files.append((module_name, os.path.join(root, file)))
    return py_files

# Create Cython extensions for each .py file
extensions = [Extension(f"miksi_ai_sdk.{module}", [f]) for module, f in find_py_files(package_path)]

setup(
    name="miksi-ai-sdk",
    version="0.0.18",
    author="RichardKaranuMbuti",
    author_email="officialforrichardk@gmail.com",
    description="Miksi-AI empowers your BI",
    long_description=open(os.path.join(directory_path, 'docs.md')).read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Miksi-io/Custom-Agent",
    packages=find_packages(include=["miksi_ai_sdk", "miksi_ai_sdk.*"]),
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
    install_requires=load_requirements(),
    python_requires='>=3.6',
    classifiers=[
        # Add your classifiers here
    ],
)