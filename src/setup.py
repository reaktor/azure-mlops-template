from setuptools import setup, find_packages

data = dict(
    name="my_ml_project",
    version="0.0.1",
    packages=find_packages(),
)

if __name__ == '__main__':
    setup(**data)
