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

RELTYPE2NAME = "reltype2typename"
PATH2TYPENAME = "path2typename"
TYPE2RELTYPE = "path2reltype"

lookup_tables = {}

def register( table: str, src: str, dst: str ):
    global lookup_tables
    if not table in lookup_tables:
        lookup_tables[table] = {}
    lookup_tables[table][src] = dst

def registerBoth( table_fwd: str, table_rev: str, one: str, two: str ):
    register( table_fwd, one, two )
    register( table_rev, two, one )

# def registerWithDuplicates( table: str, src: str, dst: str ):
#     global lookup_tables
#     if not table in lookup_tables:
#         lookup_tables[table] = {}
#     if src in lookup_tables[table] and lookup_tables[table][src] != dst:
#         if isinstance( lookup_tables[table][src], list ):
#             lookup_tables[table][src].append( dst )
#             print( f"LOOKUP REGISTER {table}:{src} - multiple values: {lookup_tables[table][src]}" )
#         else:
#             lookup_tables[table][src] = [lookup_tables[table][src], dst]
#             print( f"LOOKUP REGISTER {table}:{src} - multiple values: {lookup_tables[table][src]}" )
#     else:
#         lookup_tables[table][src] = dst

def get( table: str, key: str ) -> str:
    global lookup_tables
    try:
        return lookup_tables[table][key]
    except KeyError:
        return None

