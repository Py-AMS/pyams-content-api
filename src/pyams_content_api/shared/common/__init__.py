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

"""PyAMS_content_api.shared.common module

This module defines base JSON shared content exporter.
"""

__docformat__ = 'restructuredtext'

from pyramid.interfaces import IRequest

from pyams_content.shared.common import IWfSharedContent
from pyams_content_api.feature.json import IJSONExporter, JSONBaseExporter
from pyams_content_api.shared.common.interfaces import REST_CONTENT_PUBLIC_GETTER_PATH, \
    REST_CONTENT_PUBLIC_GETTER_ROUTE_SETTING
from pyams_sequence.interfaces import ISequentialIdInfo
from pyams_utils.adapter import adapter_config
from pyams_utils.url import canonical_url


@adapter_config(required=(IWfSharedContent, IRequest),
                provides=IJSONExporter)
class JSONSharedContentExporter(JSONBaseExporter):
    """Default shared content JSON exporter"""

    getter_route_setting = REST_CONTENT_PUBLIC_GETTER_ROUTE_SETTING
    getter_route_default = REST_CONTENT_PUBLIC_GETTER_PATH

    def convert_content(self, **params):
        """Base context converter"""
        result = super().convert_content(**params)
        context = self.context
        lang = params.get('lang')
        sequence = ISequentialIdInfo(context)
        result['oid'] = sequence.hex_oid
        result['base_oid'] = sequence.get_base_oid().strip()
        getter_route = self.request.registry.settings.get(self.getter_route_setting,
                                                          self.getter_route_default)
        result['api_url'] = getter_route.format(content_type=self.context.content_type,
                                                oid=sequence.hex_oid)
        self.get_i18n_attribute(result, 'title', lang)
        if context.handle_short_name:
            self.get_i18n_attribute(result, 'short_name', lang)
        if context.handle_content_url:
            self.get_attribute(result, 'content_url')
            result['public_url'] = canonical_url(context, self.request)
        if context.handle_header:
            self.get_i18n_attribute(result, 'header', lang)
        if context.handle_description:
            self.get_i18n_attribute(result, 'description', lang)
        return result
