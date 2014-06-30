import sys
import math
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx


gDefaultPupilValue = 0.7
gDefaultIrisValue = 2.75
gDefaultCorneaBulgeValue = 10
gDefaultIrisConcaveValue = 5

gPupilValue = gDefaultPupilValue
gIrisValue = gDefaultIrisValue
gCorneaBulgeValue = gDefaultCorneaBulgeValue
gIrisConcaveValue = gDefaultIrisConcaveValue


gEyeballCtrler=''

def run():

    UI()

def buildScleraShadingNetwork():
#     try:
        #add mia_material_shader
        sclera_shd=cmds.shadingNode('mia_material_x', asShader=True)
        shadingGrp=cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=sclera_shd+'SG')
        cmds.connectAttr(sclera_shd+'.message', shadingGrp+'.miMaterialShader')
        cmds.connectAttr(sclera_shd+'.message', shadingGrp+'.miPhotonShader')
        cmds.connectAttr(sclera_shd+'.message', shadingGrp+'.miShadowShader')
        
        #add utility shaders
        sclera_col_gamma=cmds.shadingNode('gammaCorrect', asUtility=True)
        sclera_noise_rev=cmds.shadingNode('reverse', asUtility=True)
        sclera_vein_noise_rev=cmds.shadingNode('reverse', asUtility=True)
        sclera_vein_noise_bump_md=cmds.shadingNode('multiplyDivide', asUtility=True)
        sclera_bump=cmds.shadingNode('bump2d', asUtility=True)
        
        #add texture shaders
        sclera_bright_col_ramp=cmds.shadingNode('ramp', asTexture=True)
        placeTex=cmds.shadingNode('place2dTexture', asUtility=True)
        cmds.connectAttr(placeTex+'.outUV', sclera_bright_col_ramp+'.uv')
        cmds.connectAttr(placeTex+'.outUvFilterSize',sclera_bright_col_ramp+'.uvFilterSize')
        
        sclera_vein_col_ramp=cmds.shadingNode('ramp', asTexture=True)
        placeTex=cmds.shadingNode('place2dTexture', asUtility=True)
        cmds.connectAttr(placeTex+'.outUV', sclera_vein_col_ramp+'.uv')
        cmds.connectAttr(placeTex+'.outUvFilterSize',sclera_vein_col_ramp+'.uvFilterSize')
        
        sclera_combo_col_ramp=cmds.shadingNode('ramp', asTexture=True)
        placeTex=cmds.shadingNode('place2dTexture', asUtility=True)
        cmds.connectAttr(placeTex+'.outUV', sclera_combo_col_ramp+'.uv')
        cmds.connectAttr(placeTex+'.outUvFilterSize',sclera_combo_col_ramp+'.uvFilterSize')
        
        sclera_vein_noise_threshold=cmds.shadingNode('ramp', asTexture=True)
        placeTex=cmds.shadingNode('place2dTexture', asUtility=True)
        cmds.connectAttr(placeTex+'.outUV', sclera_vein_noise_threshold+'.uv')
        cmds.connectAttr(placeTex+'.outUvFilterSize',sclera_vein_noise_threshold+'.uvFilterSize')
        
        sclera_bump_ramp=cmds.shadingNode('ramp', asTexture=True)
        placeTex=cmds.shadingNode('place2dTexture', asUtility=True)
        cmds.connectAttr(placeTex+'.outUV', sclera_bump_ramp+'.uv')
        cmds.connectAttr(placeTex+'.outUvFilterSize',sclera_bump_ramp+'.uvFilterSize')
        
        sclera_noise=cmds.shadingNode('fractal', asTexture=True)
        placeFractalTex=cmds.shadingNode('place2dTexture', asUtility=True)
        cmds.connectAttr(placeFractalTex+'.outUV', sclera_noise+'.uv')
        cmds.connectAttr(placeFractalTex+'.outUvFilterSize', sclera_noise+'.uvFilterSize')
        
        sclera_vein_noise=cmds.shadingNode('fractal', asTexture=True)
        placeFractalTex=cmds.shadingNode('place2dTexture', asUtility=True)
        cmds.connectAttr(placeFractalTex+'.outUV', sclera_vein_noise+'.uv')
        cmds.connectAttr(placeFractalTex+'.outUvFilterSize', sclera_vein_noise+'.uvFilterSize')
        
        #connect nodes
        cmds.connectAttr(sclera_noise+'.outColor', sclera_noise_rev+'.input')
        cmds.connectAttr(sclera_noise_rev+'.output', sclera_bright_col_ramp+'.colorGain')
        cmds.connectAttr(sclera_noise+'.outColor', sclera_bright_col_ramp+'.colorOffset')
        cmds.connectAttr(sclera_bright_col_ramp+'.outColor', sclera_combo_col_ramp+'.colorEntryList[1].color')
        
        cmds.connectAttr(sclera_vein_col_ramp+'.outColor', sclera_combo_col_ramp+'.colorOffset')
        cmds.connectAttr(sclera_combo_col_ramp+'.outColor', sclera_col_gamma+'.value')
        cmds.connectAttr(sclera_col_gamma+'.outValue', sclera_shd+'.diffuse')
        cmds.connectAttr(sclera_vein_noise+'.outColor', sclera_combo_col_ramp+'.colorGain')
        
        cmds.connectAttr(sclera_bump+'.outNormal', sclera_shd+'.overall_bump')
        cmds.connectAttr(sclera_bump_ramp+'.outColorR', sclera_bump+'.bumpValue')
        cmds.connectAttr(sclera_noise+'.outColor', sclera_bump_ramp+'.colorGain')
        cmds.connectAttr(sclera_vein_noise_bump_md+'.output', sclera_bump_ramp+'.colorOffset')
        cmds.connectAttr(sclera_vein_noise_rev+'.output', sclera_vein_noise_bump_md+'.input1')
        cmds.connectAttr(sclera_vein_noise_rev+'.output', sclera_vein_col_ramp+'.colorGain')
        cmds.connectAttr(sclera_vein_noise+'.outColor', sclera_vein_noise_rev+'.input')
        cmds.connectAttr(sclera_vein_noise_threshold+'.outColorR', sclera_vein_noise+'.threshold')
        
        #set node attributes
        cmds.setAttr(sclera_shd+'.diffuse_roughness', 0.3)
        cmds.setAttr(sclera_shd+'.reflectivity', 0.5)
        
        cmds.setAttr(sclera_col_gamma+'.gamma', 0.455, 0.455, 0.455)
        cmds.setAttr(sclera_combo_col_ramp+'.type', 1)
        cmds.setAttr(sclera_combo_col_ramp+'.interpolation', 4)
        cmds.setAttr(sclera_combo_col_ramp+'.colorEntryList[0].color', 0.461, 0.075, 0.075)
        cmds.setAttr(sclera_combo_col_ramp+'.colorEntryList[0].position', 0.5)
        cmds.setAttr(sclera_combo_col_ramp+'.colorEntryList[1].position', 1)
    
        cmds.setAttr(sclera_bright_col_ramp+'.colorEntryList[0].color', 0.875, 0.922, 0.950)
        cmds.setAttr(sclera_bright_col_ramp+'.colorEntryList[0].position', 0)
        
        cmds.setAttr(sclera_vein_col_ramp+'.type', 1)
        cmds.setAttr(sclera_vein_col_ramp+'.interpolation', 4)
        cmds.setAttr(sclera_vein_col_ramp+'.colorEntryList[0].color', 0.680, 0.462, 0.481)
        cmds.setAttr(sclera_vein_col_ramp+'.colorEntryList[0].position', 1)
        cmds.setAttr(sclera_vein_col_ramp+'.colorEntryList[1].color', 0.504, 0.063, 0.063)
        cmds.setAttr(sclera_vein_col_ramp+'.colorEntryList[1].position', 0.405)
        
        cmds.setAttr(sclera_bump_ramp+'.type', 1)
        cmds.setAttr(sclera_bump_ramp+'.interpolation', 4)
        cmds.setAttr(sclera_bump_ramp+'.colorEntryList[0].color', 0, 0, 0)
        cmds.setAttr(sclera_bump_ramp+'.colorEntryList[0].position', 1)
        cmds.setAttr(sclera_bump_ramp+'.colorEntryList[1].color', 0.3, 0.3, 0.3)
        cmds.setAttr(sclera_bump_ramp+'.colorEntryList[1].position', 0.95)
        cmds.setAttr(sclera_bump_ramp+'.colorEntryList[2].color', 0.3, 0.3, 0.3)
        cmds.setAttr(sclera_bump_ramp+'.colorEntryList[2].position', 0)
        
        cmds.setAttr(sclera_vein_noise_threshold+'.type', 1)
        cmds.setAttr(sclera_vein_noise_threshold+'.interpolation', 2)
        cmds.setAttr(sclera_vein_noise_threshold+'.colorEntryList[0].color', 1, 1, 1)
        cmds.setAttr(sclera_vein_noise_threshold+'.colorEntryList[0].position', 1)
        cmds.setAttr(sclera_vein_noise_threshold+'.colorEntryList[1].color', 0, 0, 0)
        cmds.setAttr(sclera_vein_noise_threshold+'.colorEntryList[1].position', 0.57)
        cmds.setAttr(sclera_vein_noise_threshold+'.colorEntryList[2].color', 0, 0, 0)
        cmds.setAttr(sclera_vein_noise_threshold+'.colorEntryList[2].position', 0.125)
        cmds.setAttr(sclera_vein_noise_threshold+'.colorEntryList[3].color', 1, 1, 1)
        cmds.setAttr(sclera_vein_noise_threshold+'.colorEntryList[3].position', 0.045)
        cmds.setAttr(sclera_vein_noise_threshold+'.noise', 0.114)
        cmds.setAttr(placeFractalTex+'.repeatUV', 0.5, 2)
        
        cmds.setAttr(sclera_noise+'.ratio', 0.5)
        cmds.setAttr(sclera_noise+'.levelMax', 5)
        
        cmds.setAttr(sclera_vein_noise+'.frequencyRatio', 3)
        cmds.setAttr(sclera_vein_noise+'.bias', 0.6)
        cmds.setAttr(sclera_vein_noise+'.inflection', True)
        
        cmds.setAttr(sclera_bump+'.bumpDepth', 0.15)
        cmds.setAttr(sclera_bump+'.adjustEdges', True)
        cmds.setAttr(sclera_vein_noise_bump_md+'.operation', 1)
        cmds.setAttr(sclera_vein_noise_bump_md+'.input2', 0.1, 0.1, 0.1)
        
        #rename nodes
        cmds.rename(sclera_shd, 'sclera_shd')
        cmds.rename(shadingGrp, 'sclera_shdSG')
        cmds.rename(sclera_col_gamma, 'sclera_col_gamma')
        cmds.rename(sclera_noise_rev, 'sclera_noise_rev')
        cmds.rename(sclera_vein_noise_rev, 'sclera_vein_noise_rev')
        cmds.rename(sclera_vein_noise_bump_md, 'sclera_vein_noise_bump_md')
        cmds.rename(sclera_bump, 'sclera_bump')
        cmds.rename(sclera_bright_col_ramp, 'sclera_bright_col_ramp')
        cmds.rename(sclera_vein_col_ramp, 'sclera_vein_col_ramp')
        cmds.rename(sclera_combo_col_ramp, 'sclera_combo_col_ramp')
        cmds.rename(sclera_vein_noise_threshold, 'sclera_vein_noise_threshold')
        cmds.rename(sclera_bump_ramp, 'sclera_bump_ramp')
        cmds.rename(sclera_noise, 'sclera_noise')
        cmds.rename(sclera_vein_noise, 'sclera_vein_noise')
