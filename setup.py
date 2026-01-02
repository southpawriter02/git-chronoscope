"""
git-chronoscope: Generate time-lapse visualizations of Git repository evolution.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="git-chronoscope",
    version="0.9.0-beta.1",
    author="Git Chronoscope Team",
    author_email="chronoscope@example.com",
    description="Generate time-lapse visualizations of Git repository evolution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/southpawriter02/git-chronoscope",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "GitPython>=3.1.0",
        "Pillow>=9.0.0",
        "Pygments>=2.10.0",
        "tqdm>=4.60.0",
        "Flask>=2.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "git-chronoscope=src.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
