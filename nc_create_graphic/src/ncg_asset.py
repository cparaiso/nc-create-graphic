from typing import Dict, List
import yaml
from uuid import uuid1
import os

COMP_PATH = os.environ['COMP_REPO']
                       
def process_text_fields(text_fields: List) -> List[Dict]:
    '''
    process text fields 
    '''
    fields_uuids = [] 

    for index, field in enumerate(text_fields):
        field['uuid'] = str(uuid1())
        field['index'] = index + 1
        fields_uuids.append(field)
        
        __create_fd_text_fields(field)

    return fields_uuids

def media_insert_text_field(fields: List[Dict], media: Dict) -> Dict:
    assets = []

    for field in fields:
        assets.append(field['uuid'])
        media['ui']['svgs'][0][f"text{field['index']}"] = field['uuid']
    
    media['assets'] = assets

    return media

def media_insert_css(fields: List[Dict], media: Dict) -> Dict:
    text_fields = []
    with open('../templates/css.yml', 'r') as f:
        css_yml = yaml.safe_load(f)

    css_yml['id'] = str(uuid1())
    css_yml['file'] = f"{css_yml['id']}.css"
    css_yml['containerId'] = media['id']

    for field in fields:
        css_text_field = {
            'type': 'text',
            'content': field['text'],
            'cssId': f"text{field['index']}",
            'id': css_yml['id'],
            'attributes': {
                'type': 'TEXT',
                'x': 0,
                'y': 0,
                'size': 22
            }
        } 

        text_fields.append(css_text_field)

    css_yml['textFields'] = text_fields

    __create_fd_css(css_yml)

    media['stylesheet'] = css_yml['id']
    return media   

def media_create() -> Dict:
    with open('../templates/media.yml', 'r') as f:
        media = yaml.safe_load(f)

    media['id'] = str(uuid1())

    return media

def __create_fd_text_fields(text_field: Dict) -> None:
    '''
    create directories and text files for a single text field
    '''

    with open('../templates/text.yml', 'r') as f:
        text_yml = yaml.safe_load(f)

    text_yml['id'] = text_field['uuid']
    text_yml['file'] = f"{text_field['uuid']}.md"
    
    # create directory with uuid
    dir = f"{COMP_PATH}/source/assets/{text_yml['id']}"
    os.mkdir(dir)

    # create yml file for text field
    with open(f"{dir}/{text_yml['id']}.yml", 'w') as f:
        yaml.dump(text_yml, f)

    # create markdown file for text field
    with open(f"{dir}/{text_yml['id']}.md", 'w') as f:
        f.write(text_field['text'])

def __create_fd_css(css: Dict) -> None:
    '''
    create directories and files for css
    '''
    
    dir = f"{COMP_PATH}/source/assets/{css['id']}"
    os.mkdir(dir)
    
    with open(f"{dir}/{css['id']}.yml", 'w') as f:
        yaml.dump(css, f)

    with open(f"{dir}/{css['file']}", 'w') as f:
        f.write('')

