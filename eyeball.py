import sys
import math
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx


gPupilValue = 0.7
gIrisValue = 2.75
gCorneaBulgeValue = 10
gIrisConcaveValue = 10

gNamespace='eyeball1'
#gEyeballCtrler='eyeballCtrl1'

def run():

    UI()
    
    
    
def createNew(*args):

    buildEyeballGeo()

    
    
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
    
    #buttons
    cmds.setParent(mainLayout)   
    cmds.separator(h=15, style='none')
    cmds.rowColumnLayout(numberOfColumns=2, cw=[(1,100),(2,180)], columnOffset=[(1,'both',5),(2,'both',5)])
    cmds.button(label='reset values', c=reset)
    cmds.button(label='create new', c=createNew)
    cmds.button(label='setCurrent')
    cmds.separator(h=5, style='none')
        
    cmds.showWindow(window)
    
    
    
def changeIrisSize(*args):
    irisSize=args[0]
    print 'enter changePupilSize'

    
def reset(*args):
    selected=cmds.ls(selection=True)
    if len(selected)!=1 or cmds.nodeType(selected[0])!='locator':
        raise RuntimeError, 'Please select one eyeControler.'
    else:
        print 'enter reset, selected:'
        print selected



def linstep(start, end, para):
    if para>=end:
        return 1;
    elif para<=start:
        return 0;
    else:
        return (para-start)/(end-start)



def buildEyeballGeo():  

#create eyeball controler-----------------------------------------------------------------------------------------


    gEyeballCtrler=cmds.spaceLocator()[0]
    cmds.addAttr(longName='pupilSize', attributeType='float', keyable=True, defaultValue=0.7)
    cmds.addAttr(longName='irisSize', attributeType='float', keyable=True, defaultValue=2.75)
    cmds.addAttr(longName='irisConcave', attributeType='float', keyable=True, defaultValue=10)
    cmds.addAttr(longName='corneaBulge', attributeType='float', keyable=True, defaultValue=10)
    
    
#cornea-----------------------------------------------------------------------------------------

    #create eyeball base geometry and detach
    eyeballSphere=cmds.sphere(sections=20, spans=20, axis=(0,0,1), radius=0.5)[0]
#     eyeballSphere=eyeballSphere[0]
    pieceNames = cmds.detachSurface(eyeballSphere, ch=1, rpo=1, parameter=(0.1,20))
    corneaGeo=pieceNames[0];
    corneaDetach=pieceNames[2];
    cmds.parent(eyeballSphere, gEyeballCtrler, relative=True)
    cmds.parent(corneaGeo, gEyeballCtrler, relative=True)

    #add lattice and deform cornea
    cmds.select(corneaGeo)
    (corneaLat,corneaLatGeo,corneaLatGeoBase)= cmds.lattice(dv=(2,2,6), oc=False)
    cmds.setAttr(corneaLatGeo+'.scale', 1.1, 1.1, 1.1)
    cmds.setAttr(corneaLatGeoBase+'.scale', 1.1, 1.1, 1.1)
    
    corneaDetachRider=cmds.createNode('transform')
    corneaDeformGrp=cmds.createNode('transform')
    corneaRadius=cmds.createNode('transform')
            
    cmds.parent(corneaDeformGrp, corneaDetachRider, relative=True)
    cmds.parent(corneaRadius, corneaDetachRider, relative=True)
    cmds.parent(corneaLatGeo, corneaDeformGrp, relative=True)
    cmds.parent(corneaLatGeoBase, corneaDeformGrp, relative=True)
    cmds.parent(corneaDetachRider, gEyeballCtrler, relative=True)
    
    cmds.hide(corneaDetachRider)
    
    
#iris-----------------------------------------------------------------------------------------

    #create eyeball base geometry and detach
    eyeballSphere2=cmds.sphere(sections=20, spans=20, axis=(0,0,1), radius=0.5)[0]
    pieceNames = cmds.detachSurface(eyeballSphere2, ch=1, rpo=1, parameter=(0.1,20))
    irisGeo=pieceNames[0]
    irisDetach=pieceNames[2]
    cmds.delete(eyeballSphere2)
    cmds.parent(irisGeo, gEyeballCtrler, relative=True)

    #add lattice and deform iris
    cmds.select(irisGeo)
    (irisLat,irisLatGeo,irisLatGeoBase) = cmds.lattice(dv=(2,2,2), oc=False)
    cmds.setAttr(irisLatGeo+'.scale', 1.1, 1.1, -2)
    cmds.setAttr(irisLatGeoBase+'.scale', 1.1, 1.1, 2)
    cmds.setAttr(irisLatGeo+'.translateZ', -0.5)
    cmds.setAttr(irisLatGeoBase+'.translateZ', -0.5)
    
    irisDetachRider=cmds.createNode('transform')
    irisDeformGrp=cmds.createNode('transform')
    irisRadius=cmds.createNode('transform')
            
    cmds.parent(irisDeformGrp, irisDetachRider, relative=True)
    cmds.parent(irisRadius, irisDetachRider, relative=True)
    cmds.parent(irisLatGeo, irisDeformGrp, relative=True)
    cmds.parent(irisLatGeoBase, irisDeformGrp, relative=True)
    cmds.parent(irisDetachRider, gEyeballCtrler, relative=True)

    cmds.hide(irisDetachRider)
    
