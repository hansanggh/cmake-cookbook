import os


def parse_yaml(file_name):
    '''
    Parse file_name and return dictionary.
    If file does not exist, return empty dictionary.
    '''
    import yaml
    import sys
    if os.path.isfile(file_name):
        with open(file_name, 'r') as f:
            try:
                config = yaml.load(f, yaml.SafeLoader)
            except yaml.YAMLError as exc:
                print(exc)
                sys.exit(-1)
        return config
    return {}


def extract_menu_file(file_name, generator, ci_environment):
    '''
    Reads file_name in yml format and returns:
    expected_failure (bool): if True, then the current generator is not supported
    env: dictionary of environment variables passed to CMake
    definitions: dictionary of CMake configure-step definitions
    '''
    config = parse_yaml(file_name)

    if ci_environment not in config:
        return False, {}, {}

    failing_generators = []
    if 'failing_generators' in config[ci_environment]:
        failing_generators = config[ci_environment]['failing_generators']
    expect_failure = generator in failing_generators

    # assemble env vars
    env = {}
    if 'env' in config[ci_environment]:
        for entry in config[ci_environment]['env']:
            for k in entry.keys():
                v = entry[k]
                env[k] = v

    # assemble definitions
    definitions = {}
    if 'definitions' in config[ci_environment]:
        for entry in config[ci_environment]['definitions']:
            for k in entry.keys():
                v = entry[k]
                definitions[k] = v

    return expect_failure, env, definitions
