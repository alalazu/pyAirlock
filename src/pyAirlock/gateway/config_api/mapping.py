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
Handle Mapping

Please refer to the [Airlock Gateway REST API](https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html#mapping) documentation to understand how
it works, e.g. the requirements for loading and activating a configuration.
"""

from . import element


class Mapping( element.ConfigElement ):
    """
    CRUD and connection management REST API for mappings
    """
    ELEMENT_PATH = "mappings"
    RELATIONSHIPS = ["virtual-hosts", "back-end-groups", "openapi-documents", "graphql-documents",
                     "json-web-key-sets/remotes", "json-web-key-sets/locals",
                     "ip-address-whitelists", "ip-address-blacklists", "ip-address-blacklist-exceptions",
                     "bot-management-source-ip-address-whitelists",
                     "icap-request-client-views", "icap-request-backend-views",
                     "icap-response-client-views", "icap-response-backend-views",
                     "templates", "api-policy-services", "anomaly-shield-applications"]
    RELATIONTYPES = ["virtual-host", "back-end-group", "openapi-document", "graphql-document",
                     "remote-json-web-key-set", "local-json-web-key-set",
                     "ip-address-list", "ip-address-list", "ip-address-list",
                     "ip-address-list",
                     "icap-request-client-view", "icap-request-backend-view",
                     "icap-response-client-view", "icap-response-backend-view",
                     "mapping-template", "api-policy-service", "anomaly-shield-application"]
    
    def _registerLookup( self ):
        return [(self.ELEMENT_PATH, "mapping")]
    
    def maintenance_page( self, id: int, enable: bool=False ) -> bool:
        """
        Enable/disable maintenance page for mapping

        Parameter:
        * `id`: identifier of mapping
        """
        if enable:
            return self._post( "maintenance", id=id, expect=[204,404] )
        else:
            return self._delete( "maintenance", id=id, expect=[204,404] )
    
