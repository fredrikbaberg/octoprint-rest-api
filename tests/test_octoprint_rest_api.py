#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `octoprint_rest_api` package."""

import asyncio
import responses
import requests
import pytest
import json
from nose.tools import assert_raises
from functools import partial


import asyncio
from click.testing import CliRunner

from octoprint_rest_api import OctoPrint
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

@responses.activate
def test_get_api_key():
    event_loop = asyncio.get_event_loop()
    with assert_raises(requests.exceptions.ConnectionError):
        OP = OctoPrint('127.0.0.1', 1)
        try:
            event_loop.run_until_complete(OP.get_api_key('test', None, 1))
        finally:
            #event_loop.close()
            pass
    with assert_raises(requests.exceptions.ConnectionError):
        OP = OctoPrint('127.0.0.2', 1)
        try:
            event_loop.run_until_complete(OP.get_api_key('test', None, 1))
        finally:
            #event_loop.close()
            pass
    OP = OctoPrint('mock', 1)
    responses.add(responses.GET, 'http://mock:1/plugin/appkeys/probe', json={}, status=404)
    with assert_raises(Exception):
        try:
            event_loop.run_until_complete(OP.get_api_key('test', None, 1))
        finally:
            #event_loop.close()
            pass
    responses.replace(responses.GET, 'http://mock:1/plugin/appkeys/probe', json={}, status=204)
    def request_callback_fail(request):
        return (404, {}, json.dumps({}))
    responses.add_callback(
        responses.POST, 'http://mock:1/plugin/appkeys/request',
        callback=request_callback_fail,
        content_type='application/json',
    )
    with assert_raises(Exception):
        try:
            event_loop.run_until_complete(OP.get_api_key('test', None, 1))
        finally:
            #event_loop.close()
            pass
    def request_callback_successs(request):
        return (201, {}, json.dumps({'app_token': 'abc'}))
    responses.remove(responses.POST, 'http://mock:1/plugin/appkeys/request')
    responses.add_callback(
        responses.POST, 'http://mock:1/plugin/appkeys/request',
        callback=request_callback_successs,
        content_type='application/json',
    )
    with assert_raises(Exception):
        try:
            event_loop.run_until_complete(OP.get_api_key('test', None, 1))
        finally:
            #event_loop.close()
            pass
    responses.add(responses.GET, 'http://mock:1/plugin/appkeys/request/abc', json={}, status=202)
    responses.add(responses.GET, 'http://mock:1/plugin/appkeys/request/abc', json={}, status=404)
    with assert_raises(Exception):
        try:
            event_loop.run_until_complete(OP.get_api_key('test', None, 1))
        finally:
            #event_loop.close()
            pass
    responses.remove(responses.GET, 'http://mock:1/plugin/appkeys/request/abc')
    responses.add(responses.GET, 'http://mock:1/plugin/appkeys/request/abc', json={}, status=202)
    responses.add(responses.GET, 'http://mock:1/plugin/appkeys/request/abc', json={'api_key': 'secretkey'}, status=200)
    try:
        assert event_loop.run_until_complete(OP.get_api_key('test', None, 1)) == True
    finally:
        #event_loop.close()
        pass
    

    
# @responses.activate
# def test_get_api_key_request():
#     responses.add(responses.POST, 'http://mock:1/plugin/appkeys/request', json={}, status=201)
#     OP = OctoPrint('mock', 1)
#     event_loop = asyncio.get_event_loop()
#     with assert_raises(requests.exceptions.ReadTimeout):
#         try:
#             event_loop.run_until_complete(OP.get_api_key('test', None, 1))
#         finally:
#             #event_loop.close()
#             pass


# def test_set_api_key():
#     from octoprint_rest_api import OctoPrint
#     OP = OctoPrint('127.0.0.1', 80)
#     assert OP._set_api_key('123')

# def test_deregister():
#     from octoprint_rest_api import OctoPrint
#     OP = OctoPrint('127.0.0.1', 80)
#     OP._set_api_key('123')
#     assert True, OP.deregister()
    
# def test_retrieve_appkeys():
#     from octoprint_rest_api import OctoPrint
#     OP = OctoPrint('127.0.0.1', 80)
#     OP._set_api_key('123')
#     assert True, OP.retrieve_appkeys()

# def test_get_printer_version():
#     from octoprint_rest_api import OctoPrint
#     OP = OctoPrint('127.0.0.1', 80)
#     OP._set_api_key('123')
#     assert True, OP.get_printer_version()

# def test_get_printer_status():
#     from octoprint_rest_api import OctoPrint
#     OP = OctoPrint('127.0.0.1', 80)
#     OP._set_api_key('123')
#     assert True, OP.get_printer_status()

# def test_get_printer_job():
#     from octoprint_rest_api import OctoPrint
#     OP = OctoPrint('127.0.0.1', 80)
#     OP._set_api_key('123')
#     assert True, OP.get_printer_job()

# def test_pause_print():
#     from octoprint_rest_api import OctoPrint
#     OP = OctoPrint('127.0.0.1', 80)
#     OP._set_api_key('123')
#     assert True, OP.pause_print()
