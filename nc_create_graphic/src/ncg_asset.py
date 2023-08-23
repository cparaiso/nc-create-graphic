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
    print(text_fields)
    for index, field in enumerate(text_fields):
        field['uuid'] = str(uuid1())
        field['index'] = index + 1
        fields_uuids.append(field)
        
        __create_dir_files(field)

    return fields_uuids

def __create_dir_files(text_field: Dict) -> None:
    '''
    create directories and text files for a single text field
    '''

    with open('../templates/text.yml', 'r') as f:
        text_yml = yaml.safe_load(f)

    text_yml['id'] = text_field['uuid']
    text_yml['file'] = f'{text_field["uuid"]}.md'
    
    # create directory with uuid
    dir = f'{COMP_PATH}/source/assets/{text_yml["id"]}'
    os.mkdir(dir)

    # create yml file for text field
    with open(f"{dir}/{text_yml['id']}.yml", 'w') as f:
        yaml.dump(text_yml, f)

    # create markdown file for text field
    with open(f"{dir}/{text_yml['id']}.md", 'w') as f:
        f.write(text_field['text'])



