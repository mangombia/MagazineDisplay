# MagazineDisplay

A Kivy-based application that displays a 4x10 grid of images with animated transitions. Each image transitions every 20 seconds, cycling through all 40 positions before repeating.

## Prerequisites
- Python 3.11 or later
- Git

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/MagazineDisplay.git
   cd MagazineDisplay
   
2. Create a virtual environment and activate it:
    python -m venv venv
    source/bin/activate # On Windows: venv\Scripts\activate

4. Install dependencies:
    pip install -r requirements.txt

5. Configure the image directory and interval in config.ini:
    Edit config.ini to point to your image directory

   [Settings]
   image_dir = /path/to/your/images
   flip_interval = 20.0

6. Run the application:
    python magazine_display.py
