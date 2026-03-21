# Multimodal Skin Cancer Detection

## Table of Contents
- [About](#about)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
  - [Data Setup](#data-setup)
- [Data Source and Usage](#data-source-and-usage)

## About
This project examines whether AI models can identify skin cancer using different types of input data. It compares image-only models, metadata-only models, and models that combine clinical and dermoscopic images with clinical metadata to assess differences in performance and reliability. The study also investigates which data sources provide the strongest predictive signal and whether combining inputs offers meaningful improvements.

## Getting Started

### Prerequisites
- Python 3.9+ 
- `pip`
- `venv`

### Environment Setup

#### 1. Create and Activate a Virtual Environment
From the project root, create a virtual environment:

```bash
python -m venv .venv
```

After creating the virtual environment, activate it using the command below:

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux (bash/zsh):

```bash
source .venv/bin/activate
```

#### 2. Install Package and Dependencies
Install this repository as a local package along with its dependencies:

```bash
pip install -e .
```

#### 3. Deactivate the Virtual Environment
When you are done working:

```bash
deactivate
```
### Data Setup

Download the dataset from the [MRA-MIDAS dataset](https://aimi.stanford.edu/datasets/mra-midas-Multimodal-Image-Dataset-for-AI-based-Skin-Cancer) page. After downloading, extract the dataset, rename the folder to `raw_images`, and place it in the following directory. Ensure the folder structure matches the expected input paths used in the code.

```bash
data/
└── input/
    └── raw_images/
```

## Data Source and Usage
This project uses the [MRA-MIDAS dataset](https://aimi.stanford.edu/datasets/mra-midas-Multimodal-Image-Dataset-for-AI-based-Skin-Cancer) (Multimodal Image Dataset for AI-based Skin Cancer) provided by the Stanford Center for Artificial Intelligence in Medicine and Imaging (AIMI). The dataset contains paired clinical and dermoscopic images of skin lesions, along with biopsy-confirmed diagnoses and associated clinical metadata. 

The dataset is owned and curated by Stanford AIMI and is made available for non-commercial research purposes through Stanford’s data portal. Users are expected to acknowledge Stanford AIMI in publications, presentations, and other outputs using the following language:

> “This research used data provided by the Stanford Center for Artificial Intelligence in Medicine and Imaging (AIMI). AIMI curated a publicly available imaging data repository containing clinical imaging and data from Stanford Health Care, the Stanford Children’s Hospital, the University Healthcare Alliance, and Packard Children's Health Alliance clinics provisioned for research use by the Stanford Medicine Research Data Repository (STARR).”

For more details, please visit [Stanford AIMI Shared Datasets](https://aimi.stanford.edu/shared-datasets).