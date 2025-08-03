# Import libraries needed for the app
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.config import Config
from PIL import Image as PILImage
import os
import random
import configparser

# Configure Kivy for full-screen display
Config.set('graphics', 'multisamples', '0')  # Optimize rendering
Config.set('graphics', 'width', '3840')      # Set width to 4K for testing
Config.set('graphics', 'height', '2160')     # Set height to 4K for testing
Config.set('graphics', 'fullscreen', '0')    # Set to '0' for testing in PyCharm, 'auto' for Pi

class MagazineGrid(GridLayout):
    def __init__(self, image_dir, flip_interval, **kwargs):
        super().__init__(**kwargs)
        self.cols = 10  # 10 columns for 4x10 grid
        self.rows = 4   # 4 rows for 4x10 grid
        self.image_dir = os.path.expanduser(image_dir)
        self.flip_interval = flip_interval
        self.image_widgets = []
        if not os.path.exists(self.image_dir):
            raise FileNotFoundError(f"Image directory not found: {self.image_dir}")
        self.image_files = [f for f in os.listdir(self.image_dir) if f.endswith(('.jpg', '.png'))]
        if not self.image_files:
            raise ValueError(f"No images found in {self.image_dir}")
        print(f"Initial image files count: {len(self.image_files)}")

        self.preprocess_images()

        initial_images = random.sample(self.image_files, min(40, len(self.image_files)))
        for img_file in initial_images:
            img_widget = Image(source=os.path.join(self.image_dir, img_file), allow_stretch=True, keep_ratio=True)
            self.image_widgets.append(img_widget)
            self.add_widget(img_widget)

        self.padding = 0
        self.spacing = 0
        self.size_hint = (1, 1)
        self.available_positions = list(range(40))  # Track untransitioned positions (0 to 39)
        self.transitions_count = 0  # Count transitions to reset cycle

        Clock.schedule_interval(self.flip_random_image, self.flip_interval)

    def preprocess_images(self):
        target_size = (384, 540)  # 384x540 to match 5:7 aspect ratio (0.711)
        for img_file in self.image_files:
            img_path = os.path.join(self.image_dir, img_file)
            with PILImage.open(img_path) as img:
                img = img.resize(target_size, PILImage.LANCZOS)
                img.save(img_path)

    def flip_random_image(self, dt):  # dt is unused but required by Clock.schedule_interval
        if not self.available_positions:  # Reset cycle if all positions used
            self.available_positions = list(range(40))
            self.transitions_count = 0
            print("Cycle reset: All positions transitioned")

        if self.available_positions:
            # Pick a random position index from available positions
            pos_index = random.choice(self.available_positions)
            widget = self.image_widgets[pos_index]
            self.image_files = [f for f in os.listdir(self.image_dir) if f.endswith(('.jpg', '.png'))]
            print(f"Current image files count: {len(self.image_files)}")
            current_images = [os.path.basename(w.source) for w in self.image_widgets]
            print(f"Current displayed images: {len(current_images)}")
            available_images = [f for f in self.image_files if f not in current_images]
            print(f"Available images for swap: {len(available_images)}")
            if available_images:
                new_image = random.choice(available_images)
                print(f"Selected new image: {new_image}")

                # Update widget source and animate opacity
                widget.source = os.path.join(self.image_dir, new_image)  # Set new image
                widget.opacity = 0  # Start transparent
                anim = Animation(opacity=1, duration=1.5, t='in_out_quad')
                anim.start(widget)

                # Remove the used position and update transition count
                self.available_positions.remove(pos_index)
                self.transitions_count += 1
                print(f"Transitions completed: {self.transitions_count}")
            else:
                print("No new images available for swap.")
        else:
            print("No available positions left (should not occur due to reset)")

class MagazineApp(App):
    def __init__(self, img_dir, flip_int):  # Renamed parameters to avoid shadowing
        super().__init__()
        self.image_dir = img_dir
        self.flip_interval = flip_int

    def build(self):
        return MagazineGrid(self.image_dir, self.flip_interval)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    image_dir = config.get('Settings', 'image_dir', fallback='/Users/jeffreymiller/Pictures/NewYorkerCovers')
    flip_interval = config.getfloat('Settings', 'flip_interval', fallback=20.0)

    MagazineApp(image_dir, flip_interval).run()