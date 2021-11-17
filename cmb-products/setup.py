from setuptools import setup, find_packages
setup(
    name="cmb-products",
    version="0.0.1",
    author="Mark A. Jensen",
    author_email="mark-dot-jensen-at-nih-dot-gov",
    description="automate creation of Moonshot Biobank data products",
    url="https://github.com/CIIT/cmbiobank-tools",
    python_requires='>=3.9',
    packages=find_packages(),
    package_data={
        "cmb-products.py":["cmb-products.yaml"]
    },
    install_requires=[
        'PyYAML>=5.1.1',
        'XlsxWriter>=3.0.2',
        'pyexcel>=0.6.7'
    ]
)
