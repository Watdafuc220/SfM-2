"""
SFM-2 Setup Script
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="sfm2",
    version="1.0.0",
    author="SFM-2 Team",
    description="Syntax-aware Foundation Model for Programming Languages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bryantad/SfM-2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9", 
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Code Generators",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": ["pytest>=7.0.0", "black>=22.0.0", "flake8>=5.0.0", "mypy>=0.971"],
    },
    entry_points={
        "console_scripts": [
            "sfm2-train=sfm2.training.pipeline:main",
            "sfm2-evaluate=sfm2.training.evaluation:main",
        ],
    },
)
