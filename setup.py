
from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import os

package_name = 'miksi_ai_sdk'

def find_cython_extensions(package_dir):
    extensions = []
    for root, _, files in os.walk(package_dir):
        for file in files:
            if file.endswith(".pyx"):
                full_path = os.path.join(root, file)
                module_path = full_path[:-4].replace(os.path.sep, '.')
                ext = Extension(module_path, [full_path])
                extensions.append(ext)
    return extensions

extensions = cythonize(find_cython_extensions(package_name), compiler_directives={'language_level': "3"})

setup(
    name="miksi-ai-sdk",
    version="0.0.19",
    author="RichardKaranuMbuti",
    author_email="officialforrichardk@gmail.com",
    description="Miksi-AI empowers your BI",
    long_description=open('docs.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Miksi-io/Custom-Agent",
    packages=find_packages(exclude=["*.py"]),
    ext_modules=extensions,
    python_requires='>=3.6',
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    zip_safe=False  # This is important for making sure the binary files are not zip archived
)

