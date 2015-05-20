import sys
import os
import json
import base64

import pyblish.api

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyblish_utils

import ftrack
import ft_utils


@pyblish.api.log
class SelectFtrack(pyblish.api.Selector):
    """Selects current workfile"""

    order = pyblish.api.Selector.order + 0.5
    hosts = ['*']
    version = (0, 1, 0)

    host = sys.executable.lower()

    def process_context(self, context):

        decodedEventData = json.loads(
            base64.b64decode(
                os.environ.get('FTRACK_CONNECT_EVENT')
            )
        )

        taskid = decodedEventData.get('selection')[0]['entityId']

        ft_context = ft_utils.getContext(taskid)

        context.set_data('ft_context', value=ft_context)

        self.log.info('Found ftrack data')