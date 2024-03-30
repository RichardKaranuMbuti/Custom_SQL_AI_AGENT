from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import os

def find_cython_extensions(package_dir):
    extensions = []
    for root, dirs, files in os.walk(package_dir):
        for file in files:
            if file.endswith(".py"):
                # Generating a full path to the py file
                full_path = os.path.join(root, file)
                # Removing the .py extension and replacing os separators
                module_path = full_path[:-3].replace(os.path.sep, '.')
                ext = Extension(module_path, [full_path])
                extensions.append(ext)
    return extensions

# Dynamically find extensions
package_dir = 'miksi_ai_sdk'
extensions = find_cython_extensions(package_dir)

setup(
    name="miksi-ai-sdk",
    version="0.0.19",
    author="RichardKaranuMbuti",
    author_email="officialforrichardk@gmail.com",
    description="Miksi-AI empowers your BI",
    long_description=open('docs.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Miksi-io/Custom-Agent",
    # Avoiding find_packages() as we're manually specifying extension modules
    packages=['miksi_ai_sdk'],  # Adjust according to your package structure
    ext_modules=cythonize(extensions, language_level="3"),
    python_requires='>=3.6',
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)