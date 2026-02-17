"""
Utility functions for validating output data.
"""

from pathlib import Path

import pandas as pd


def check_split_ratios(dist_dict):
    """Check the distribution across the splits for each image set."""

    for dist, df in dist_dict.items():
        print(f"\n{dist}")

        # Split distribution
        print("Split raw counts:")
        print(df["split"].value_counts())

        print("\nSplit proportions:")
        print(df["split"].value_counts(normalize=True))

        # Target distribution by split
        print("\nTarget proportions by split:")
        print(
            df.groupby("split")["midas_path_binary"].value_counts(
                normalize=True
            )
        )


def count_files_in_image_folders(root_dir):
    """Count number of image files in each train/val/test and class folder."""

    root_dir = Path(root_dir)

    for dist_dir in sorted(root_dir.iterdir()):
        if not dist_dir.is_dir():
            continue

        print(f"\n=== {dist_dir.name} ===")

        for split in ["train", "val", "test"]:
            for label in ["benign", "malignant"]:
                folder = dist_dir / split / label

                if not folder.exists():
                    print(f"{split}/{label}: MISSING FOLDER")
                    continue

                file_count = sum(p.is_file() for p in folder.iterdir())
                print(f"{split:<5} / {label:<9}: {file_count}")
