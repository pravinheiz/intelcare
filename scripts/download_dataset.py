import gdown
import os

url = "https://drive.google.com/uc?export=download&id=1oWSRdZuoT9YIBb4-UG2ZJ-6ijyIbErgK"
output_path = "data/raw/healthcare_dataset.csv"

os.makedirs("data/raw", exist_ok=True)
gdown.download(url, output_path, quiet=False)
