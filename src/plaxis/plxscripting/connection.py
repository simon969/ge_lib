"""
Purpose: provides low level methods to fire commands to a server.
    The methods accept commmand line strings and return JSON for parsing by
    the client.

Subversion data:
    $Id: connection.py 19385 2015-06-01 12:49:43Z tj $
    $URL: https://tools.plaxis.com/svn/sharelib/trunk/PlxObjectLayer/Server/plxscripting/connection.py $

Copyright (c) Plaxis bv. All rights reserved.

Unless explicitly acquired and licensed from Licensor under another
license, the contents of this file are subject to the Plaxis Public
License ("PPL") Version 1.0, or subsequent versions as allowed by the PPL,
and You may not copy or use this file in either source code or executable
form, except in compliance with the terms and conditions of the PPL.

All software distributed under the PPL is provided strictly on an "AS
IS" basis, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, AND
LICENSOR HEREBY DISCLAIMS ALL SUCH WARRANTIES, INCLUDING WITHOUT
LIMITATION, ANY WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE, QUIET ENJOYMENT, OR NON-INFRINGEMENT. See the PPL for specific
language governing rights and limitations under the PPL.
"""

from . import requests
import json
import time
import uuid
import re

# import encryption
from . import encryption

from .const import (ENVIRONMENT, ACTION, COMMANDS, NAME, FILENAME, INTERNAL_SERVER_ERROR,
                    MEMBERS, NAMED_OBJECTS, PROPERTY_VALUES, LIST,
                    LIST_QUERIES, ENUMERATION, SELECTION, OWNER, PROPERTYNAME,
                    PHASEGUID, OBJECTS, NULL_GUID, JSON_KEY_RESPONSE,
                    JSON_KEY_CODE, JSON_KEY_REQUEST_DATA, JSON_KEY_REPLY_CODE)

from .plx_scripting_exceptions import PlxScriptingError, EncryptionError

JSON_HEADER = {"content-type": "application/json"}
MAD_EXCEPTION_ITEMS_TO_KEEP = ['operating system', 'program up time', 'processors', 'physical memory',
                               'free disk space', 'executable', 'version   ', 'exception class', 'exception message']


def clean_mad_exception_log(exception):
    matches = re.findall(r'^(.*): (.*)$', exception, re.MULTILINE)
    matches = [match for match in matches if any([item in match[0] for item in MAD_EXCEPTION_ITEMS_TO_KEEP])]

    is_async_exception = False
    for index, match in enumerate(matches):
        if 'Original call stack' in match[0]:
            is_async_exception = True
            matches[index] = (match[0].replace('Original call stack', '') + '\r\n').split(': ')
    cleaned_exception = '\n'.join(['{}: {}'.format(*match) for match in matches])

    if is_async_exception:
        start_tag = 'thread'
        end_tag = 'main thread'
    else:
        start_tag = 'main thread'
        end_tag = 'thread'
    main_thread = re.search(r'{} .*?:.*?{}'.format(start_tag, end_tag), exception, re.DOTALL)
    if main_thread:
        cleaned_exception += '\n' + main_thread.group(0).replace('\r\n{}'.format(end_tag), '')
    return cleaned_exception


class Response(object):
    def __init__(self, response, text, json_dict):
        self.reason = response.reason
        self.url = response.url
        self.status_code = response.status_code
        self.text = text
        self.json_dict = json_dict
        self.ok = response.ok
        self.headers = response.headers

    def json(self):
        return self.json_dict


