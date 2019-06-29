from setuptools import setup, find_packages

setup(
    name = "ine_python",
    packages = find_packages(),
    install_requires=["numpy", "pandas", "requests"],
)
