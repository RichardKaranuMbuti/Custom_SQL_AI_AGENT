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
def get_py_files(directory):
    # Adjusted to get .py files for Cython compilation
    return [f for f in glob.glob(os.path.join(directory, '**/*.py'), recursive=True) if not f.endswith('__init__.py')]

# Get all .py files ------
package_files = get_py_files(package_path)

# Create Cython extensions for each .py file
extensions = [
    Extension(os.path.splitext(os.path.relpath(f, directory_path))[0].replace(os.path.sep, '.'), [f])
    for f in package_files
]

setup(
    name="miksi-ai-sdk",
    version="0.0.17",
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
