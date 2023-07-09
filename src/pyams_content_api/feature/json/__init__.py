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

"""PyAMS_content_api.feature.json module

This module defines base JSON exporter class.
"""

__docformat__ = 'restructuredtext'

from pyams_content_api.feature.json.interfaces import IJSONExporter
from pyams_file.interfaces.thumbnail import IThumbnails
from pyams_i18n.interfaces import II18n, INegotiator
from pyams_utils.adapter import ContextRequestAdapter
from pyams_utils.interfaces.text import IHTMLRenderer
from pyams_utils.registry import get_pyramid_registry, get_utility
from pyams_utils.url import absolute_url


class JSONBaseExporter(ContextRequestAdapter):
    """JSON base exporter"""

    def to_json(self, **params):
        """JSON converter"""
        lang = params.get('lang')
        if not lang:
            negotiator = get_utility(INegotiator)
            params['lang'] = negotiator.server_language
        result = self.convert_content(**params)
        registry = get_pyramid_registry()
        target = self.conversion_target
        if target is None:
            return result
        for name, converter in registry.getAdapters((target, self.request), IJSONExporter):
            if not name:  # exclude this default adapter
                continue
            if (('included' in params) and (name not in params['included'].split(','))) or \
                    (('excluded' in params) and (name in params['excluded'].split(','))):
                continue
            output = converter.to_json(**params)
            if not output:
                continue
            if converter.is_inner:
                result.update({name: output})
            else:
                result.update(output)
        return result

    @property
    def conversion_target(self):
        """Conversion target getter"""
        return self.context

    def convert_content(self, **params):
        """Base context converter"""
        return {}

    def get_attribute(self, result, attr, name=None, converter=None, context=None):
        """Get standard attribute"""
        if context is None:
            context = self.context
        if not hasattr(context, attr):
            return
        if name is None:
            name = attr
        value = getattr(context, attr)
        if value or (value is False):
            if converter is not None:
                value = converter(value)
            result[name] = value

    def get_i18n_attribute(self, result, attr, lang, name=None, context=None):
        """Get localized attribute"""
        if context is None:
            context = self.context
        if not hasattr(context, attr):
            return
        if name is None:
            name = attr
        if lang:
            value = II18n(context).query_attribute(attr, lang=lang)
            if value:
                result[name] = value

    def get_html_attribute(self, result, attr, lang, name=None, context=None):
        """Get HTML attribute"""
        if context is None:
            context = self.context
        if not hasattr(context, attr):
            return
        if name is None:
            name = attr
        if lang:
            value = II18n(context).query_attribute(attr, lang=lang)
            if value:
                renderer = self.request.registry.queryMultiAdapter((value, self.request),
                                                                   IHTMLRenderer,
                                                                   name='oid_to_href')
                if renderer is not None:
                    result[name] = renderer.render()

    def get_list_attribute(self, result, items, name, **params):
        """Get list as inner """
        registry = get_pyramid_registry()
        values = []
        for item in items:
            converter = registry.queryMultiAdapter((item, self.request), IJSONExporter)
            if converter is not None:
                value = converter.to_json(params)
                if value:
                    values.append(value)
        if values:
            result[name] = values

    def get_file_url(self, attr, context=None, **params):
        """Get file URL"""
        if context is None:
            context = self.context
        file = getattr(context, attr, None)
        if isinstance(file, dict):
            file = file.get(params.get('lang'))
        if not file:
            return None
        return absolute_url(file, self.request)

    def get_image_url(self, attr, context=None, **params):
        """Get image URL"""
        if context is None:
            context = self.context
        image = getattr(context, attr, None)
        if isinstance(image, dict):
            image = image.get(params.get('lang'))
        if not image:
            return None
        thumbnails = IThumbnails(image, None)
        if thumbnails is not None:
            display_name = params.get('display_name')
            display_size = params.get('display_size', 'w800')
            if display_name:
                thumbnail = thumbnails.get_thumbnail('{}:{}'.format(display_name, display_size))
            else:
                thumbnail = thumbnails.get_thumbnail(display_size)
            return absolute_url(thumbnail, self.request)
        return absolute_url(image, self.request)
