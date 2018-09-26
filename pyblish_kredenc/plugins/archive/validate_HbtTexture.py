import pyblish.api
from maya import cmds



class ValidateHbtTexture(pyblish.api.Validator):
    """
    Validate Hungry bear Tales Highest texture resolution on object that have
    HBT_ attributes using function from HBT_switch_tex.py
    auto switch if poossible
    """

    order = pyblish.api.ValidatorOrder - 0.01
    #families = ['Deadline']
    #category = 'texture'
    label = 'Hungry Bear Tales Tex Check'
    optional = True

    def process(self, context):
        #procces all posiible shapes parents (ie transforms)
        invalid = False

        skip = True
        if context.data.get('ftrackData'):
            if context.data['ftrackData']['Project']['code'] == 'hbt':
                skip = True # alwaYS SKIP

        if not(skip):
            import hbt_switch_tex as hbtSw
            reload(hbtSw)

            nhbtData=hbtSw.switchTexture()

            nhbtData.option = 0
            nhbtData.validatorCheck()
            nhbtData.fast = False

            if len(nhbtData.validatorSelection) > 0:
                invalid = True

            nhbtData.all = True
            nhbtData.switch()

            #try to switch materials only to 100% color without specular
            import matConvert as mCon
            reload(mCon)
            mCon.allMatsDiffuseOnly()

            #disconnect all non essential materials from shading group ie., old alSurfaceNopdes
            import maya_utils as mu
            reload(mu)
            mu.disconnectNonEssential()


            if invalid:
                self.log.info("Meshes automaticly switched to highest resolution texture.")
            else:
                self.log.info("No switching of texture necessary.")
        else:
            self.log.info("HBT texture check skipped. no HBT project.")
