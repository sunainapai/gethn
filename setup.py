"""Setup script."""

import setuptools

import myhn

setuptools.setup(
    name='myhn',
    version=myhn.__version__,
    author=myhn.__author__,
    description=myhn.__doc__,
    long_description=open('README.rst').read(),
    url='https://github.com/sunainapai/myhn',
    py_modules=['myhn'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet',
        'Topic :: Utilities',
    ],
)
