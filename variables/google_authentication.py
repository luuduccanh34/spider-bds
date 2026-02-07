from variables.helper import BaseConfig

class GoogleAuthentication(BaseConfig):
    """
    Configuration loader for Google authentication and project access.

    This class inherits from `BaseConfig` and defines the required
    environment variables (or Airflow Variables) needed to authenticate
    with Google Cloud and its services.

    Attributes
    ----------
    VARIABLES : list[str]
        List of required configuration variables:
        - "GOOGLE_SERVICE_ACCOUNT": Service account JSON key or path used for Google API authentication.
        - "GOOGLE_CLOUD_PROJECT": Google Cloud Project ID where resources are located.
    """
    VARIABLES = [
        "GOOGLE_SERVICE_ACCOUNT",
        "GOOGLE_CLOUD_PROJECT"
    ]
