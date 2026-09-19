import os
import random
import shutil

# Set random seed for reproducibility
random.seed(42)

# Dataset folders
images_dir = "datasets/images"
labels_dir = "datasets/labels"

# Split ratios
train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

# Get all image files
images = [
    f for f in os.listdir(images_dir)
    if f.endswith((".jpg", ".jpeg", ".png"))
]

# Shuffle images
random.shuffle(images)

# Calculate split sizes
train_end = int(len(images) * train_ratio)
val_end = train_end + int(len(images) * val_ratio)

train_images = images[:train_end]
val_images = images[train_end:val_end]
test_images = images[val_end:]

# Create folders
for split in ["train", "valid", "test"]:
    os.makedirs(f"datasets/{split}/images", exist_ok=True)
    os.makedirs(f"datasets/{split}/labels", exist_ok=True)

# Function to copy images and labels
def copy_files(image_list, split):
    for image_file in image_list:
        label_file = os.path.splitext(image_file)[0] + ".txt"

        shutil.move(
            os.path.join(images_dir, image_file),
            os.path.join(f"datasets/{split}/images", image_file)
        )

        if os.path.exists(os.path.join(labels_dir, label_file)):
            shutil.move(
                os.path.join(labels_dir, label_file),
                os.path.join(f"datasets/{split}/labels", label_file)
            )

# Copy files
copy_files(train_images, "train")
copy_files(val_images, "valid")
copy_files(test_images, "test")

# Print results
print("\nDataset Split Complete!")
print(f"Train Images : {len(train_images)}")
print(f"Valid Images : {len(val_images)}")
print(f"Test Images  : {len(test_images)}")