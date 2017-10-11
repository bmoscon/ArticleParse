from setuptools import setup
from setuptools import find_packages


setup(
    name="articleparse",
    version="0.2.0",
    author="Bryant Moscon",
    author_email="bmoscon@gmail.com",
    description=("Heuristic text extraction from news articles"),
    license="GPL",
    keywords=["text extraction", ],
    url="https://github.com/bmoscon/articleparse",
    packages=find_packages(exclude=['tests']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
    ],
)
