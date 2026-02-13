from setuptools import setup


def read_requirements():
    with open("requirements.txt", "r") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]


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
    install_requires=read_requirements(),
    python_requires=">=3.7",
    description="ML models on the Stanford MRA-MIDAS skin cancer dataset",
    author="Jerome Wong, Kaitlin (Kaily) Daida",
    author_email="jrmwong@umich.edu, kdaida@umich.edu",
)
