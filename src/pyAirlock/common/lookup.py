"""
AirScript: Airlock (Gateway) Configuration Script

Copyright (c) 2019-2024 Urs Zurbuchen <urs.zurbuchen@ergon.ch>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

lookup_tables = {}

def register( table: str, src: str, dst: str ):
    global lookup_tables
    if not table in lookup_tables:
        lookup_tables[table] = {}
    lookup_tables[table][src] = dst

def registerBoth( table_fwd: str, table_rev: str, one: str, two: str ):
    register( table_fwd, one, two )
    register( table_rev, two, one )

def get( table: str, key: str ) -> str:
    global lookup_tables
    try:
        return lookup_tables[table][key]
    except KeyError:
        return None
