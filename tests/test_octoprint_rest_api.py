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
    
@responses.activate
def test_deregister():
    def request_callback_deregister(request):
        if request.headers['X-Api-Key']:
            return (204, {}, json.dumps({}))
        else:
            return (403, {}, json.dumps({}))
    responses.add_callback(
        responses.POST, 'http://mock:1/api/plugin/appkeys',
        callback=request_callback_deregister,
        content_type='application/json'
    )
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    assert OP.deregister() == True

@responses.activate
def test_retrieve_appkeys():
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    responses.add(responses.GET, 'http://mock:1/api/plugin/appkeys', json={'keys': [], 'pending': []}, status=200)
    assert OP.retrieve_appkeys() == {'keys': [], 'pending': []}
    
@responses.activate
def test_get_printer_version():
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    responses.add(responses.GET, 'http://mock:1/api/version', json={'api': '0.1', 'server': '1.3.10', 'text': 'OctoPrint 1.3.10'}, status=200)
    assert OP.get_printer_version() == {'api': '0.1', 'server': '1.3.10', 'text': 'OctoPrint 1.3.10'}
    
@responses.activate
def test_get_printer_status():
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    _status = {
        "temperature": {
            "tool0": {
                "actual": 214.8821,
                "target": 220.0,
                "offset": 0
            },
            "bed": {
                "actual": 50.221,
                "target": 70.0,
                "offset": 5
            }
        },
        "state": {
            "text": "Operational",
            "flags": {
                "operational": True,
                "paused": False,
                "printing": False,
                "cancelling": False,
                "pausing": False,
                "sdReady": True,
                "error": False,
                "ready": True,
                "closedOrError": False
            }
        }
    }
    responses.add(responses.GET, 'http://mock:1/api/printer', json=_status, status=200)
    assert OP.get_printer_status() == _status

@responses.activate
def test_get_printer_connection():
    _status = {
        "current": {
            "state": "Operational",
            "port": "/dev/ttyACM0",
            "baudrate": 250000,
            "printerProfile": "_default"
        },
        "options": {
            "ports": ["/dev/ttyACM0", "VIRTUAL"],
            "baudrates": [250000, 230400, 115200, 57600, 38400, 19200, 9600],
            "printerProfiles": [{"name": "Default", "id": "_default"}],
            "portPreference": "/dev/ttyACM0",
            "baudratePreference": 250000,
            "printerProfilePreference": "_default",
            "autoconnect": True
        }
    }
    responses.add(responses.GET, 'http://mock:1/api/connection', json=_status, status=200)
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    assert OP.get_printer_connection() == _status

@responses.activate
def test_get_printer_files():
    _status = {}
    responses.add(responses.GET, 'http://mock:1/api/files?recursive=true', json=_status, status=200)
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    assert OP.get_printer_files() == _status

@responses.activate
def test_get_printer_job():
    _status = {
        "job": {
            "file": {
                "name": "whistle_v2.gcode",
                "origin": "local",
                "size": 1468987,
                "date": 1378847754
            },
            "estimatedPrintTime": 8811,
            "filament": {
                "length": 810,
                "volume": 5.36
            }
        },
        "progress": {
            "completion": 0.2298468264184775,
            "filepos": 337942,
            "printTime": 276,
            "printTimeLeft": 912
        },
        "state": "Printing"
    }
    responses.add(responses.GET, 'http://mock:1/api/job', json=_status, status=200)
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    assert OP.get_printer_job() == _status


@responses.activate
def test_pause_print():
    def request_callback_pause(request):
        return (204, {}, json.dumps({}))
    responses.add_callback(
        responses.POST, 'http://mock:1/api/job',
        callback=request_callback_pause,
        content_type='application/json',
    )
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    OP.connected = False
    assert OP.pause_print() == False
    OP.connected = True
    assert OP.pause_print().json() == {}

@responses.activate
def test_resume_print():
    def request_callback_resume(request):
        return (204, {}, json.dumps({}))
    responses.add_callback(
        responses.POST, 'http://mock:1/api/job',
        callback=request_callback_resume,
        content_type='application/json',
    )
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    OP.connected = False
    assert OP.resume_print() == False
    OP.connected = True
    assert OP.resume_print().json() == {}

@responses.activate
def test_get_printer_tool_state():
    _status = {
        "tool0": {
            "actual": 214.8821,
            "target": 220.0,
            "offset": 0
        },
        "tool1": {
            "actual": 25.3,
            "target": None,
            "offset": 0
        }
    }
    responses.add(responses.GET, 'http://mock:1/api/printer/tool', json=_status, status=200)
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    assert OP.get_printer_tool_state() == _status

@responses.activate
def test_get_printer_bed_state():
    _status = {
        "bed": {
            "actual": 50.221,
            "target": 70.0,
            "offset": 5
        }
    }
    responses.add(responses.GET, 'http://mock:1/api/printer/bed', json=_status, status=200)
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    assert OP.get_printer_bed_state() == _status

@responses.activate
def test_get_printer_chamber_state():
    _status = {
        "chamber": {
            "actual": 50.221,
            "target": 70.0,
            "offset": 5
        }
    }
    responses.add(responses.GET, 'http://mock:1/api/printer/chamber', json=_status, status=200)
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    assert OP.get_printer_chamber_state() == _status

@responses.activate
def test_get_printer_sd_state():
    _status = {
        "ready": True
    }
    responses.add(responses.GET, 'http://mock:1/api/printer/sd', json=_status, status=200)
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    assert OP.get_printer_sd_state() == _status

@responses.activate
def test_get_printer_profiles():
    _status = {
        "profiles": []
    }
    responses.add(responses.GET, 'http://mock:1/api/printerprofiles', json=_status, status=200)
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    assert OP.get_printer_profiles() == _status

@responses.activate
def test_get_printer_settings():
    _status = {}
    responses.add(responses.GET, 'http://mock:1/api/settings', json=_status, status=200)
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    assert OP.get_printer_settings() == _status

@responses.activate
def test_set_printer_settings():
    def request_callback_set(request):
        return (200, {}, json.dumps({'api': {'enabled': True}, 'appearance': {
                    'color': 'green'
                }}))
    responses.add_callback(
        responses.POST, 'http://mock:1/api/settings',
        callback=request_callback_set,
        content_type='application/json',
    )
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    assert OP.set_printer_settings().json() == {
        'api': {
            'enabled': True
        },
        'appearance': {
            'color': 'green'
        }
    }

@responses.activate
def test_get_slicing():
    _status = {}
    responses.add(responses.GET, 'http://mock:1/api/slicing', json=_status, status=200)
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    assert OP.get_slicing() == _status

@responses.activate
def test_get_system_commands():
    _status = {}
    responses.add(responses.GET, 'http://mock:1/api/system/commands', json=_status, status=200)
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    assert OP.get_system_commands() == _status

@responses.activate
def test_get_timelapse():
    _status = {'config': []}
    responses.add(responses.GET, 'http://mock:1/api/timelapse', json=_status, status=200)
    OP = OctoPrint('mock', 1)
    OP._set_api_key('abc')
    assert OP.get_timelapse() == _status
