import sys
import math
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kPluginCmdName = "eyeball"

kPupilFlagName = "pupil"
kIrisFlagName = "iris"
kCorneaBulgeFlagName = "corneaBulge"
kIrisConcaveFlagName = "irisConcave"




def UI():
    print 'enterUI'
    if cmds.window('eyeballWindow', exists=True):
        cmds.deleteUI('eyeballWindow')
        
    window=cmds.window('eyeballWindow', title='eyeball editor', w=300, h=300, mnb=False, mxb=False, sizeable=False)
    
    mainLayout=cmds.columnLayout(w=300, h=300, columnOffset=('both',0))
    
    #banner image
    imagePath=cmds.internalVar(upd=True)+"icon/eyeballBanner.jpg"
    cmds.image(image=imagePath, w=280)
    cmds.separator(h=15, style='none')

    #input editor
    cmds.rowColumnLayout(numberOfColumns=2, cw=[(1,100),(2,180)], columnOffset=[(1,'both',5),(2,'both',5)])
    cmds.text('iris_size', align='left')
    cmds.floatField('irisSizeField', value=2.75, cc=changeIrisSize)
    cmds.text('pupil_size', align='left')
    cmds.floatField(value=0.7)
    cmds.text('cornea_bulge', align='left')
    cmds.floatField(value=10)
    cmds.text('iris_concave', align='left')
    cmds.floatField(value=10)
    
    #reset button
    cmds.setParent(mainLayout)   
    cmds.separator(h=15, style='none')
    cmds.rowColumnLayout(numberOfColumns=2, cw=[(1,100),(2,180)], columnOffset=[(1,'both',5),(2,'both',5)])
    cmds.button(label='reset values', c=reset)
    cmds.text('')
    cmds.separator(h=5, style='none')
        
    cmds.showWindow(window)
    
def changeIrisSize(*args):
    irisSize=args[0]
    print 'enter changePupilSize'

    
def reset(*args):
    print 'enter reset'



# Command
class scriptedCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        
    # Invoked when the command is run.
    def doIt(self,argList):
        print 'enter doIt'
        self.parseArguments(argList)
        self.calcExpressions()
        self.buildEyeballGeo()



    def buildEyeballGeo(self):
#conea-------------------------------------------------------------------------------------
        #create eyeball base geometry and detach
        cmds.sphere(name='eyeballSphere', sections=20, spans=20, axis=(0,0,1), radius=0.5)     
        pieceNames = cmds.detachSurface('eyeballSphere', ch=1, rpo=1, parameter=(self.cornea_par,20))
        cmds.rename(pieceNames[0],'corneaGeo')

        #add lattice and deform cornea
        cmds.select('corneaGeo')
        latticeNames = cmds.lattice(dv=(2,2,6), oc=False)
        cmds.rename(latticeNames[0], 'corneaLat')
        cmds.rename(latticeNames[1], 'corneaLatGeo')
        cmds.rename(latticeNames[2], 'corneaLatGeoBase')
        
        cmds.createNode('transform', name='corneaDetachRider')
        cmds.createNode('transform', name='corneaDetachGrp')
        cmds.createNode('transform', name='corneaRadius')
                
        cmds.parent('corneaDetachGrp', 'corneaDetachRider', relative=True)
        cmds.parent('corneaRadius', 'corneaDetachRider', relative=True)
        cmds.parent('corneaLatGeo', 'corneaDetachGrp', relative=True)
        cmds.parent('corneaLatGeoBase', 'corneaDetachGrp', relative=True)
        
        cmds.setAttr('corneaDetachRider.translateZ', self.cornea_tz)
        cmds.setAttr('corneaRadius.translateX', self.cornea_rad)
        cmds.setAttr('corneaDetachGrp.translateZ', (0.5-self.cornea_tz)*0.5)
        cmds.setAttr('corneaDetachGrp.scaleX', self.cornea_rad*2.0)
        cmds.setAttr('corneaDetachGrp.scaleY', self.cornea_rad*2.0)
        cmds.setAttr('corneaDetachGrp.scaleZ', 0.5-self.cornea_tz)
        cmds.setAttr('corneaLatGeo.scale', 1.1, 1.1, 1.1)
        cmds.setAttr('corneaLatGeoBase.scale', 1.1, 1.1, 1.1)
        
        #deform latticeGeo
        for x in range(0,2):
            for y in range(0,2):
                for z in range(3,6):
                    pointNameStr='corneaLatGeo.pt['+str(x)+']['+str(y)+']['+str(z)+']'
                    cmds.select(pointNameStr)
                    cmds.move(0, 0, 0.05, r=True)

        #to what extend does the geometry deform from latticeGeoBase to latticeGeo
        corneaEnvelope = (1.0 - (self.linstep(0.0,11.0,self.irisFlagValue))) * (self.corneaBulgeFlagValue * 0.1);
        cmds.setAttr('corneaLat.envelope', corneaEnvelope)

