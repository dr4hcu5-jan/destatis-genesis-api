from setuptools import setup

setup(
    name='src',
    version='0.0.1',
    package_dir={"": "src"},
    url='https://github.com/j-suchard/destatis-genesis-api',
    license='BSD-3-Clause',
    author='Jan Eike Suchard',
    author_email='jan-eike,suchard@magenta.de',
    maintainer='Jan Eike Suchard',
    maintainer_email='jan-eike.suchard@magenta.de',
    description='Wrapper for the DESTATIS GENESIS database',
    install_requires=['pydantic', 'aiohttp[speedups]', 'requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience ::  Education",
        "Intended Audience ::  Science/Research",
        "License :: OSI Approved :: BSD License"
    ]
)