#     except:
#         cmds.namespace(set=':')
#         print 'what?'

def buildCorneaShadingNetwork():
#     try:
        #add mia_material_shader
        cornea_shd=cmds.shadingNode('mia_material_x', asShader=True)
        shadingGrp=cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=cornea_shd+'SG')
        cmds.connectAttr(cornea_shd+'.message', shadingGrp+'.miMaterialShader')
        cmds.connectAttr(cornea_shd+'.message', shadingGrp+'.miPhotonShader')
        cmds.connectAttr(cornea_shd+'.message', shadingGrp+'.miShadowShader')
        
        #add utility shaders
        cornea_col_gamma=cmds.shadingNode('gammaCorrect', asUtility=True)
        cornea_noise_rev=cmds.shadingNode('reverse', asUtility=True)
        
        #add texture shaders
        cornea_trans_ramp=cmds.shadingNode('ramp', asTexture=True)
        placeTex=cmds.shadingNode('place2dTexture', asUtility=True)
        cmds.connectAttr(placeTex+'.outUV', cornea_trans_ramp+'.uv')
        cmds.connectAttr(placeTex+'.outUvFilterSize', cornea_trans_ramp+'.uvFilterSize')
        
        cornea_col_ramp=cmds.shadingNode('ramp', asTexture=True)
        placeTex=cmds.shadingNode('place2dTexture', asUtility=True)
        cmds.connectAttr(placeTex+'.outUV', cornea_col_ramp+'.uv')
        cmds.connectAttr(placeTex+'.outUvFilterSize', cornea_col_ramp+'.uvFilterSize')
        
        cornea_noise=cmds.shadingNode('fractal', asTexture=True)
        placeFractalTex=cmds.shadingNode('place2dTexture', asUtility=True)
        cmds.connectAttr(placeFractalTex+'.outUV', cornea_noise+'.uv')
        cmds.connectAttr(placeFractalTex+'.outUvFilterSize', cornea_noise+'.uvFilterSize')
        
        #connect nodes
        cmds.connectAttr(cornea_col_gamma+'.outValue', cornea_shd+'.diffuse')
        cmds.connectAttr(cornea_trans_ramp+'.outColorR', cornea_shd+'.transparency')
        cmds.connectAttr(cornea_col_ramp+'.outColor', cornea_col_gamma+'.value')
        cmds.connectAttr(cornea_noise+'.outColor', cornea_col_ramp+'.colorOffset')
        cmds.connectAttr(cornea_noise+'.outColor', cornea_noise_rev+'.input')
        cmds.connectAttr(cornea_noise_rev+'.output', cornea_col_ramp+'.colorGain')
    
        #set node attributes
        cmds.setAttr(cornea_shd+'.diffuse_roughness', 0.3)
        cmds.setAttr(cornea_shd+'.reflectivity', 0.5)
        cmds.setAttr(cornea_shd+'.refr_ior', 1.3)
        
        cmds.setAttr(cornea_col_gamma+'.gamma', 0.455, 0.455, 0.455)
        cmds.setAttr(cornea_trans_ramp+'.type', 1)
        cmds.setAttr(cornea_trans_ramp+'.interpolation', 4)
        cmds.setAttr(cornea_trans_ramp+'.colorEntryList[0].color', 1, 1, 1)
        cmds.setAttr(cornea_trans_ramp+'.colorEntryList[0].position', 1)
        cmds.setAttr(cornea_trans_ramp+'.colorEntryList[1].color', 1, 1, 1)
        cmds.setAttr(cornea_trans_ramp+'.colorEntryList[1].position', 0.2)
        cmds.setAttr(cornea_trans_ramp+'.colorEntryList[2].color', 0, 0, 0)
        cmds.setAttr(cornea_trans_ramp+'.colorEntryList[2].position', 0)
    
        cmds.setAttr(cornea_col_ramp+'.colorEntryList[0].color', 0.875, 0.922, 0.950)
        cmds.setAttr(cornea_col_ramp+'.colorEntryList[0].position', 0)
     
        cmds.setAttr(cornea_noise+'.ratio', 0.5)
        cmds.setAttr(cornea_noise+'.levelMax', 5)
        cmds.setAttr(placeFractalTex+'.coverage', 4, 1)
        cmds.setAttr(placeFractalTex+'.translateFrame', 4, 0)
        
        #rename nodes
        cmds.rename(cornea_col_ramp, 'cornea_col_ramp')
        cmds.rename(cornea_trans_ramp, 'cornea_trans_ramp')
        cmds.rename(cornea_noise, 'cornea_noise')
        cmds.rename(cornea_col_gamma, 'cornea_col_gamma')
        cmds.rename(cornea_shd, 'cornea_shd')
        cmds.rename(shadingGrp,'cornea_shdSG')
