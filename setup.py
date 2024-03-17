from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import os
from os.path import join
import glob

# Directory containing your miksisdk package
directory_path = os.path.dirname(os.path.abspath(__file__))
miksisdk_path = join(directory_path, 'miksi_ai_sdk')

# Function to get all .py files except __init__.py from miksisdk directory
def get_py_files(directory):
    return [f for f in glob.glob(join(directory, '**/*.py'), recursive=True)
            if not f.endswith('__init__.py')]

# Get all .py files to be cythonized
miksisdk_files = get_py_files(miksisdk_path)

# Create extensions for each .py file
extensions = [
    Extension(
        name=os.path.splitext(os.path.relpath(file, directory_path))[0].replace(os.path.sep, '.'),
        sources=[file],
        include_dirs=[directory_path]  # Ensure this is adjusted or removed based on your needs
    ) for file in miksisdk_files
]

setup(
    name="miksi_ai_sdk",
    version="0.0.6",
    author="RichardKaranuMbuti",
    author_email="officialforrichardk@gmail.com",
    description="Miksi-AI empowers your BI",
    long_description=open(os.path.join(directory_path, 'docs.md')).read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Miksi-io/Custom-Agent",
    packages=find_packages(),
    ext_modules=cythonize(extensions, language_level="3"),
    install_requires=[
        "Cython", "langchain", "sqlalchemy", "pymysql",
        "langchain_openai", "openai"
    ],
    python_requires='>=3.6',
    classifiers=[
        # Add all relevant classifiers here
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

'''
import os
from os.path import join
from setuptools import setup, Extension
from Cython.Build import cythonize
import glob

# Directory containing your miksisdk package
directory_path = os.path.dirname(os.path.abspath(__file__))
miksisdk_path = join(directory_path, 'miksi_ai_sdk')

# Function to get all .py files from miksisdk directory
def get_py_files(directory):
    return glob.glob(join(directory, '*.py'))

# Get all .py files to be cythonized
miksisdk_files = get_py_files(miksisdk_path)

# Create extensions for each .py file
extensions = [
    Extension(
        name=os.path.splitext(os.path.relpath(file, directory_path))[0].replace(os.path.sep, '.'),
        sources=[file]
    ) for file in miksisdk_files
]

setup(
    name="miksi_ai_sdk",
    version="0.0.4",
    install_requires=[
        "pip", "setuptools", "langchain", "sqlalchemy", "pymysql",
         "langchain", "langchain_openai","openai", "Cython"
    ],
     long_description=open('docs.md').read(),
    long_description_content_type='text/markdown',
    ext_modules=cythonize(extensions, language_level="3")
)
'''