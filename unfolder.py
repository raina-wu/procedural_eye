# Copyright (C) 
# 
# File: unfoldCmd.py
#
# Author: Autodesk Developer Network

import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

# Command name
kPluginCmdName = "doUnfold"







# unfold command
class unfold(OpenMayaMPx.MPxCommand):
    
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.previousSelectionList = OpenMaya.MSelectionList()
        self.foldFlagList = []
        
    #get face edge id list
    def getFaceInfo(self, mesh, faceId, faceVertices, faceEdges, connectedFaces):
                
        faceIter = OpenMaya.MItMeshPolygon(mesh)
        meshFn = OpenMaya.MFnMesh(mesh)
        
        if faceId >= meshFn.numPolygons() or faceId < 0:
            pass
        else:
            while not faceIter.isDone():
                if faceIter.index() == faceId:
                    faceIter.getEdges(faceEdges)
                    faceIter.getConnectedFaces(connectedFaces)
                    faceIter.getVertices(faceVertices)
                    break
                faceIter.next()
    

    #- This method performs the action of the command. It iterates over all
    #- selected items and prints out connected plug and dependency node type
    #- information.
    def doIt(self, args):
        OpenMaya.MGlobal.getActiveSelectionList(self.previousSelectionList)
 
        meshDagPath = OpenMaya.MDagPath()
        mesh = OpenMaya.MObject()
        
        objIter = OpenMaya.MItSelectionList(self.previousSelectionList)
        while (objIter.isDone() == 0):
            objIter.getDagPath(meshDagPath)
            objIter.getDependNode(mesh)
            meshName = meshDagPath.fullPathName()
            
            foldedFaceIdList  = OpenMaya.MIntArray()
            
            
            currentLayerIdList = OpenMaya.MIntArray()
            currentLayerIdList.append(0)
            
            nextLayerIdList = OpenMaya.MIntArray()
            
            while currentLayerIdList.length() > 0:
                for i in range(0, currentLayerIdList.length()):
                    faceVertices = OpenMaya.MIntArray()
                    faceEdges = OpenMaya.MIntArray()
                    connectedFaces = OpenMaya.MIntArray()
                    self.getFaceInfo(mesh, i, faceVertices, faceEdges, connectedFaces)
                    
                    for j in range(0, connectedFaces.length()): 
                        if connectedFaces[i] not in foldedFaceIdList:
                            nextLayerIdList.append(connectedFaces[i])
                            #do unfolding
                            foldedFaceIdList.append(connectedFaces[i])
                    
                currentLayerIdList = nextLayerIdList
                nextLayerIdList.clear()
            

                    
        
#         OpenMaya.MGlobal.getActiveSelectionList(self.previousSelectionList)
#         
#         finalFacesSelection = OpenMaya.MSelectionList()
#         meshDagPath = OpenMaya.MDagPath()
#         multiEdgeComponent = OpenMaya.MObject()
#         singleEdgeComponent = OpenMaya.MObject()
#         
#         
#         edgeComponentIter = OpenMaya.MItSelectionList(self.previousSelectionList, OpenMaya.MFn.kMeshEdgeComponent)
#         while (edgeComponentIter.isDone() == 0):
#             edgeComponentIter.getDagPath(meshDagPath, multiEdgeComponent)
#             meshName = meshDagPath.fullPathName()
#             
#             if not multiEdgeComponent.isNull():
#                 edgeIter = OpenMaya.MItMeshEdge(meshDagPath, multiEdgeComponent)
#                 while (edgeIter.isDone()==0):
#                     connectedFacesIndices = OpenMaya.MIntArray
#                     edgeIter.getConnectedFaces(connectedFacesIndices)
#                     
#                     faceIter = OpenMaya.MItMeshPolygon(meshDagPath)
#                     for i in range(0, connectedFacesIndices.length()):
#                         faceEdgesIndices = OpenMaya.MIntArray()
#                         faceIter.setIndex(connectedFacesIndices[i], dummyIndex)
#                     
        