#     except:
#         cmds.namespace(set=':')

def buildIrisShadingNetwork():
#     try:
        #add mia_material_shader
        iris_shd=cmds.shadingNode('mia_material_x', asShader=True)
        shadingGrp=cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=iris_shd+'SG')
        cmds.connectAttr(iris_shd+'.message', shadingGrp+'.miMaterialShader')
        cmds.connectAttr(iris_shd+'.message', shadingGrp+'.miPhotonShader')
        cmds.connectAttr(iris_shd+'.message', shadingGrp+'.miShadowShader')
        
        #add utility shaders
        iris_col_gamma=cmds.shadingNode('gammaCorrect', asUtility=True)
        iris_col_pma=cmds.shadingNode('plusMinusAverage', asUtility=True)
        
        #add texture shaders
        iris_base_col_ramp=cmds.shadingNode('ramp', asTexture=True)
        placeTex=cmds.shadingNode('place2dTexture', asUtility=True)
        cmds.connectAttr(placeTex+'.outUV', iris_base_col_ramp+'.uv')
        cmds.connectAttr(placeTex+'.outUvFilterSize', iris_base_col_ramp+'.uvFilterSize')
        
        iris_col_ramp=cmds.shadingNode('ramp', asTexture=True)
        placeTex=cmds.shadingNode('place2dTexture', asUtility=True)
        cmds.connectAttr(placeTex+'.outUV', iris_col_ramp+'.uv')
        cmds.connectAttr(placeTex+'.outUvFilterSize', iris_col_ramp+'.uvFilterSize')
        
        fractal=cmds.shadingNode('fractal', asTexture=True)
        placeFractalTex=cmds.shadingNode('place2dTexture', asUtility=True)
        cmds.connectAttr(placeFractalTex+'.outUV', fractal+'.uv')
        cmds.connectAttr(placeFractalTex+'.outUvFilterSize', fractal+'.uvFilterSize')
        
        #connect nodes
        cmds.connectAttr(iris_col_gamma+'.outValue', iris_shd+'.diffuse')
        cmds.connectAttr(iris_col_pma+'.output3D', iris_col_gamma+'.value')
        cmds.connectAttr(iris_col_ramp+'.outColor', iris_col_pma+'.input3D[0]')
        cmds.connectAttr(iris_base_col_ramp+'.outColor', iris_col_pma+'.input3D[1]')
        cmds.connectAttr(fractal+'.outColor', iris_col_ramp+'.colorGain')
        
    
        #set node attributes
        cmds.setAttr(iris_shd+'.reflectivity', 0)
        
        cmds.setAttr(iris_col_gamma+'.gamma', 0.4, 0.4, 0.4)
        cmds.setAttr(iris_base_col_ramp+'.type', 1)
        cmds.setAttr(iris_base_col_ramp+'.interpolation', 4)
        cmds.setAttr(iris_base_col_ramp+'.colorEntryList[0].color', 0, 0, 0)
        cmds.setAttr(iris_base_col_ramp+'.colorEntryList[0].position', 1)
        cmds.setAttr(iris_base_col_ramp+'.colorEntryList[1].color', 0.164, 0.240, 0.287)
        cmds.setAttr(iris_base_col_ramp+'.colorEntryList[1].position', 0.84)
        cmds.setAttr(iris_base_col_ramp+'.colorEntryList[2].color', 0.227, 0.312, 0.391)
        cmds.setAttr(iris_base_col_ramp+'.colorEntryList[2].position', 0.515)
        cmds.setAttr(iris_base_col_ramp+'.colorEntryList[3].color', 0.088, 0.099, 0.132)
        cmds.setAttr(iris_base_col_ramp+'.colorEntryList[3].position', 0)
    
        cmds.setAttr(iris_col_ramp+'.type', 1)
        cmds.setAttr(iris_col_ramp+'.interpolation', 4)
        cmds.setAttr(iris_col_ramp+'.colorEntryList[0].color', 0, 0, 0)
        cmds.setAttr(iris_col_ramp+'.colorEntryList[0].position', 1)
        cmds.setAttr(iris_col_ramp+'.colorEntryList[1].color', 0.386, 0.529, 0.474)
        cmds.setAttr(iris_col_ramp+'.colorEntryList[1].position', 0.825)
        cmds.setAttr(iris_col_ramp+'.colorEntryList[2].color', 0.448, 0.555, 0.609)
        cmds.setAttr(iris_col_ramp+'.colorEntryList[2].position', 0.495)
        cmds.setAttr(iris_col_ramp+'.colorEntryList[3].color', 0.102, 0.107, 0.103)
        cmds.setAttr(iris_col_ramp+'.colorEntryList[3].position', 0.005)
        
        cmds.setAttr(fractal+'.amplitude', 0.85)
        cmds.setAttr(fractal+'.threshold', 0.15)
        cmds.setAttr(fractal+'.ratio', 0.5)
        cmds.setAttr(fractal+'.levelMin', 3)
        cmds.setAttr(fractal+'.levelMax', 5)
        cmds.setAttr(placeFractalTex+'.repeatUV', 0.15, 2)
        cmds.setAttr(placeFractalTex+'.noiseUV', 0.002, 0.002)
        
        #rename nodes
        cmds.rename(iris_col_ramp, 'iris_col_ramp')
        cmds.rename(iris_base_col_ramp, 'iris_base_col_ramp')
        cmds.rename(fractal, 'fractal')
        cmds.rename(iris_col_gamma, 'iris_col_gamma')
        cmds.rename(iris_col_pma, 'iris_col_pma')
        cmds.rename(iris_shd, 'iris_shd')
        cmds.rename(shadingGrp,'iris_shdSG')
