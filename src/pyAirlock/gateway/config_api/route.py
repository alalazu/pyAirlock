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
Handle Host

Please refer to the [Airlock Gateway REST API](https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html#host) documentation to understand how
it works, e.g. the requirements for loading and activating a configuration.
"""

from . import element


class RouteIPV4Destination( element.ConfigElement ):
    """
    CRUD and connection management REST API for IPv4 destination route entries
    """
    ELEMENT_PATH = "routes/ipv4/destination"
    RELATIONPATH = []
    
    def _registerLookup( self ):
        return [(self.ELEMENT_PATH, "route-ipv4-destination")]
    
class RouteIPV6Destination( element.ConfigElement ):
    """
    CRUD and connection management REST API for IPv6 destination route entries
    """
    ELEMENT_PATH = "routes/ipv6/destination"
    RELATIONPATH = []
    
    def _registerLookup( self ):
        return [(self.ELEMENT_PATH, "route-ipv6-destination")]
    
class RouteIPV4Source( element.ConfigElement ):
    """
    CRUD and connection management REST API for IPv4 source route entries
    """
    ELEMENT_PATH = "routes/ipv4/source"
    RELATIONPATH = []
    
    def _registerLookup( self ):
        return [(self.ELEMENT_PATH, "route-ipv4-source")]
    
class RouteIPV6Source( element.ConfigElement ):
    """
    CRUD and connection management REST API for IPv6 source route entries
    """
    ELEMENT_PATH = "routes/ipv6/source"
    RELATIONPATH = []
    
    def _registerLookup( self ):
        return [(self.ELEMENT_PATH, "route-ipv6-source")]
    
