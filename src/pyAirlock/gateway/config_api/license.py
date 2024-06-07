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
Handle License

Please refer to the [Airlock Gateway REST API](https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html#host) documentation to understand how
it works, e.g. the requirements for loading and activating a configuration.
"""

from typing import Union

from . import element
from pyAirlock.common import exception


class License( element.ConfigElement ):
    """
    REST API to handle Airlock Gateway license
    """
    ELEMENT_PATH = "license"
    RELATIONSHIPS = []
    OPERATIONS = "RUD"
    
    def _registerLookup( self ):
        return [(self.ELEMENT_PATH, "license-response")]
    
    def update( self, id: int, data: dict ) -> Union[dict, None]:
        """
        Use REST API to upload license to workspace
        
        Parameters:

        * `id`: identifier of configuration element to update
        * `data`: dict with configuration element data structure. Please refer to Airlock Gateway REST API documentation (https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html) for details. Will be converted to JSON.

        Returns:
        * REST API response element `data` as dict
        """
        try:
            del data['relationships']
        except KeyError:
            pass
        try:
            if data['type'] != self.ELEMENT_PATH:
                raise exception.AirlockDataTypeError( self.ELEMENT_PATH )
        except KeyError:
            raise exception.AirlockInvalidDataFormatError()
        resp = self._gw.patch( f"/configuration/{self.ELEMENT_PATH}", data={'data': data}, expect=[200] )
        try:
            return resp.json()['data']
        except KeyError:
            raise exception.AirlockDataError()

