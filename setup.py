import os
from setuptools import setup, find_packages

# Directory containing your miksisdk package
directory_path = os.path.dirname(os.path.abspath(__file__))

setup(
    name="miksi_ai_sdk",
    version="0.0.5",
    description="Miksi-AI empowers your BI",
    long_description=open(os.path.join(directory_path, 'docs.md')).read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Miksi-io/Custom-Agent",
    author="RichardKaranuMbuti",
    author_email="officialforrichardk@gmail.com",
    packages=find_packages(),
    install_requires=[
        "langchain", "sqlalchemy", "pymysql",
        "langchain_openai", "openai"
    ],
    python_requires='>=3.6',
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