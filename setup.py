from setuptools import setup

setup(
    name = 'MonteCarlo',
    version = '0.1.0',
    author = 'wsr7qr',
    author_email = 'wsr7qr@virginia.edu',
    packages = ['montecarlo', 'tests'],
    #scripts = ['bin/script1','bin/script2'],
    url = 'https://github.com/sgmurek/monte_carlo',
    description = 'A package to create sets of dice, play games with them, and analyze the results.',
    #long_description = open('README.txt').read(),
    install_requires = [
        "pandas",
        "numpy",
    ]
)