#         #- Select all objects currently selected into the Maya editor.
#         slist = OpenMaya.MSelectionList()
#         OpenMaya.MGlobal.getActiveSelectionList( slist )
#         #- Create an iterator on the selection list (using the iterator pattern).
#         iter = OpenMaya.MItSelectionList( slist, OpenMaya.MFn.kDagNode )
# 
#         #- Iterate over all selected dependency nodes
#         while ( iter.isDone() == 0 ): 
#             #- Not getting the dag path, it will only return one path. I.e.:
#             #dagPath = OpenMaya.MDagPath 
#             #iter.getDagPath(dagPath)
# 
#             #- Instead, get the dependency node first and then apply MFnDagNode function set onto it.
#             depNode = OpenMaya.MObject()
#             iter.getDependNode(depNode)
# 
#             fnDag = OpenMaya.MFnDagNode(depNode)
#             print "********************************************************"
#             sys.stdout.write( '\n' )
#             print "The selected node name is %s, node type : %s" % (fnDag.name(), depNode.apiTypeStr())
#             sys.stdout.write( '\n' )
# 
#             #- Retrieve number of instances on this dag node
#             num = fnDag.instanceCount(1)
#             if( num != 1 ):
#                 print "Number of instances on this node is : %d" % num
#                 sys.stdout.write( '\n' )
#             
#             #Save out the MMatrix __str__ function so we can replace it once were done
#             oldMMatrix_str = OpenMaya.MMatrix .__str__        
#             # Call my new printing function to print the matrix so that is it readable
#             OpenMaya.MMatrix.__str__ = myMatrix_str        
#             
#             #- Retrieve all the instanced paths of this dag node and print out them
#             dagPathArray = OpenMaya.MDagPathArray()
#             fnDag.getAllPaths(dagPathArray)
#             for j in range (0, dagPathArray.length()):
#                 instanceDagPath = dagPathArray[j]
#                 print "Dag Path %d for this node: %s" % (j, instanceDagPath.fullPathName())
#                 
#                 sys.stdout.write( '\n' )
#             
#                 #- Get the exclusive matrix of this node
#                 exMatrix = instanceDagPath.exclusiveMatrix()
# 
#                 print "The exclusive transformation matrix of this node is:"
#                 print exMatrix
#                 sys.stdout.write( '\n' )
# 
#                 #- Get the inclusive matrix of this node
#                 #- If it is a shape node, the inclusive and exclusive matrix should be the same
#                 #- If it is a transform node and its transformation matrix is not identity, they 
#                 #- should be different!
#                 inMatrix = instanceDagPath.inclusiveMatrix()
#                 print "The inclusive transformation matrix of this node is:"
#                 print inMatrix
#                 sys.stdout.write( '\n' )
# 
#                 #- If this dag node is a transform node, also get its local transformation matrix
#                 if (depNode.hasFn(OpenMaya.MFn.kTransform)):
#                     fnTrans = OpenMaya.MFnTransform(instanceDagPath)
#                     localMatrix = fnTrans.transformation()
#                     print "The local transformation matrix represented by this transform node is:"
#                     print localMatrix.asMatrix()
#                     sys.stdout.write( '\n' )
#                 
#             iter.next()
#             # Replace MMatrix __str__ function to the default
#             OpenMaya.MMatrix.__str__ = oldMMatrix_str


#New __str__ function for Making the matrix readable....
def myMatrix_str(self):
    return "[[%g,%g,%g,%g][%g,%g,%g,%g][%g,%g,%g,%g][%g,%g,%g,%g]]" % (self(0,0), self(0,1), self(0,2), self(0,3), 
    self(1,0), self(1,1), self(1,2), self(1,3), self(2,0), self(2,1), self(2,2), self(2,3), self(3,0), self(3,1), self(3,2), self(3,3))

# Creator
def cmdCreator():
    return OpenMayaMPx.asMPxPtr( unfold() )

# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerCommand( kPluginCmdName, cmdCreator )
    except:
        sys.stderr.write( "Failed to register command: %s\n" % kPluginCmdName )

# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )

