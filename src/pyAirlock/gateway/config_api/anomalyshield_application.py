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
Handle Anomaly Shield Application

Please refer to the [Airlock Gateway REST API](https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html#api-policy-service)
documentation to understand how it works, e.g. the requirements for loading and activating a configuration.
"""

from . import element


class AnomalyShieldApplication( element.ConfigElement ):
    """
    CRUD and connection management REST API for Anomaly Shield applications
    """
    ELEMENT_PATH = "anomaly-shield-applications"
    RELATIONSHIPS = ["mappings", "anomaly-shield-rules", "training-data-collection-exclusions", "anomaly-detection-exclusions", "response-rule-exceptions"]
    RELATIONTYPES = ["mapping", "anomaly-shield-rule", "anomaly-shield-traffic-matcher", "anomaly-shield-traffic-matcher", "anomaly-shield-traffic-matcher"]
    
    def _registerLookup( self ):
        return [(self.ELEMENT_PATH, "anomaly-shield-application")]
    
