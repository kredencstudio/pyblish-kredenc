import pyblish.api
import os
from maya import cmds
import pymel

@pyblish.api.log
class ValidateAssembly(pyblish.api.Validator):
    """"""

    families = ['model']
    optional = True
    label = 'Model - Assembly'

    def process(self, instance):


        for node in instance:

            node = pymel.core.PyNode(node)

            root = node.root()


            asset = os.getenv("ASSET_BUILD")

            # msg = 'Your model needs to be grouped\
            #     as |%s_geo_grp' % asset
            # assert root == "|%s_geo_grp" % asset, msg

            nodes = None
            nodes = pymel.core.ls(node.getChildren(), dag=True, exactType="transform")

            if not nodes:
                nodes = [node]

            id_fail = []
            name_fail = []
            for node in nodes:
                asset_attr = '{}.assetid'.format(node)
                msg = '{} is missing assetid attribute'.format(node)
                if not cmds.objExists(asset_attr):
                    self.log.warning(msg)
                    id_fail.append(node)

                if not node.endswith('_geo'):
                    self.log.warning('{} name must end with "_geo"'.format(node))
                    name_fail.append(node)

            assert (len(id_fail) == len(name_fail) == 0), 'Validation failed'