#     except:
#         cmds.namespace(set=':')

def buildPupilShadingNetwork():
#     try:
        #build surface shader
        pupil_shd=cmds.shadingNode('surfaceShader', asShader=True)
        shadingGrp=cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=pupil_shd+'SG')
        cmds.connectAttr(pupil_shd+'.outColor', shadingGrp+'.surfaceShader')
        
        #rename nodes
        cmds.rename(pupil_shd, 'pupil_shd')
        cmds.rename(shadingGrp, 'pupil_shdSG')
#     except:
#         cmds.namespace(set=':')
#     
    
def createNew(*args):
#     try:
        
        cnt=1
        nameSpace='eyeball'+str(cnt)
        while cmds.namespace(exists=nameSpace):
            cnt=cnt+1
            nameSpace='eyeball'+str(cnt)
            
        cmds.namespace(add=nameSpace)
        cmds.namespace(set=nameSpace)
        buildEyeballGeo()
        
        buildIrisShadingNetwork()
        cmds.select(nameSpace+':irisGeo')
        cmds.hyperShade(assign=nameSpace+':iris_shd')
        
        buildPupilShadingNetwork()
        cmds.select(nameSpace+':pupilGeo')
        cmds.hyperShade(assign=nameSpace+':pupil_shd')
    
        buildScleraShadingNetwork()
        cmds.select(nameSpace+':eyeballSphere')
        cmds.hyperShade(assign=nameSpace+':sclera_shd')   
        
        buildCorneaShadingNetwork()
        cmds.select(nameSpace+':corneaGeo')
        cmds.hyperShade(assign=nameSpace+':cornea_shd')    
        
        cmds.namespace(set=':')
        