#iris-----------------------------------------------------------------------------------------

        #create eyeball base geometry and detach
        cmds.sphere(name='eyeballSphere2', sections=20, spans=20, axis=(0,0,1), radius=0.5)     
        pieceNames = cmds.detachSurface('eyeballSphere2', ch=1, rpo=1, parameter=(self.iris_par,20))
        cmds.rename(pieceNames[0],'irisGeo')
        cmds.delete('eyeballSphere2')

        #add lattice and deform iris
        cmds.select('irisGeo')
        latticeNames = cmds.lattice(dv=(2,2,2), oc=False)
        cmds.rename(latticeNames[0], 'irisLat')
        cmds.rename(latticeNames[1], 'irisLatGeo')
        cmds.rename(latticeNames[2], 'irisLatGeoBase')
        
        cmds.createNode('transform', name='irisDetachRider')
        cmds.createNode('transform', name='irisDetachGrp')
        cmds.createNode('transform', name='irisRadius')
                
        cmds.parent('irisDetachGrp', 'irisDetachRider', relative=True)
        cmds.parent('irisRadius', 'irisDetachRider', relative=True)
        cmds.parent('irisLatGeo', 'irisDetachGrp', relative=True)
        cmds.parent('irisLatGeoBase', 'irisDetachGrp', relative=True)
        
        cmds.setAttr('irisDetachRider.translateZ', self.iris_tz)
        cmds.setAttr('irisRadius.translateX', self.iris_rad)
        cmds.setAttr('irisDetachGrp.translateZ', (0.5-self.iris_tz)*0.5)
        cmds.setAttr('irisLatGeo.translateZ', -0.5)
        cmds.setAttr('irisLatGeoBase.translateZ', -0.5)
        cmds.setAttr('irisLatGeo.scale', 1.1, 1.1, -2)
        cmds.setAttr('irisLatGeoBase.scale', 1.1, 1.1, 2)
        cmds.setAttr('irisDetachGrp.scaleX', self.iris_rad*2.0)
        cmds.setAttr('irisDetachGrp.scaleY', self.iris_rad*2.0)
        cmds.setAttr('irisDetachGrp.scaleZ', 0.5-self.iris_tz)
               
        #to what extend does the geometry deform from latticeGeoBase to latticeGeo
        cmds.setAttr('irisLat.envelope', self.irisConcaveFlagValue * 0.1)

#pupil----------------------------------------------------------------------------------------
        #create eyeball base geometry and detach       
        pieceNames = cmds.detachSurface('irisGeo', ch=1, rpo=1, parameter=(self.pupil_par,20))
        cmds.rename(pieceNames[0],'pupilGeo')

        #hide auxiliary nodes
        cmds.hide('corneaDetachRider')
        cmds.hide('irisDetachRider')



    def testFunc(self):
        print 'enter testFunc'


    def linstep(self, start, end, para):
        if para>=end:
            return 1;
        elif para<=start:
            return 0;
        else:
            return (para-start)/(end-start)
    
    
    def calcExpressions(self):
        # cornea translate Z
        self.cornea_tz = (math.cos(math.radians(self.irisFlagValue*9.0))) * 0.5
        # cornea radius
        self.cornea_rad  = ( math.sin(math.radians(self.irisFlagValue*9.0)) ) * 0.5
        #define nurbs surface cornea detach position
        self.cornea_par  = ((1.0 - self.linstep( 0.0,10.0,self.irisFlagValue )) * 10.0 ) + 10.0

        #define nurbs surface iris detach position
        self.iris_par = ((1.0 - ((self.irisFlagValue+0.3)*0.1)) * 10.0 ) + 10.0
        self.iris_tz =  ( math.cos(math.radians((self.irisFlagValue+0.3)*9.0)) ) * 0.485
        self.iris_rad = ( math.sin(math.radians((self.irisFlagValue+0.3)*9.0)) ) * 0.485        
        
        #define nurbs surface pupil detach position
        self.pupil_par = max( (((1.0 - ((self.pupilFlagValue)*0.1)) * 10.0 ) + 10.0), self.iris_par + 0.1 )

 
        
     
    def parseArguments(self, argList):
        print 'enter parseArg'
        #default valuess
        self.pupilFlagValue = 0.7
        self.irisFlagValue = 2.75
        self.corneaBulgeFlagValue = 10
        self.irisConcaveFlagValue = 10
       
#        argData = OpenMaya.MArgParser( self.syntax(), argList )
#         if argData.isFlagSet(kPupilFlagName):
#             self.pupilFlagValue = argData.flagArgumentInt( kPupilFlagName, 0 )
#         if argData.isFlagSet (kIrisFlagName):
#             self.irisFlagValue = argData.flagArgumentInt( kIrisFlagName, 0 )
#         if argData.isFlagSet(kCorneaBulgeFlagName):
#             self.corneaBulgeFlagValue = argData.flagArgumentInt( kCorneaBulgeFlagName, 0 )
#         if argData.isFlagSet(kIrisConcaveFlagName):
#             self.irisConcaveFlagValue = argData.flagArgumentInt( kIrisConcaveFlagName, 0 ) 

        print 'leave parseArg'




# Creator
def cmdCreator():
    return OpenMayaMPx.asMPxPtr( scriptedCommand() )
    
# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerCommand( kPluginCmdName, cmdCreator )
    except:
        sys.stderr.write( "Failed to register command: %s\n" % kPluginCmdName )
        raise

# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )