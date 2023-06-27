import os
import json

import supervisely as sly
from tqdm import tqdm

input = "./lemons-fs"
output = "./results"
os.makedirs(output, exist_ok=True)

# Creating Supervisely project from local directory.
project = sly.Project(input, sly.OpenMode.READ)
print("Opened project: ", project.name)
print("Number of images in project:", project.total_items)

# Showing annotations tags and classes.
print(project.meta)

# Iterating over classes in project, showing their names, geometry types and colors.
for obj_class in project.meta.obj_classes:
    print(
        f"Class '{obj_class.name}': geometry='{obj_class.geometry_type}', color='{obj_class.color}'",
    )

# Iterating over tags in project, showing their names and colors.
for tag in project.meta.tag_metas:
    print(f"Tag '{tag.name}': color='{tag.color}'")

print("Number of datasets (aka folders) in project:", len(project.datasets))

progress = tqdm(project.datasets, desc="Processing datasets")
for dataset in project.datasets:
    # Iterating over images in dataset, using the paths to the images and annotations.
    for item_name, image_path, ann_path in dataset.items():
        print(f"Item '{item_name}': image='{image_path}', ann='{ann_path}'")

        ann_json = json.load(open(ann_path))
        ann = sly.Annotation.from_json(ann_json, project.meta)

        img = sly.image.read(image_path)  # rgb - order

        for label in ann.labels:
            # Drawing each label on the image.
            label.draw(img)

        res_image_path = os.path.join(output, item_name)
        sly.image.write(res_image_path, img)

        # Or alternatively draw annotation (all labels at once) preview with
        # ann.draw_pretty(img, output_path=res_image_path)

        progress.update(1)
