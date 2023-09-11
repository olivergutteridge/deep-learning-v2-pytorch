import os
import shutil
import random
from PIL import Image

def SplitData(root_dir, train_dir_name='Train', test_dir_name='Test', categories=['Cat', 'Dog'], test_split_ratio=0.2):
    # Check if train and test directories already exist in root_dir
    if os.path.exists(os.path.join(root_dir, train_dir_name)) and os.path.exists(os.path.join(root_dir, test_dir_name)):
        print("Split has already occurred. Skipping the splitting process.")
        # Delete the original Cat and Dog directories
        for category in categories:
            try:
                shutil.rmtree(os.path.join(root_dir, category))
            except FileNotFoundError:
                pass  # Directory doesn't exist
        return None

    # Define the directory paths for Train and Test
    train_dir = os.path.join(root_dir, train_dir_name)
    test_dir = os.path.join(root_dir, test_dir_name)

    # Create Train and Test directories
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Initialize a list to keep track of removed images
    removed_images = []

    # Iterate through each category (Cat and Dog)
    for category in categories:
        # Create subdirectories for Cat and Dog in Train and Test
        train_category_dir = os.path.join(train_dir, category)
        test_category_dir = os.path.join(test_dir, category)

        os.makedirs(train_category_dir, exist_ok=True)
        os.makedirs(test_category_dir, exist_ok=True)

        # Get a list of all images in the current category
        category_images = os.listdir(os.path.join(root_dir, category))

        # Shuffle the images randomly
        random.shuffle(category_images)

        # Calculate the number of images to be moved to the test set
        num_test_images = int(len(category_images) * test_split_ratio)

        # Move images to the test directory, handling errors
        for img_filename in category_images[:num_test_images]:
            src_path = os.path.join(root_dir, category, img_filename)
            dest_path = os.path.join(test_category_dir, img_filename)
            try:
                im = Image.open(src_path)
                shutil.move(src_path, dest_path)
            # Do stuff with the image
            except IOError:
                # Handle the IOError by deleting the file
                try:
                    os.remove(src_path)
                    print(f"Deleted file: {src_path}")
                except OSError as e:
                    print(f"Error deleting file: {src_path}, {e}")

        # Move the remaining images to the train directory, handling errors
        for img_filename in category_images[num_test_images:]:
            src_path = os.path.join(root_dir, category, img_filename)
            dest_path = os.path.join(train_category_dir, img_filename)
            try:
                im = Image.open(src_path)
                shutil.move(src_path, dest_path)
            # Do stuff with the image
            except IOError:
                # Handle the IOError by deleting the file
                try:
                    os.remove(src_path)
                    print(f"Deleted file: {src_path}")
                except OSError as e:
                    print(f"Error deleting file: {src_path}, {e}")

    # Delete the original Cat and Dog directories
    for category in categories:
        try:
            shutil.rmtree(os.path.join(root_dir, category))
        except FileNotFoundError:
            pass  # Directory doesn't exist

    print("Data split into Train and Test sets with a {:.1%} test split.".format(test_split_ratio))
    return None
