from setuptools import find_packages, setup

setup(
    name="mra_midas_skin_cancer_ml",
    version="0.1.0",
    packages=[
        "mra_midas_skin_cancer_ml.utils",
        "mra_midas_skin_cancer_ml.notebooks",
    ],
    package_dir={
        "mra_midas_skin_cancer_ml.utils": "utils",
        "mra_midas_skin_cancer_ml.notebooks": "notebooks",
    },
    install_requires=[
        "pandas",
        "openpyxl",
    ],
    python_requires=">=3.7",
    description="ML models on the Stanford MRA-MIDAS skin cancer dataset",
    author="Your Name",
    author_email="your.email@example.com",
)
