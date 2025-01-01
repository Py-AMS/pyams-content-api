# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

__docformat__ = 'restructuredtext'

from pyramid.interfaces import IRequest

from pyams_content.component.association import IAssociationContainer, IAssociationContainerTarget
from pyams_content.component.association.interfaces import IAssociationParagraph
from pyams_content_api.component.paragraph import JSONBaseParagraphExporter
from pyams_content_api.feature.json import IJSONExporter
from pyams_utils.adapter import adapter_config


@adapter_config(name='associations',
                required=(IAssociationContainerTarget, IRequest),
                provides=IJSONExporter)
@adapter_config(required=(IAssociationParagraph, IRequest),
                provides=IJSONExporter)
class JSONAssociationParagraphExporter(JSONBaseParagraphExporter):
    """JSON association paragraph exporter"""
    
    def convert_content(self, **params):
        result = super().convert_content(**params)
        associations = []
        registry = self.request.registry
        container = IAssociationContainer(self.context)
        for association in container.get_visible_items(self.request):
            exporter = registry.queryMultiAdapter((association, self.request), IJSONExporter)
            if exporter is not None:
                output = exporter.to_json(**params)
                if output:
                    associations.append(output)
        if associations:
            result['associations'] = associations
        return result
        