#     except:
#         cmds.namespace(set=':')

    
    
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
    cmds.text('objInfo', label='', align='left')
    cmds.separator(h=5, style='none')

    #input editor
    cmds.rowColumnLayout(numberOfColumns=2, cw=[(1,100),(2,180)], columnOffset=[(1,'both',5),(2,'both',5)])
    cmds.text('iris_size', align='left')
    cmds.floatField('irisSizeField', value=gDefaultIrisValue, cc=setIrisSize)
    cmds.text('pupil_size', align='left')
    cmds.floatField('pupilSizeField', value=gDefaultPupilValue, cc=setPupilSize)
    cmds.text('cornea_bulge', align='left')
    cmds.floatField('corneaBulgeField', value=gDefaultCorneaBulgeValue, cc=setCorneaBulge)
    cmds.text('iris_concave', align='left')
    cmds.floatField('irisConcaveField', value=gDefaultIrisConcaveValue, cc=setIrisConcave)
    
    #buttons
    cmds.setParent(mainLayout)   
    cmds.separator(h=15, style='none')
    cmds.rowColumnLayout(numberOfColumns=2, cw=[(1,100),(2,180)], columnOffset=[(1,'both',5),(2,'both',5)])
    cmds.button(label='reset values', c=reset)
    cmds.button(label='create new', c=createNew)
    cmds.button(label='set current', c=setCurrent)
    cmds.separator(h=5, style='none')
        
    cmds.showWindow(window)
    
    
    


