import pyblish.api
import pymel


class ValidateConstructionHistory(pyblish.api.Validator):
    """ Ensure no construction history exists on the nodes in the instance """

    families = ['model']
    optional = True
    label = 'Model - Construction History'

    def process(self, instance):
        """Process all the nodes in the instance """

        check = True

        # for node in cmds.ls(type='transform'):
        for node in instance:

            node = pymel.core.PyNode(node)

            # skipping references
            if not node.isReferenced():

                self.log.info('Validating: {}'.format(node.name()))

                history = node.listHistory(pruneDagObjects=True)
                if history:
                    for h in history:
                        if not h.isReferenced():
                            msg = 'Node "%s" has construction' % node
                            msg += ' history: %s' % h
                            self.log.error(msg)
                            check = False


        assert check, 'Nodes in the scene has construction history.'
