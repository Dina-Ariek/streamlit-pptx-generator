# utils/file_utils.py

import os
import pandas as pd

def get_project_path(*path_segments):
    """Return the absolute path from the root of the project."""
    root = os.path.dirname(os.path.dirname(__file__))  # goes back to the project root
    return os.path.join(root, *path_segments)

def load_csv(file_name):
    """Load CSV file from the 'data' folder."""
    file_path = get_project_path("data", file_name)
    print(f"Loading file from: {file_path}")  # Debugging line to check the path
    return pd.read_csv(file_path)
