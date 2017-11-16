"""A setuptools based setup module.
Based on the example at https://github.com/pypa/sampleproject/blob/master/setup.py
"""

from setuptools import setup

setup(
    name="transmaths",
    version="0.1.dev1",
    description="A Python module which makes division by zero possible.",
    long_description="A Python module which makes division by zero possible.",
    url="https://github.com/BenjaminEHowe/python-transmaths",
    author="Benjamin Howe",
    author_email="ben@bh96.uk",
    license='MIT',
        classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
    ],
    keywords="transmathematics transcomputation nullity zero",
    py_modules=["transmaths"],
)
