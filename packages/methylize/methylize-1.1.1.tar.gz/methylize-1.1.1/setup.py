# Lib
from setuptools import setup, find_packages
exec(open('methylize/version.py').read())

requirements = [
    'pandas',
    'numpy',
    'scipy',
    'statsmodels',
    'matplotlib',
    'methylprep',
    'pymysql',
    'toolshed',
    'interlap',
    #'cpv', #'cpv @ git+https://github.com/brentp/combined-pvalues.git@v0.50.6#egg=cpv',
    'adjustText',
    'joblib',
    'seaborn',
]

setup(
    name='methylize',
    version=__version__,
    description='EWAS Analysis software for Illumina methylation arrays',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    project_urls = {
        "Documentation": "https://life-epigenetics-methylize.readthedocs-hosted.com/en/latest/",
        "Source": "https://github.com/FOXOBioScience/methylize/",
        "Funding": "https://FOXOBioScience.com/"
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Framework :: Jupyter',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Financial and Insurance Industry',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
      ],
    keywords='analysis methylation dna data processing life epigenetics illumina parallelization',
    url='https://github.com/FOXOBioScience/methylize',
    license='MIT',
    license_files = ('LICENSE.txt',),
    author='FOXO Bioscience',
    author_email='info@FOXOBioScience.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest',
            'coverage'
        ]
    },
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest',
        'coverage'
        ],
    entry_points={
        'console_scripts': [
            'methylize = methylize:main',
        ],
    },
)
