import argparse
import json
import os
import shutil
import time
from datetime import datetime
from pathlib import Path

import yaml

i = 1
post_id = 1
tag_list = []
tag_pair = {}

image_size = ("w300", "w600", "w1000", "w2000")
folder_path_list = []


def main(input_folder, output_file_name):
    images_path = Path("images/size")
    images_path.mkdir(exist_ok=True)
    for folder_path in image_size:
        folder_path = images_path.joinpath(folder_path)
        folder_path.mkdir(exist_ok=True)
        folder_path_list.append(folder_path)

    data_template = {
        "db": [
            {
                "meta": {"exported_on": int(time.time() * 1000), "version": "5.41.0"},
                "data": {
                    "posts": [],
                    "tags": [],
                    "posts_tags": [],
                },
            }
        ]
    }

    def get_featured_image(image_tag, dir_path):
        if type(image_tag) == list:
            print(f"Feature image is")
            print({image_tag[0]["src"]})

            featured_image_path = os.path.join(dir_path, image_tag[0]["src"])

            for folder_path in folder_path_list:
                try:
                    shutil.copy(featured_image_path, str(folder_path))
                except FileNotFoundError:
                    return ""

            return "__GHOST_URL__/content/images/" + image_tag[0]["src"]

        else:
            return ""

    def process_front_matter(front_matter, dir_path):
        global i, post_id
        for tag in front_matter.get("tags", ""):
            if tag not in tag_list:
                tag_list.append(tag)
                tag_pair[tag] = i
                tag = {"id": i, "name": tag, "slug": tag}
                data_template["db"][0]["data"]["tags"].append(tag)
                i += 1
            else:
                continue

        for tag in front_matter.get("tags", ""):
            tag = {"tag_id": tag_pair[tag], "post_id": post_id}
            data_template["db"][0]["data"]["posts_tags"].append(tag)

        date = front_matter.get("date", "")
        feature_image = get_featured_image(front_matter.get("resources", ""), dir_path)

        result = {
            "id": post_id,
            "title": front_matter.get("title", ""),
            "slug": front_matter.get("slug", ""),
            "feature_image": feature_image,
            "meta_title": front_matter.get("title", ""),
            "meta_description": front_matter.get("subtitle", ""),
            "status": "published",
            "created_at": date,
            "updated_at": front_matter.get("lastmod", date),
            "published_at": front_matter.get("lastmod", date),
            "tags": [{"name": tag.strip()} for tag in front_matter.get("tags", [])],
            "mobiledoc": "",
        }
        post_id += 1
        return result

    def markdown_to_mobiledoc(markdown_content: str):
        # to remove custom shortcodes
        markdown_content = markdown_content.replace("{{<lb>}}", "")
        markdown_content = markdown_content.replace("{{< lb >}}", "")
        mobiledoc = {
            "version": "0.3.1",
            "markups": [],
            "atoms": [],
            "cards": [
                ["markdown", {"cardName": "markdown", "markdown": markdown_content}]
            ],
            "sections": [[10, 0]],
        }
        return json.dumps(mobiledoc)

    for dir_path, dir_names, file_name in os.walk(input_folder):
        # print(dir_path, dir_names, file_name)
        for a in file_name:
            if a.endswith(".md"):
                input_file_path = os.path.join(dir_path, a)
                with open(input_file_path, "r", encoding="utf-8") as input_file:
                    input_content = input_file.read()
                    try:
                        split_content = input_content.split("---")
                        yaml_content, markdown_content = split_content[1], "---".join(
                            split_content[2:]
                        )
                    except IndexError:
                        continue
                    print(dir_path)
                    front_matter = yaml.safe_load(yaml_content)
                    post_data = process_front_matter(front_matter, dir_path)
                    post_data["mobiledoc"] = markdown_to_mobiledoc(
                        markdown_content.strip()
                    )
                    data_template["db"][0]["data"]["posts"].append(post_data)

    with open(output_file_name, "w", encoding="utf-8") as output_file:
        json.dump(data_template, output_file, ensure_ascii=False, indent=4, default=str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert Hugo posts to Ghost JSON format."
    )
    parser.add_argument(
        "input_folder", help="Path to the folder containing Hugo posts (content)"
    )
    parser.add_argument("output_file_name", help="Name of the output JSON file")

    args = parser.parse_args()
    # main("D:\shekharverma\content", "testing.json")
    main(args.input_folder, args.output_file_name)