#pupil-----------------------------------------------------------------------------------------
    #detach from iris geometry       
    pieceNames = cmds.detachSurface(irisGeo, ch=1, rpo=1, parameter=(0.1,20))
    pupilGeo=pieceNames[0]
    pupilDetach=pieceNames[2]
    cmds.parent(pupilGeo, gEyeballCtrler, relative=True)
    
    
#connect attributes-----------------------------------------------------------------------------------------
    
    expressionStr='''
                    //calculate cornea-related parameters
                    //cornea translate Z
                    float $cornea_tz = (cos(deg_to_rad('''+gEyeballCtrler+'''.irisSize*9.0))) * 0.5;
                    //cornea radius
                    float $cornea_rad  = (sin(deg_to_rad('''+gEyeballCtrler+'''.irisSize*9.0))) * 0.5;
                    //define nurbs surface cornea detach position
                    float $cornea_par  = ((1.0 - linstep( 0.0,10.0,'''+gEyeballCtrler+'''.irisSize)) * 10.0 ) + 10.0;
                    '''+corneaDetach+'''.parameter[0] = $cornea_par;
                    '''+corneaDetachRider+'''.translateZ = $cornea_tz;
                    '''+corneaRadius+'''.translateX = $cornea_rad;
                    '''+corneaDeformGrp+'''.translateZ = ( 0.5 - $cornea_tz ) * 0.5;
                    '''+corneaDeformGrp+'''.scaleX = '''+corneaDeformGrp+'''.scaleY = $cornea_rad * 2.0;
                    '''+corneaDeformGrp+'''.scaleZ = ( 0.5 - $cornea_tz );
                    '''+corneaLat+'''.envelope = (1.0 - (smoothstep(0.0,11.0,'''+gEyeballCtrler+'''.irisSize))) * ('''+gEyeballCtrler+'''.corneaBulge * 0.1);
                    
                    //calculate iris-related parameters
                    float $iris_tz   = ( cos(deg_to_rad(('''+gEyeballCtrler+'''.irisSize+0.3)*9.0)) ) * 0.485;
                    float $iris_rad  = ( sin(deg_to_rad(('''+gEyeballCtrler+'''.irisSize+0.3)*9.0)) ) * 0.485;
                    float $iris_par  = ((1.0 - (('''+gEyeballCtrler+'''.irisSize+0.3)*0.1)) * 10.0 ) + 10.0;
                    '''+irisDetach+'''.parameter[0] = $iris_par;
                    '''+irisDetachRider+'''.translateZ = $iris_tz;
                    '''+irisRadius+'''.translateX = $iris_rad;
                    '''+irisDeformGrp+'''.translateZ = ( 0.5 - $iris_tz ) * 0.5;
                    '''+irisDeformGrp+'''.scaleX = '''+irisDeformGrp+'''.scaleY = $iris_rad * 2.0;
                    '''+irisDeformGrp+'''.scaleZ = ( 0.5 - $iris_tz );
                    '''+irisLat+'''.envelope = '''+gEyeballCtrler+'''.irisConcave * 0.1;
                    
                    float $pupil_par = max( (((1.0 - (('''+gEyeballCtrler+'''.pupilSize)*0.1)) * 10.0 ) + 10.0), $iris_par + 0.1 );
                    '''+pupilDetach+'''.parameter[0] = $pupil_par;
                    '''
    
    cmds.expression(s=expressionStr)

    #deform latticeGeo
    for x in range(0,2):
        for y in range(0,2):
            for z in range(3,6):
                pointNameStr=corneaLatGeo+'.pt['+str(x)+']['+str(y)+']['+str(z)+']'
                cmds.select(pointNameStr)
                cmds.move(0, 0, 0.05, r=True)
 
#rename objects------------------------------------

    cnt=1
    gEyeballCtrlerName='eyeballCtrl'+str(cnt)
    while cmds.namespace(exists=gEyeballCtrlerName):
        cnt=cnt+1
        gEyeballCtrlerName='eyeballCtrl'+str(cnt)
    
    cmds.rename(gEyeballCtrler, gEyeballCtrlerName)
    cmds.rename(pupilGeo, 'pupilGeo')
    cmds.rename(pupilDetach, 'pupilDetach')
    
    cmds.rename(irisLat, 'irisLat')
    cmds.rename(irisLatGeo, 'irisLatGeo')
    cmds.rename(irisLatGeoBase, 'irisLatGeoBase')
    cmds.rename(irisGeo,'irisGeo')
    cmds.rename(irisDetach,'irisDetach')
    cmds.rename(irisDetachRider,'irisDetachRider')
    cmds.rename(irisDeformGrp,'irisDeformGrp')
    cmds.rename(irisRadius,'irisRadius')
    cmds.rename(corneaLat, 'corneaLat')
    cmds.rename(corneaLatGeo, 'corneaLatGeo')
    cmds.rename(corneaLatGeoBase, 'corneaLatGeoBase')
    cmds.rename(eyeballSphere,'eyeballSphere')
    cmds.rename(corneaGeo,'corneaGeo')
    cmds.rename(corneaDetach,'corneaDetach')
    cmds.rename(corneaDetachRider,'corneaDetachRider')
    cmds.rename(corneaDeformGrp,'corneaDeformGrp')
    cmds.rename(corneaRadius,'corneaRadius')
