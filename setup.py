"""Setup program for gitlabel CLI
"""
from setuptools import setup

setup(
    name='GitLabel',
    version='1.0',
    license='MIT License',
    author='Doug Mahugh',
    py_modules=['gitlabel'],
    install_requires=[
        'Click',
        'Requests'
    ],
    entry_points='''
        [console_scripts]
        gitlabel=gitlabel:cli
    '''
)