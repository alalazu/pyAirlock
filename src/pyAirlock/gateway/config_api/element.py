# pyAirlock: Python library for Airlock products
# 
# Copyright (c) 2019-2024 Urs Zurbuchen <info@airlock.com>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
Base handler for configuration elements

Please refer to the [Airlock Gateway REST API](https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html) documentation to understand how
it works, e.g. the requirements for loading and activating a configuration.
"""

from typing import Union

from ...common import exception, log, lookup

class ConfigElement( object ):
    """
    Base class for CRUD and connection management REST API of all configuration elements
    """
    # path under /configuration
    ELEMENTPATH = ""
    # subpath after /configuration/.../relationships
    RELATIONPATH = None
    # config element type_name of the referenced resource
    RELATIONTYPE = []
    # key in config element data for relationships
    RELATIONDATA = None
    # Create, Read, Update, Delete, Link
    OPERATIONS = "CRUDL"
    
    def __init__( self, name, gw, run_info ):
        """
        Parameters:
		
        * `name` is a user-friendly (short) name
        * `gw` references a `pyAirlock.gateway.config_api.gateway.GW` object to communicate with the Airlock Gateway
        * `run_info` is provided by the Airscript shell and allows access to configuration and command line parameters
        """
        self._name = name
        self._gw = gw
        self._run_info = run_info
        self._log = log.Log( self.__module__, self._run_info )
        for item in self._registerLookup():
            lookup.register( lookup.PATH2TYPENAME, item[0], item[1] )
        lst_key = self.RELATIONDATA if self.RELATIONDATA else self.RELATIONPATH
        if lst_key:
            lst_typ = self.RELATIONTYPE
            for idx in range( len( lst_key )):
                key = lst_key[idx]
                if key == "":
                    continue
                try:
                    typ = lst_typ[idx]
                except IndexError:
                    typ = key
                lookup.register( lookup.RELTYPE2NAME, key, typ )
            # for idx in range( len( lst_typ )):
            #     typ = lst_typ[idx]
            #     try:
            #         key = lst_key[idx]
            #     except IndexError:
            #         key = key
            #     if key == "":
            #         continue
            #     lookup.registerWithDuplicates( lookup.TYPE2RELTYPE, typ, key )
    
    def create( self, data: dict ) -> dict:
        """
        Use REST API to create a configuration element in workspace
        
        Parameters:

        * `data`: dict with configuration element data structure. Please refer to Airlock Gateway REST API documentation (https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html) for details. Will be converted to JSON.

        Returns: REST API response element `data` as dict
        """
        if not "C" in self.OPERATIONS:
            raise exception.AirlockInvalidOperation()
        if 'relationships' in data:
            raise exception.AirlockDataConnectionError()
        data_type = self._document_type( self.ELEMENT_PATH )
        try:
            if data['type'] != data_type:
                raise exception.AirlockDataTypeError( data_type )
        except KeyError:
            raise exception.AirlockInvalidDataFormatError()
        resp = self._gw.post( f"/configuration/{self.ELEMENT_PATH}", data={'data': data}, expect=[201] )
        try:
            return resp.json()['data']
        except KeyError:
            raise exception.AirlockDataError()

    def read( self, id: int=None ) -> Union[dict, list[dict], None]:
        """
        Use REST API to fetch definition of one or all configuration elements of loaded configuration from Airlock Gateway.
        
        Parameters:

        * `id`: identifier of configuration element to retrieve, if not set, all elements are returned

        Returns:
        * REST API response element `data` as dict or list of dicts
        * may also be empty dict if call does not return any data (response code 204)
        * None if object not found
        """
        if not "R" in self.OPERATIONS:
            raise exception.AirlockInvalidOperation()
        if id:
            resp = self._gw.get( f"/configuration/{self.ELEMENT_PATH}/{id}", expect=[200,404] )
            if resp.status_code == 404:
                self._log.verbose( f"{self._name}: No such {self._document_type( self.ELEMENT_PATH )}: {id}" )
                return None
        else:
            resp = self._gw.get( f"/configuration/{self.ELEMENT_PATH}", expect=[200,404] )
            if resp.status_code == 404:
                return {}
        try:
            return resp.json()['data']
        except KeyError:
            raise exception.AirlockDataError()
    
    def update( self, id: int, data: dict ) -> Union[dict, None]:
        """
        Use REST API to update a configuration element in workspace
        
        Parameters:

        * `id`: identifier of configuration element to update
        * `data`: dict with configuration element data structure. Please refer to Airlock Gateway REST API documentation (https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html) for details. Will be converted to JSON.

        Returns:
        * REST API response element `data` as dict
        * may also be empty dict if call does not return any data (response code 204)
        * None if object not found
        """
        if not "U" in self.OPERATIONS:
            raise exception.AirlockInvalidOperation()
        try:
            del data['relationships']
        except KeyError:
            pass
        data_type = self._document_type( self.ELEMENT_PATH )
        try:
            if data['type'] != data_type:
                raise exception.AirlockDataTypeError( data_type )
        except KeyError:
            raise exception.AirlockInvalidDataFormatError()
        if "C" in self.OPERATIONS:
            # if element can be created, we have an id
            path = f"/configuration/{self.ELEMENT_PATH}/{id}"
        else:
            path = f"/configuration/{self.ELEMENT_PATH}"
        resp = self._gw.patch( path, data={'data': data}, expect=[200,404] )
        if resp.status_code == 404:
            self._log.verbose( f"{self._name}: No such {data_type}: {id}" )
            return None
        try:
            return resp.json()['data']
        except KeyError:
            raise exception.AirlockDataError()

    def delete( self, id: int, subpath: str=None, data: dict=None, expect: list[int]=[204,404] ) -> bool:
        """
        Perform REST API DELETE on object class's endpoint and return HTTP response.
        
        Parameters:

        * `id`: identifier of configuration element
        * `subpath`: configuration element specific path under REST API endpoint
        * `data`: dict with correct structure, depending on class. Please refer to Airlock Gateway REST API documentation (https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html) for details. Will be converted to JSON.
        * `expect`: list of expected HTTP response codes, other values result in exceptions

        Returns: True on success, False otherwise
        """
        if not "D" in self.OPERATIONS:
            raise exception.AirlockInvalidOperation()
        if "C" in self.OPERATIONS:
            # if element can be created, we have an id
            path = f"/configuration/{self.ELEMENT_PATH}/{id}"
        else:
            path = f"/configuration/{self.ELEMENT_PATH}"
        resp = self._gw.delete( f"{path}{self._subpath( subpath )}", data=data, expect=expect )
        if resp.status_code == 404:
            self._log.verbose( f"{self._name}: No such {self._document_type( self.ELEMENT_PATH )}: {id}" )
            return False
        return True
    
    def addConnection( self, reltype: str, id: int, relation_id: int, meta: dict=None ) -> bool:
        """
        Use REST API to add a connection

        Parameters:

        * `reltype`: type of connection to add
        * `id`: identifier of configuration element to which connection is added
        * `relation_id`: identifier of configuration element to add as new connection
        * `meta`: JSON API meta data for request, usually not required but see ICAP connections for mappings, e.g. https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html#add-icap-request-client-view

        Returns: True on success, False otherwise
        """
        if not "L" in self.OPERATIONS:
            raise exception.AirlockInvalidOperation()
        if self.RELATIONPATH == None:
            raise exception.AirlockNotSupportedError()
        if relation_id < 0:
            # builtin object
            return True
        if self.RELATIONDATA:
            try:
                idx = self.RELATIONDATA.index( reltype )
            except ValueError:
                raise exception.AirlockInvalidRelationshipTypeError()
            subpath = self.RELATIONPATH[idx]
        else:
            subpath = reltype
        if subpath[-1] == 's':
            data = {"data": [{'type': lookup.get( lookup.RELTYPE2NAME, reltype ), 'id': relation_id}]}
        else:
            data = {"data": {'type': lookup.get( lookup.RELTYPE2NAME, reltype ), 'id': relation_id}}
        if meta:
            data['meta'] = meta
        resp = self.patch( id, f"relationships/{subpath}", data=data, expect=[204,404] )
        if resp == None:
            return False
        return True

    def removeConnection( self, reltype: str, id: int, relation_id: int ) -> bool:
        """
        Use REST API to remove a connection

        Parameters:

        * `reltype`: type of connection to remove
        * `id`: identifier of configuration element from which connection is removed
        * `relation_id`: identifier of configuration element to disconnect

        Returns: True on success, False otherwise
        """
        if not "L" in self.OPERATIONS:
            raise exception.AirlockInvalidOperation()
        if self.RELATIONPATH == None:
            raise exception.AirlockNotSupportedError()
        if relation_id < 0:
            # builtin object
            return True
        if self.RELATIONDATA:
            try:
                idx = self.RELATIONDATA.index( reltype )
            except ValueError:
                raise exception.AirlockInvalidRelationshipTypeError()
            subpath = self.RELATIONPATH[idx]
        else:
            subpath = reltype
        if subpath[-1] == 's':
            data = {"data": [{'type': lookup.get( lookup.RELTYPE2NAME, reltype ), 'id': relation_id}]}
        else:
            data = {"data": {'type': lookup.get( lookup.RELTYPE2NAME, reltype ), 'id': relation_id}}
        resp = self.delete( id, f"relationships/{subpath}", data=data, expect=[204,404] )
        if not resp:
            return False
        return True

    def get( self, id: int=None, subpath: str=None, expect: list[int]=[200,404] ) -> Union[dict, list[dict], None]:
        """
        Perform REST API GET on object class's endpoint and return HTTP response.
        
        Parameters:

        * `id`: identifier of configuration element, retrieve all if no specified
        * `subpath`: configuration element specific path under REST API endpoint
        * `expect`: list of expected HTTP response codes, other values result in exceptions

        Returns:
        * REST API response element `data` as dict or list of dicts
        * may also be empty dict if call does not return any data (response code 204)
        * None if object not found
        """
        if id:
            resp = self._gw.get( f"/configuration/{self.ELEMENT_PATH}/{id}{self._subpath( subpath )}", expect=expect )
        else:
            resp = self._gw.get( f"/configuration/{self.ELEMENT_PATH}{self._subpath( subpath )}", expect=expect )
        if resp.status_code == 404:
            self._log.verbose( f"{self._name}: No such {self._document_type( self.ELEMENT_PATH )}: {id}" )
            return None
        try:
            return resp.json()['data']
        except KeyError:
            raise exception.AirlockDataError()
    
    def post( self, id: int=None, subpath: str=None, data: dict=None, expect: list[int]=[200,204,404] ) -> Union[dict, list[dict], None]:
        """
        Perform REST API POST on object class's endpoint and return HTTP response.
        
        Parameters:

        * `id`: identifier of configuration element, act on element type if not specified. e.g. create new
        * `subpath`: configuration element specific path under REST API endpoint
        * `data`: dict with correct structure, depending on class. Please refer to Airlock Gateway REST API documentation (https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html) for details. Will be converted to JSON.
        * `expect`: list of expected HTTP response codes, other values result in exceptions

        Returns:
        * REST API response element `data` as dict or list of dicts
        * may also be empty dict if call does not return any data (response code 204)
        * None if object not found
        """
        if id:
            resp = self._gw.post( f"/configuration/{self.ELEMENT_PATH}/{id}{self._subpath( subpath )}", data=data, expect=expect )
        else:
            resp = self._gw.post( f"/configuration/{self.ELEMENT_PATH}{self._subpath( subpath )}", data=data, expect=expect )
        if resp.status_code == 404:
            self._log.verbose( f"{self._name}: No such {self._document_type( self.ELEMENT_PATH )}: {id}" )
            return None
        elif resp.status_code == 204:
            return {}
        try:
            return resp.json()['data']
        except KeyError:
            raise exception.AirlockDataError()
    
    def patch( self, id: int, subpath: str=None, data: dict=None, expect: list[int]=[200,404] ) -> Union[dict, list[dict], None]:
        """
        Perform REST API PATCH on object class's endpoint and return HTTP response.
        
        Parameters:

        * `id`: identifier of configuration element
        * `subpath`: configuration element specific path under REST API endpoint
        * `data`: dict with correct structure, depending on class. Please refer to Airlock Gateway REST API documentation (https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html) for details. Will be converted to JSON.
        * `expect`: list of expected HTTP response codes, other values result in exceptions

        Returns:
        * REST API response element `data` as dict or list of dicts
        * may also be empty dict if call does not return any data (response code 204)
        * None if object not found
        """
        resp = self._gw.patch( f"/configuration/{self.ELEMENT_PATH}/{id}{self._subpath( subpath )}", data=data, expect=expect )
        if resp.status_code == 404:
            self._log.verbose( f"{self._name}: No such {self._document_type( self.ELEMENT_PATH )}: {id}" )
            return None
        elif resp.status_code == 204:
            return {}
        try:
            return resp.json()['data']
        except KeyError:
            raise exception.AirlockDataError()
    
    def put( self, id: int, subpath: str=None, data: dict=None, expect: list[int]=[200,404] ) -> Union[dict, list[dict], None]:
        """
        Perform REST API PUT on object class's endpoint and return HTTP response.
        
        Parameters:
        
        * `id`: identifier of configuration element, act on element type if not specified. e.g. import
        * `subpath`: configuration element specific path under REST API endpoint
        * `data`: dict with correct structure, depending on class. Please refer to Airlock Gateway REST API documentation (https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html) for details. Will be converted to JSON.
        * `expect`: list of expected HTTP response codes, other values result in exceptions

        Returns:
        * REST API response element `data` as dict or list of dicts
        * may also be empty dict if call does not return any data (response code 204)
        * None if object not found
        """
        if id:
            resp = self._gw.put( f"/configuration/{self.ELEMENT_PATH}/{id}{self._subpath( subpath )}", data=data, expect=expect )
        else:
            resp = self._gw.put( f"/configuration/{self.ELEMENT_PATH}{self._subpath( subpath )}", data=data, expect=expect )
        if resp.status_code == 404:
            self._log.verbose( f"{self._name}: No such {self._document_type( self.ELEMENT_PATH )}: {id}" )
            return None
        elif resp.status_code == 204:
            return {}
        try:
            return resp.json()['data']
        except KeyError:
            raise exception.AirlockDataError()
    
    def _registerLookup( self ):
        return []
    
    def _subpath( self, subpath: str ) -> str:
        if subpath:
            return f"/{subpath}"
        else:
            return ""
    
    def _document_type( self, subpath: str ) -> str:
        typename = lookup.get( lookup.PATH2TYPENAME, subpath )
        return typename if typename else subpath
    
        if subpath == "json-web-key-sets/remotes":
            return "remote-json-web-key-set"
        elif subpath == "json-web-key-sets/locals":
            return "local-json-web-key-set"
        elif subpath[:11] == "ip-address-":
            return "ip-address-list"
        elif subpath in ["bot-management-source-ip-address-whitelists", "session-dos-mitigation-source-ip-whitelists"]:
            return "ip-address-list"
        elif subpath[:9] == "mappings-":
            return "mapping"
        elif subpath == "templates":
            return "mapping-template"
        elif subpath == "client-certificates":
            return "ssl-certificate"
        elif subpath == "api-security/openapi-documents":
            return "openapi-document"
        elif subpath == "api-security/graphql-documents":
            return "graphql-document"
        elif subpath in ["training-data-collection-exclusions", "anomaly-detection-exclusions", "response-rule-exceptions"]:
            return "anomaly-shield-traffic-matcher"
        return subpath
    
