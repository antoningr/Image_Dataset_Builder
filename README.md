# 🧠 Image Dataset Builder

A Python tool to automatically download and build custom image datasets from DuckDuckGo image search.  
Perfect for AI, machine learning, computer vision projects or data augmentation tasks.

---

## Features

- 🔍 Search and download images by keyword(s)
- 📦 Support for multiple queries at once
- 📥 Specify number of images per query
- 🖼️ Supports multiple image formats (JPG, PNG, WEBP)
- 🔄 Option to convert all images to JPG
- ✅ Ensures the exact number of valid images are saved
- 🧼 Handles bad URLs, timeouts, and unreadable files
- 🖼️ Displays the first and last image downloaded per query
- 📁 Organizes images into per-query subfolders
- 🛠️ CLI script packaged with `setup.py` for installable tool

---

## Installation & Run (with a CLI)

1. Clone this repository:
    ```bash
   git clone https://github.com/antoningr/Image_Dataset_Builder.git
    ```
2. Change directory:
    ```bash
    cd Image_Dataset_Builder
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the script using Python:
    ```bash
    python image_dataset_builder.py
    ```

---

## Example
- Enter your search queries (comma-separated): forest fire, forest
- How many images per query? (default = 10): 20
- Convert all images to JPG? (y/n): y

---

## Files Included
- mage_dataset_builder.py — main script
- setup.py — packaging config
- requirements.txt — dependencies

---

## Requirements
- Python 3.7+
è Internet access (uses DuckDuckGo image search API)