class EncryptionHandler(object):
    def __init__(self, password):
        self._password = password
        self._reply_code = ""
        self._last_request_data = ""

    @property
    def last_request_data(self):
        return self._last_request_data

    def encrypt(self, payload):
        if JSON_KEY_REPLY_CODE in payload:
            raise EncryptionError("Payload must not have {} field before"
                                  " encryption.".format(JSON_KEY_REPLY_CODE))

        self._reply_code = uuid.uuid4().hex
        payload[JSON_KEY_REPLY_CODE] = self._reply_code
        jsondata = json.dumps(payload)
        self._last_request_data = jsondata

        encrypted_jsondata, init_vector = encryption.encrypt(
            jsondata, self._password)

        outer = {}
        outer[JSON_KEY_CODE] = init_vector
        outer[JSON_KEY_REQUEST_DATA] = encrypted_jsondata
        return json.dumps(outer)

    def decrypt(self, response):
        response_json = response.json()
        encrypted_response = response_json[JSON_KEY_RESPONSE]
        init_vector = response_json[JSON_KEY_CODE]
        decrypted_response_text = encryption.decrypt(encrypted_response, init_vector,
                                                     self._password)

        if len(decrypted_response_text) == 0:
            raise EncryptionError("Couldn't decrypt response.")

        decrypted_response = json.loads(decrypted_response_text)
        # Detect possible MITM attacks by verifying the reply code.
        if decrypted_response[JSON_KEY_REPLY_CODE] != self._reply_code:
            raise EncryptionError("Reply code is different from what "
                                  "was sent! Server might be spoofed!")

        return Response(response, decrypted_response_text, decrypted_response)


