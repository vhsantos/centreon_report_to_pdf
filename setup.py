from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='centreon_report_to_pdf',
    packages=['centreon_report_to_pdf'],
    version='1.5.4',
    description='Generate a PDF from Centreon Dashboard and optional sent it by email',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Victor Hugo dos Santos',
    author_email='listas.vhs@gmail.com',
    url='https://github.com/vhsantos/centreon_report_to_pdf',
    download_url='https://github.com/vhsantos/centreon_report_to_pdf/archive/v1.5.4.tar.gz',
    keywords='centreon report pdf email dashboard',
    classifiers=["Programming Language :: Python :: 3.5",
                 "Topic :: System :: Monitoring",
                 "Development Status :: 6 - Mature", "Intended Audience :: System Administrators",
                 "Operating System :: OS Independent", "Environment :: Console"],
    install_requires=[
        'reportlab>=3.5',
        'pandas>=1.0',
        'requests>=2.23',
        'pytz>=2022.1',
    ],
    include_package_data=True
)
