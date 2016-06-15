import maya.cmds as cm

#------------------------------------------------------------
# This script makes a follicle on the selected vertex. It will
# follow the mesh, and can be used for constraining objects to a mesh.
# How to use: 
# 1. Select the vertex
# 2. run the script! Yes, that is all. 
#-------------------------------------------------------------
def makeFollicle():
    selection = cm.ls(sl=True)
    
    for i in range(0, len(selection)):  
        pos = cm.xform(selection[i], q=True, t=True, ws=True)
        follicleShape = cm.createNode('follicle')
        maya.mel.eval('pickWalk -d up;')
        follicle = cm.listRelatives(follicleShape, p=True)
        follicle = follicle[0]
        cm.move(pos[0], pos[1], pos[2], follicleShape, ws=True)
        
        mesh = selection[0].split('.vtx')[0]
        
        cm.connectAttr(mesh+'.outMesh', follicleShape+'.inputMesh', f=True)
        cm.connectAttr(mesh+'.worldMatrix', follicleShape+'.inputWorldMatrix', f=True)
        cm.connectAttr(follicleShape+'.outRotate', follicle+'.rotate', f=True)
        cm.connectAttr(follicleShape+'.outTranslate', follicle+'.translate', f=True)
    
        VtxToUV = cm.polyListComponentConversion(selection[i], fv=True, tuv=True)
        cm.select(VtxToUV)
        UV = cm.polyEditUV( query=True,)
        print UV, mesh
    
        cm.setAttr(follicleShape+'.parameterU', UV[0])
        cm.setAttr(follicleShape+'.parameterV', UV[1])
makeFollicle()    