def setCurrent(*args):

    selected=cmds.ls(selection=True)
    
    if len(selected)!=1:
        cmds.error('More than one object selected. Please select only one eyeControler.')
    else:
        try:
            nodeName=selected[0]
            pupilValue=cmds.getAttr(nodeName+'.pupilSize')
            irisValue=cmds.getAttr(nodeName+'.irisSize')
            irisConcave=cmds.getAttr(nodeName+'.irisConcave')
            corneaBulge=cmds.getAttr(nodeName+'.corneaBulge')
            
            gPupilValue=pupilValue
            gIrisValue=irisValue
            gIrisConcave=irisConcave
            gCorneaBulge=corneaBulge
            
            global gEyeballCtrler
            gEyeballCtrler=nodeName   
            
            cmds.text('objInfo', edit=True, label='current controler: '+gEyeballCtrler)
            cmds.floatField('pupilSizeField', edit=True, value=pupilValue)
            cmds.floatField('irisSizeField', edit=True, value=irisValue)
            cmds.floatField('irisConcaveField', edit=True, value=irisConcave)
            cmds.floatField('corneaBulgeField', edit=True, value=corneaBulge)
    
        except:
            cmds.error('Eyeball attributes missing. This command requires one eyeControler object to be selected.')
  
def reset(*args):

    if len(gEyeballCtrler)==0:
        cmds.error('Please set current eyeball controler.')
    else:
        setPupilSize(gDefaultPupilValue)
        setIrisSize(gDefaultIrisValue)
        setCorneaBulge(gDefaultCorneaBulgeValue)
        setIrisConcave(gDefaultIrisConcaveValue)
        cmds.floatField('pupilSizeField', edit=True, value=gDefaultPupilValue)
        cmds.floatField('irisSizeField', edit=True, value=gDefaultIrisValue)
        cmds.floatField('irisConcaveField', edit=True, value=gDefaultIrisConcaveValue)
        cmds.floatField('corneaBulgeField', edit=True, value=gDefaultCorneaBulgeValue)
    
