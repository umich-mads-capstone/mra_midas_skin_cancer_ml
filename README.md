# Multimodal Skin Cancer Detection

## Table of Contents
- [Description](#description)
- [Data Access](#data-access)
- [Getting Started](#getting-started)

## Description
This project examines whether AI models can identify skin cancer using different types of input data. It compares image-only models, metadata-only models, and models that combine clinical and dermoscopic images with clinical metadata to assess differences in performance and reliability. The study also investigates which data sources provide the strongest predictive signal and whether combining inputs offers meaningful improvement.

## Data Access
This project uses the MRA-MIDAS (Multimodal Image Dataset for AI-based Skin Cancer) provided by the Stanford Center for Artificial Intelligence in Medicine and Imaging. The dataset contains paired clinical and dermoscopic images of skin lesions, along with biopsy-confirmed diagnoses and associated clinical metadata.

The dataset is owned and curated by Stanford AIMI and is made available for research purposes through Stanford’s data portal. Access is granted under a research use agreement, and users must comply with all applicable terms and conditions, including registration and approval where required.

The dataset is provided free of charge for non-commercial research use. Redistribution of the dataset or its contents is not permitted unless explicitly allowed under the agreement. Proper attribution to Stanford AIMI is required in any publications or outputs derived from the data. For more details, please visit: https://aimi.stanford.edu/shared-datasets

## Getting Started

### Prerequisites
- Python 3.9+ 
- `pip`
- `venv`

### 1. Create and Activate a Virtual Environment
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

### 2. Install Package and Dependencies
Install this repository as a local package along with its dependencies:

```bash
pip install -e .
```

### 3. Deactivate the Virtual Environment
When you are done working:

```bash
deactivate
```
