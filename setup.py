from setuptools import setup
import os.path as op

with open(op.join(op.dirname(op.realpath(__file__)), 'figura', '_version.py')) as version_file:
    exec(version_file.read())

install_requires = []
tests_require = [
    'pytest>=7.1.0'
]
setup_requires = [
    'multimethod>=1.9.0'
]

setup(
    name='figura',
    version=__version__,
    description='Simple python scripting for creating CAD files',
    url='https://github.com/andrsd/figura',
    author='David Andrs',
    author_email='andrsd@gmail.com',
    license='MIT',
    packages=['figura'],
    entry_points={
        'console_scripts': [
            'figura = figura.__main__:main'
        ]
    },
    install_requires=install_requires,
    tests_require=tests_require,
    setup_requires=setup_requires
)
