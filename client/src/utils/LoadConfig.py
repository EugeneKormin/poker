import yaml


def load_config(config_path=None):
    """
    Load configuration from YAML file

    Args:
        config_path (str, optional): Path to config file.
                                     Defaults to standard locations.

    Returns:
        dict: Parsed configuration dictionary
    """

    # Load and parse YAML
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Optional: Validate configuration
    __validate_config(config)

    return config


def __validate_config(config):
    """
    Optional validation of configuration structure
    """
    required_keys = ['models', 'server', 'logging']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration section: {key}")