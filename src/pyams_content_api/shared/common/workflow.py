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

"""PyAMS_content_api.shared.common.workflow module

This module defines adapters for JSON workflow information output.
"""

from pyramid.interfaces import IRequest

from pyams_content.shared.common import IWfSharedContent
from pyams_content_api.feature.json import IJSONExporter, JSONBaseExporter
from pyams_utils.adapter import adapter_config
from pyams_utils.timezone import tztime
from pyams_workflow.interfaces import IWorkflowPublicationInfo, IWorkflowState

__docformat__ = 'restructuredtext'


@adapter_config(name='workflow',
                required=(IWfSharedContent, IRequest),
                provides=IJSONExporter)
class JSONSharedContentWorkflowExporter(JSONBaseExporter):
    """JSON shared content workflow exporter"""

    is_inner = True

    def convert_content(self, **params):
        """JSON workflow conversion"""
        result = super().convert_content(**params)
        state = IWorkflowState(self.context, None)
        if state is not None:
            result['state'] = state.state
            result['version'] = state.version_id
        pub_info = IWorkflowPublicationInfo(self.context, None)
        if pub_info is not None:
            if pub_info.publication_effective_date:
                result['publication_date'] = tztime(pub_info.publication_effective_date).isoformat()
            if pub_info.publication_expiration_date:
                result['expiration_date'] = tztime(pub_info.publication_expiration_date).isoformat()
        return result
