#!/usr/bin/env python3
import os
import yaml
import ncg_asset as text_field
import ncg_svg as svg
# from uuid import uuid1

if __name__ == '__main__':
    comp_path = os.environ['COMP_REPO']
    comp_dir = os.listdir(comp_path)
    with open('../templates/raw/input.yml', 'r') as f:
        output = yaml.safe_load(f)

    text_fields = text_field.process_text_fields(output['textFields'])
    svg.process_svg(output)
