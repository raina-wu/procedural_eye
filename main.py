import maya.cmds as cmds

cmds.flushUndo()

print cmds.pluginInfo('eyeball.py', query=True, loaded=True)

if cmds.pluginInfo('eyeball.py', query=True, loaded=True):
    cmds.select(all=True)
    cmds.delete()
    cmds.unloadPlugin('eyeball.py')
    
cmds.loadPlugin('eyeball.py')
     
cmds.eyeball( pupil=1 )


# import eyeball
# 
# reload(eyeball)
# eyeball.UI()
