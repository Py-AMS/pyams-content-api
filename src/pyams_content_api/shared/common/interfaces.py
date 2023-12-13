#
# Copyright (c) 2015-2023 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_content_api.shared.common.interfaces module

This module defines API related interfaces which are common to all shared contents.
"""

from zope.interface import Interface


__docformat__ = 'restructuredtext'


REST_CONTENT_PUBLIC_SEARCH_ROUTE = 'pyams_content.rest.search'
REST_CONTENT_PUBLIC_SEARCH_ROUTE_SETTING = 'pyams_content.api.rest.shared_content_search_route'
REST_CONTENT_PUBLIC_SEARCH_ROUTE_DEFAULT = '/api/content/rest/{content_type}'

REST_CONTENT_PUBLIC_GETTER_ROUTE = 'pyams_content.rest.getter'
REST_CONTENT_PUBLIC_GETTER_ROUTE_SETTING = 'pyams_content.api.rest.shared_content_getter_route'
REST_CONTENT_PUBLIC_GETTER_ROUTE_DEFAULT = '/api/content/rest/{content_type}/{oid}'

REST_CONTENT_INFO_ROUTE = 'pyams_content.rest.info'
REST_CONTENT_INFO_ROUTE_SETTING = 'pyams_content.api.rest.info_getter_route'
REST_CONTENT_INFO_ROUTE_DEFAULT = '/api/content/rest/{oid}/info'


class IContentAPIInfo(Interface):
    """Shared content API additional info"""
