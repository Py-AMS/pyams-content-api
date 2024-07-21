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

"""PyAMS_content_api.shared.common.info module

This module defines base shared content information getter service.
"""

from colander import MappingSchema, drop
from cornice import Service
from cornice.validators import colander_validator
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound, HTTPOk

from pyams_content.shared.common.interfaces.types import IWfTypedSharedContent
from pyams_content_api.shared.common.interfaces import IContentAPIInfo, REST_CONTENT_INFO_ROUTE
from pyams_content_api.shared.common.schema import BaseContentInfo
from pyams_i18n.interfaces import II18n
from pyams_layer.skin import apply_skin
from pyams_security.interfaces.base import USE_INTERNAL_API_PERMISSION
from pyams_security.rest import check_cors_origin, set_cors_headers
from pyams_sequence.reference import get_reference_target
from pyams_utils.rest import BaseResponseSchema, http_error, rest_responses

__docformat__ = 'restructuredtext'

from pyams_zmi.skin import AdminSkin

info_service = Service(name=REST_CONTENT_INFO_ROUTE,
                       pyramid_route=REST_CONTENT_INFO_ROUTE,
                       description="PyAMS content base information service")


@info_service.options(validators=(check_cors_origin, set_cors_headers))
def info_options(request):
    """Content options endpoint"""
    return ''


class ContentInfoResponse(BaseResponseSchema):
    """Content information schema"""
    info = BaseContentInfo(description="Content info",
                           missing=drop)


class ContentInfoResult(MappingSchema):
    """Content information response"""
    body = ContentInfoResponse()


info_get_responses = rest_responses.copy()
info_get_responses[HTTPOk.code] = ContentInfoResult(
    description="Base content information result")


@info_service.get(permission=USE_INTERNAL_API_PERMISSION,
                  validators=(check_cors_origin, colander_validator, set_cors_headers),
                  response_schemas=info_get_responses)
def get_content_info(request):
    """Content information getter"""
    oid = request.matchdict['oid']
    if not oid:
        return http_error(request, HTTPBadRequest)
    apply_skin(request, AdminSkin)
    target = get_reference_target(oid, request=request)
    if target is None:
        return http_error(request, HTTPNotFound)
    info = {
        'oid': oid,
        'title': II18n(target).query_attribute('title', request=request)
    }
    if IWfTypedSharedContent.providedBy(target):
        data_type = target.get_data_type()
        if data_type is not None:
            info['data_type'] = {
                'name': data_type.__name__,
                'label': II18n(data_type).query_attribute('label', request=request)
            }
    for name, adapter in request.registry.getAdapters((target,), IContentAPIInfo):
        info[name] = adapter
    return {
        'status': 'success',
        'info': info
    }
