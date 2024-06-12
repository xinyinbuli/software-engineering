from setuptools import setup, find_packages

setup(
    name='fje',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fje=fje.main:main',
        ],
    },
    install_requires=[
        # 列出任何依赖包，例如：
        # 'requests',
    ],
)
