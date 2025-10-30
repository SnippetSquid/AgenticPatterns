"""
Common utilities for AgenticPatterns examples.

This module configures SSL handling for corporate networks and provides
shared utilities across all pattern examples.

WARNING: Only use SSL bypassing in development/testing environments.
"""

import warnings
import httpx
import urllib3
import requests


def configure_ssl_for_corporate_networks():
    """
    Configure SSL certificate verification bypass for corporate networks.

    This function:
    - Disables SSL warnings
    - Patches httpx.Client for OpenAI/LangChain
    - Patches requests.Session for LangSmith

    WARNING: Only use this in development/testing environments where
    corporate SSL/TLS inspection is interfering with API calls.
    """
    # Suppress SSL warnings
    warnings.filterwarnings('ignore')
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Patch httpx for OpenAI/LangChain
    original_httpx_init = httpx.Client.__init__
    def patched_httpx_init(self, *args, **kwargs):
        kwargs['verify'] = False
        original_httpx_init(self, *args, **kwargs)
    httpx.Client.__init__ = patched_httpx_init

    # Patch requests for LangSmith
    original_requests_request = requests.Session.request
    def patched_requests_request(self, *args, **kwargs):
        kwargs['verify'] = False
        return original_requests_request(self, *args, **kwargs)
    requests.Session.request = patched_requests_request


def get_http_client():
    """
    Get a pre-configured httpx.Client with SSL verification disabled.

    Returns:
        httpx.Client: HTTP client configured for corporate networks
    """
    return httpx.Client(verify=False)


# Auto-configure SSL when this module is imported
configure_ssl_for_corporate_networks()