def setPupilSize(*args):
    print args
    if len(gEyeballCtrler)==0:
        cmds.error('Please set current eyeball controler.')
    else:
        gPupilValue=args[0]
        cmds.setAttr(gEyeballCtrler+'.pupilSize', gPupilValue)
       
def setIrisSize(*args):
    print args
    if len(gEyeballCtrler)==0:
        cmds.error('Please set current eyeball controler.')
    else:
        gIrisValue=args[0]
        cmds.setAttr(gEyeballCtrler+'.irisSize', gIrisValue)
        
def setIrisConcave(*args):
    print args
    if len(gEyeballCtrler)==0:
        cmds.error('Please set current eyeball controler.')
    else:
        gIrisConcaveValue=args[0]
        cmds.setAttr(gEyeballCtrler+'.irisConcave', gIrisConcaveValue)

def setCorneaBulge(*args):
    print args
    if len(gEyeballCtrler)==0:
        cmds.error('Please set current eyeball controler.')
    else:
        gCorneaBulgeValue=args[0]
        cmds.setAttr(gEyeballCtrler+'.corneaBulge', gCorneaBulgeValue)        

def linstep(start, end, para):
    if para>=end:
        return 1;
    elif para<=start:
        return 0;
    else:
        return (para-start)/(end-start)

def buildEyeballGeo():  
#     try:
    #create eyeball controler-----------------------------------------------------------------------------------------
    
    
        gEyeballCtrler=cmds.spaceLocator()[0]
        cmds.addAttr(longName='pupilSize', attributeType='float', keyable=True, defaultValue=gDefaultPupilValue)
        cmds.addAttr(longName='irisSize', attributeType='float', keyable=True, defaultValue=gDefaultIrisValue)
        cmds.addAttr(longName='irisConcave', attributeType='float', keyable=True, defaultValue=gDefaultIrisConcaveValue)
        cmds.addAttr(longName='corneaBulge', attributeType='float', keyable=True, defaultValue=gDefaultCorneaBulgeValue)
        
        
    #cornea-----------------------------------------------------------------------------------------
    
        #create eyeball base geometry and detach
        eyeballSphere=cmds.sphere(sections=20, spans=20, axis=(0,0,1), radius=0.5)[0]
    #     eyeballSphere=eyeballSphere[0]
        pieceNames = cmds.detachSurface(eyeballSphere, ch=1, rpo=1, parameter=(0.1,20))
        corneaGeo=pieceNames[0];
        corneaDetach=pieceNames[2];
        cmds.parent(eyeballSphere, gEyeballCtrler, relative=True)
        cmds.parent(corneaGeo, gEyeballCtrler, relative=True)
        
        #rebuild corneaGeo
        cmds.rebuildSurface(corneaGeo, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kc=0, su=36, du=3, sv=1, dv=3, tol=0.01, fr=0, dir=0)
    
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
                    ptTranslateZ=cmds.getAttr(pointNameStr+'.zValue')
                    cmds.setAttr(pointNameStr+'.zValue', ptTranslateZ*2+0.319)
#                     cmds.select(pointNameStr)
#                     cmds.move(0, 0, 0.05, r=True)
     
    #rename objects------------------------------------
       
        gEyeballCtrlerName='eyeballCtrler'
        
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
        
#     except:
#         cmds.namespace(set=':')
