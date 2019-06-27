#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `octoprint_rest_api` package."""

import pytest
from nose.tools import assert_raises

from click.testing import CliRunner

#from octoprint_rest_api import octoprint_rest_api
from octoprint_rest_api import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


# def test_content(response):
#     """Sample pytest test function with the pytest fixture as an argument."""
#     # from bs4 import BeautifulSoup
#     # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'octoprint_rest_api.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_import():
    import asyncio
    from octoprint_rest_api import octoprint_rest_api
    OP = octoprint_rest_api.OctoPrint('127.0.0.1', 5000)
    assert True, "Test"

def test_host_not_found():
    import asyncio
    import requests
    from octoprint_rest_api import OctoPrint
    OP = OctoPrint('hassio', 80)
    event_loop = asyncio.get_event_loop()
    with assert_raises(requests.exceptions.ConnectionError):
        try:
            event_loop.run_until_complete(OP.get_api_key('test', None, 1))
        finally:
            # event_loop.close()
            pass

def test_connection_refused():
    import asyncio
    import requests
    from octoprint_rest_api import OctoPrint
    OP = OctoPrint('127.0.0.1', 1)
    event_loop = asyncio.get_event_loop()
    with assert_raises(requests.exceptions.ConnectionError):
        try:
            event_loop.run_until_complete(OP.get_api_key('test', None, 1))
        finally:
            event_loop.close()

def test_set_api_key():
    from octoprint_rest_api import OctoPrint
    OP = OctoPrint('127.0.0.1', 80)
    assert OP._set_api_key('123')

def test_deregister():
    from octoprint_rest_api import OctoPrint
    OP = OctoPrint('127.0.0.1', 80)
    OP._set_api_key('123')
    assert True, OP.deregister()
    
def test_retrieve_appkeys():
    from octoprint_rest_api import OctoPrint
    OP = OctoPrint('127.0.0.1', 80)
    OP._set_api_key('123')
    assert True, OP.retrieve_appkeys()

def test_get_printer_version():
    from octoprint_rest_api import OctoPrint
    OP = OctoPrint('127.0.0.1', 80)
    OP._set_api_key('123')
    assert True, OP.get_printer_version()

def test_get_printer_status():
    from octoprint_rest_api import OctoPrint
    OP = OctoPrint('127.0.0.1', 80)
    OP._set_api_key('123')
    assert True, OP.get_printer_status()
