from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import os

# Dynamically compile all .py files in the miksi_ai_sdk directory
def find_cython_extensions(package_dir):
    extensions = []
    for root, dirs, files in os.walk(package_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file).replace(os.sep, '.').replace('.py', '')
                ext = Extension(path, [os.path.join(root, file)])
                extensions.append(ext)
    return extensions

package_dir = 'miksi_ai_sdk'
extensions = find_cython_extensions(package_dir)

setup(
    name="miksi-ai-sdk",
    version="0.0.18",
    author="RichardKaranuMbuti",
    author_email="officialforrichardk@gmail.com",
    description="Miksi-AI empowers your BI",
    long_description=open('docs.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Miksi-io/Custom-Agent",
    packages=find_packages(),
    ext_modules=cythonize(extensions, language_level = "3"),
    python_requires='>=3.6',
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)