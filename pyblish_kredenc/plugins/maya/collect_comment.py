import pyblish.api


class CollectComment(pyblish.api.Collector):
    """Find and collect optional comment"""
    hosts = ["maya"]

    def process(self, context):
        from maya import cmds
        if not cmds.objExists("comment.notes"):
            return

        comment = cmds.getAttr("comment.notes")
        instance = context.create_instance("Comment", family="comment")
        instance.set_data("value", comment)
        self.log.info("Found \"%s\"" % comment)
