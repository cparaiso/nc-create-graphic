#!/usr/bin/env python3
import os
from uuid import uuid1
from ruamel.yaml import YAML
import ncg_asset as asset
# import ncg_svg as svg
# from uuid import uuid1

COMP_PATH = os.environ['COMP_REPO']
if __name__ == '__main__':
    yaml = YAML()
    yaml.preserve_quotes = True
    with open('../templates/raw/input.yml', 'r') as f:
        output = yaml.load(f)
    text_fields = asset.process_text_fields(output['textFields'])
    media = asset.media_create()
    media = asset.media_insert_text_field(text_fields, media)
    media = asset.media_insert_css(text_fields, media)
    print(media) 
    # create uuid and media file
    id = uuid1()
    dir = f"{COMP_PATH}/source/medias/{id}"

    os.mkdir(dir)
    with open(f"{dir}/{id}.yml", 'w') as f:
        yaml.dump(media, f)
