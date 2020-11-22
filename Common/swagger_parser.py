import json
from pprint import pprint as pp
from importlib.resources import read_binary


def read_swagger(package):
    load_swag = json.loads(read_binary(package, resource="swagger.json")
        .decode('utf-8'))
    pp(load_swag.keys())
    '''{'swagger': numer wersji dokumentu, 
        'info': {'termsOfService': '', 'title': 'BDL API', 'version': 'v1'}, 
        'basePath': '/api/v1, 
        'paths': 0, 
        'definitions': 0, 
        'tags': 0}
    '''
    # TODO: use paths to generate get functions
    pp(load_swag['paths']['/aggregates/metadata']['get']['parameters'])
    print("==============================================")
    pp([item['name'] for item 
            in load_swag['paths']['/aggregates/metadata']['get']['parameters']])
    # TODO: use definitions for response data class containers
    print("==============================================")
    pp(load_swag['definitions']['Metadata']['properties'].keys())
