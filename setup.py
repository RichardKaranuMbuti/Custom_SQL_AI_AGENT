from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import os
import glob

# Directory containing your miksisdk package
directory_path = os.path.dirname(os.path.abspath(__file__))
miksisdk_path = os.path.join(directory_path, 'miksi_ai_sdk')


# Function to read the list of requirements from requirements.txt
def load_requirements(filename='requirements.txt'):
    with open(os.path.join(directory_path, filename), 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to get all .pyx files from miksisdk directory
def get_pyx_files(directory):
    return [f for f in glob.glob(os.path.join(directory, '**/*.py'), recursive=True)]

# Get all .pyx files ------
miksisdk_files = get_pyx_files(miksisdk_path)

# Create Cython extensions for each .pyx file
extensions = [
    Extension(os.path.splitext(os.path.relpath(f, directory_path))[0].replace(os.path.sep, '.'), [f])
    for f in miksisdk_files
]

setup(
    name="miksi-ai-sdk",
    version="0.0.16",
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
    # This line ensures that .py files are not included in your built distributions.
    # Adjust if you have specific non-Cython .py modules you wish to include.
    exclude_package_data={'': ['*.py','*.c', '*.pyx']},
)