class HTTPConnection():
    """
    Simple helper class which provides methods to make http requests to
    a server. Accepts string input and provides JSON output.
    """

    def __init__(self, host, port, timeout=5.0, request_timeout=None, password='', error_mode=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.request_timeout = request_timeout
        self.requests_count = 0
        self.logger = None
        self._password = password
        self.session = requests.session()
        self.error_mode = error_mode

        self.HTTP_HOST_PREFIX = "http://{0}:{1}/".format(host, str(port))

        self.ENVIRONMENT_ACTION_PREFIX = (self.HTTP_HOST_PREFIX + ENVIRONMENT)

        self.COMMAND_ACTION_PREFIX = (self.HTTP_HOST_PREFIX + COMMANDS)

        self.QUERY_MEMBER_NAMES_ACTION_PREFIX = (
            self.HTTP_HOST_PREFIX + MEMBERS)

        self.QUERY_NAMED_OBJECT_ACTION_PREFIX = (
            self.HTTP_HOST_PREFIX + NAMED_OBJECTS)

        self.QUERY_PROPERTY_VALUES_ACTION_PREFIX = (
            self.HTTP_HOST_PREFIX + PROPERTY_VALUES)

        self.QUERY_LIST_PREFIX = (self.HTTP_HOST_PREFIX + LIST)

        self.QUERY_ENUMERATION_PREFIX = self.HTTP_HOST_PREFIX + ENUMERATION

        self.QUERY_SELECTION_PREFIX = self.HTTP_HOST_PREFIX + SELECTION

        self._wait_for_server()
    
    # 
    # Code Change 2022/01/17: S Thomson 
    # 
    # Python 3.8 reports: AttributeError: module 'time' has no attribute 'clock'
    # https://stackoverflow.com/questions/58569361/attributeerror-module-time-has-no-attribute-clock-in-python-3-8
    # 
    # def _wait_for_server(self):
    #     start_time = time.clock()
    #     while time.clock() < start_time + self.timeout:
    #         if self.poll_connection():
    #             break
    #         time.sleep(0.1)
    #

    def _wait_for_server(self):
        start_time = time.time()
        while time.time() < start_time + self.timeout:
            if self.poll_connection():
                break
            time.sleep(0.1)
        

    def poll_connection(self):
        """
        Verify the validity of the connection by polling for a non-existant object.
        """
        payload = {ACTION: {MEMBERS: [NULL_GUID]}}
        try:
            self._send_request(self.QUERY_MEMBER_NAMES_ACTION_PREFIX, payload)
            return True
        except PlxScriptingError:
            return True
        except requests.exceptions.ConnectionError:
            return False

    def _send_request(self, operation_address, payload):
        """
        Posts the supplied JSON payload to the supplied operation address and
        returns the result.
        """
        response = self._send_request_and_get_response(operation_address, payload)
        if not response.ok:
            if self.error_mode.should_raise:
                exception_parts = [response.reason]
                if response.status_code == INTERNAL_SERVER_ERROR:
                    exception_parts.append(clean_mad_exception_log(response.json().get('bugreport', '')))
                raise PlxScriptingError('\n'.join(exception_parts))
        return response

    def _send_request_and_get_response(self, operation_address, payload):
        if self._password:
            encryption_handler = EncryptionHandler(self._password)
            json_payload = encryption_handler.encrypt(payload)
            log_payload = encryption_handler.last_request_data
        else:
            json_payload = json.dumps(payload)
            log_payload = json_payload

        if self.logger is not None:
            self.logger.log_request_start(log_payload)

        response = self.session.post(operation_address, data=json_payload,
                                     headers=JSON_HEADER, timeout=self.request_timeout)

        # Some APIs do not set a response object. In that case don't try to decrypt
        if self._password and response.text != '':
            response = encryption_handler.decrypt(response)

        if self.logger is not None:
            self.logger.log_request_end(response)

        self.requests_count += 1
        return response

    def request_environment(self, command_string, filename=''):
        """
        Send a Plaxis environment command to the server, such as creating a
        new project. A specific filename may be provided when opening a
        project. Returns the response text from the server.
        """
        payload = {ACTION: {NAME: command_string, FILENAME: filename}}
        request = self._send_request(self.ENVIRONMENT_ACTION_PREFIX, payload)
        return request.reason

    def request_commands(self, *commands):
        """
        Send a regular Plaxis command action (non-environment) to the server
        such as going to mesh mode, or creating a line.
        """
        payload = {ACTION: {COMMANDS: commands}}
        r = self._send_request(self.COMMAND_ACTION_PREFIX, payload)
        return r.json()

    def request_members(self, *guids):
        """
        Send a query to the server to retrieve the member names of a number
        objects, identified by their GUID.
        E.g. sending a GUID for a geometric object will return all its
        commands and intrinsic properties.
        """
        payload = {ACTION: {MEMBERS: guids}}
        request = self._send_request(self.QUERY_MEMBER_NAMES_ACTION_PREFIX, payload)
        return request.json()

    def request_namedobjects(self, *object_names):
        """
        Send a query to the server to retrieve representations of one or more
        objects as they are named in Plaxis. Note that this requires the user
        to know in advance what those names are.
        """
        payload = {ACTION: {NAMED_OBJECTS: object_names}}
        request = self._send_request(self.QUERY_NAMED_OBJECT_ACTION_PREFIX, payload)
        return request.json()

    def request_propertyvalues(self, owner_guid, property_name, phase_guid=""):
        """
        Send a query to the server to retrieve the property values of a
        number of objects identified by their GUID.
        Properties that have primitive values will be represented as such,
        while properties that are objects are represented as GUIDs.
        """
        payload = {ACTION: {PROPERTY_VALUES: {OWNER: owner_guid,
                                              PROPERTYNAME: property_name,
                                              PHASEGUID: phase_guid}}}
        request = self._send_request(
            self.QUERY_PROPERTY_VALUES_ACTION_PREFIX, payload)
        return request.json()

    def request_list(self, *list_queries):
        """
        Send a query to the server to perform a number of actions upon lists.
        The 'list_queries' argument consists of a list of dictionaries where
        the dictionary contains "guid", "method" and "parameters" keys and
        fields.
        """
        payload = {ACTION: {LIST_QUERIES: list_queries}}
        request = self._send_request(self.QUERY_LIST_PREFIX, payload)
        return request.json()

    def request_enumeration(self, *guids):
        """
        Send a query to the server to retrieve all possible enumeration strings
        for one or more guids that relate to enumeration objects.
        """
        payload = {ACTION: {ENUMERATION: guids}}
        request = self._send_request(self.QUERY_ENUMERATION_PREFIX, payload)
        return request.json()

    def request_selection(self, command, *guids):
        """
        Send a query to the server to alter and retrieve the current selection
        for a number of objects represented by their GUID.
        """
        payload = {ACTION: {NAME: command, OBJECTS: guids}}
        request = self._send_request(self.QUERY_SELECTION_PREFIX, payload)
        return request.json()

    def request_server_name(self):
        """
        Send a query to the server to capture the server name from response headers
        """
        payload = {ACTION: {MEMBERS: [NULL_GUID]}}
        response = self._send_request_and_get_response(self.QUERY_MEMBER_NAMES_ACTION_PREFIX, payload)
        return response.headers.get('Server')
