import nuke
import pyblish.api
import clique


@pyblish.api.log
class CollectDeadlineWriteNodes(pyblish.api.Collector):
    """Selects all write nodes"""

    hosts = ['nuke']
    version = (0, 1, 0)
    label = 'Write Nodes'

    def process(self, context):

        # storing plugin data
        plugin_data = {'EnforceRenderOrder': True}

        plugin_data['NukeX'] = nuke.env['nukex']

        plugin_data['Version'] = nuke.NUKE_VERSION_STRING.split('v')[0]

        # creating instances per write node
        for node in nuke.allNodes():
            if node.Class() == 'Write' and not node['disable'].getValue():
                instance = context.create_instance(name=node.name())
                instance.data['family'] = 'render'
                instance.data['families'] = ['deadline', 'writeNode']

                output_file = node['file'].getValue()

                instance.data['startFrame'] = int(nuke.Root().knob('first_frame').value())
                instance.data['endFrame'] = int(nuke.Root().knob('last_frame').value())
                self.log.info(instance.data['startFrame'])

                if '%' in output_file:
                    padding = int(output_file.split('%')[1][0:2])
                    padding_string = '%0{0}d'.format(padding)
                    tmp = '#' * padding
                    output_file = output_file.replace(padding_string, tmp)

                self.log.info(output_file)
                # populate instance with data
                instance.data['outputFilename'] = output_file

                # frame range
                start_frame = int(nuke.root()['first_frame'].getValue())
                end_frame = int(nuke.root()['last_frame'].getValue())
                if node['use_limit'].getValue():
                    start_frame = int(node['first'].getValue())
                    end_frame = int(node['last'].getValue())

                frames = '%s-%s\n' % (start_frame, end_frame)
                instance.data['startFrame'] = start_frame
                instance.data['endFrame'] = end_frame
                instance.data['frames'] = frames

                # Add collection
                collection = None
                try:
                    path = ""
                    if nuke.filename(node):
                        path = nuke.filename(node)
                    path += " [{0}-{1}]".format(start_frame, end_frame)
                    collection = clique.parse(path)
                except Exception as e:
                    self.log.warning(e)

                instance.data["collection"] = collection

                if str(node.name()) in ['Write1', 'Write_dpx']:
                    compname = 'main'
                else:
                    compname = node.name()

                # adding ftrack data to activate processing
                instance.data['ftrackComponents'] = {compname: {}}
                self.log.debug('component name: {}'.format(compname))

                instance.add(node)
