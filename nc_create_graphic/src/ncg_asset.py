from typing import Dict, List, Tuple
from uuid import uuid1
import os
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

COMP_PATH = os.environ['COMP_REPO']
yaml = YAML()                       
yaml.preserve_quotes = True
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

def media_insert_text_field(fields: List[Dict]) -> Tuple:
    assets = []
    ui = {} 
    for field in fields:
        double_quoted_scalar = DoubleQuotedScalarString(field['uuid'])
        assets.append(double_quoted_scalar)
        ui[f"text{field['index']}"] = double_quoted_scalar 
    

    return (assets, ui)

def media_insert_css(fields: List[Dict], media_id: str) -> Tuple:
    text_fields = []
    with open('../templates/css.yml', 'r') as f:
        css_yml = yaml.load(f)

    css_yml['id'] = str(uuid1())
    css_yml['file'] = f"{css_yml['id']}.css"
    css_yml['containerId'] = media_id 

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

    return css_yml['id']   

def media_create() -> Dict:
    with open('../templates/media.yml', 'r') as f:
        media = yaml.load(f)

    media['id'] = str(uuid1())

    return media

def create_fd_svg() -> str:
    uuid = str(uuid1())
    
    with open('../templates/svg.yml', 'r') as f:
        svg_yml = yaml.load(f)

    dir = f"{COMP_PATH}/source/assets/{uuid}"
    os.mkdir(dir)

    svg_yml['id'] = uuid
    svg_yml['file'] = f"{uuid}.svg"

    with open(f"{dir}/{uuid}.svg", 'w') as f:
        f.write('')
    
    with open(f"{dir}/{uuid}.yml", 'w') as f:
        yaml.dump(svg_yml, f)

    return DoubleQuotedScalarString(uuid)

def __create_fd_text_fields(text_field: Dict) -> None:
    '''
    create directories and text files for a single text field
    '''

    with open('../templates/text.yml', 'r') as f:
        text_yml = yaml.load(f)

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
        newline = '\n'
        text_fields = css['textFields']
        for field in text_fields:
            attrs = field['attributes']
            f.write(f'''[id="{css['containerId']}"] [id="{field['cssId']}"] {{ top: {attrs['y']}; left: {attrs['x']};size: {attrs['size']}; }}{newline}''')












