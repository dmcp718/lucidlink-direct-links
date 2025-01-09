from setuptools import setup, find_packages

setup(
    name="lucidlink_direct_links",
    version="0.1.0",
    description="LucidLink Direct Link Generation Utility",
    author="David Phillips",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.9.0",
        "requests>=2.31.0",
    ],
    python_requires=">=3.8",
)
