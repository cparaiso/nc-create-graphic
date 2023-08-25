#!/usr/bin/env python3
import os
from ruamel.yaml import YAML
import ncg_asset as asset

COMP_PATH = os.environ['COMP_REPO']
if __name__ == '__main__':
    yaml = YAML()
    yaml.preserve_quotes = True

    with open('../templates/raw/input.yml', 'r') as f:
        output = yaml.load(f)

    text_fields = asset.process_text_fields(output['textFields'])
    media = asset.create_media()
    media['assets'], media['ui']['svgs'][0] = asset.insert_textfield_media(text_fields)
    media['stylesheet'] = asset.insert_media_css(text_fields, media['id'])
    media['ui']['svgs'][0]['file'] = asset.create_fd_svg() 

    dir = f"{COMP_PATH}/source/medias/{media['id']}"
    os.mkdir(dir)
    with open(f"{dir}/{media['id']}.yml", 'w') as f:
        yaml.dump(media, f)
