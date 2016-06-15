import maya.cmds as cm
import math
import collections

'''
A script used for my final major project for selecting a number of curves and follicles. The curves which are within a certain distance of follicles will be parented to them, creating clumps of hair. 
'''
class hairMap(object):
    def __init__(self):
        
        selection = cm.ls(sl=True) 
                         
        search = 'curve'
        self.curveGrp = [el for el in selection if isinstance(el, collections.Iterable) and (search in el)]
        for a in self.curveGrp:
            if cm.listRelatives(a, p=True):
                self.curveGrp.remove(a)
        search = 'Follicle'
        self.follicleGrp = [el for el in selection if isinstance(el, collections.Iterable) and (search in el)]

        self.FolBBoxGrp = [] 
        self.Dist = 1000

    def shortDistance(self):
        if len(self.follicleGrp)<2:
            print "***ERROR: Select 2 or more follicles."
            return 
        i=-1
        for a in self.follicleGrp:
            i+=1
            x1, y1, z1, x2, y2, z2 = cm.exactWorldBoundingBox(a)
            self.FolBBoxGrp.append((x1, y1, z1))
            for b in reversed(self.follicleGrp):
                x2, y2, z2, x3, y3, z3 = cm.exactWorldBoundingBox(b)
                tempDist = math.sqrt(((x1-x2)**2)+((y1-y2)**2)+((z1-z2)**2))
                
                if tempDist < self.Dist:
                    if b==a:
                        pass
                    else:
                        self.Dist = tempDist   
        self.Dist/=2 
        
        print 'Shortest distance:', self.Dist
        if self.Dist<.5:
            print '***WARNING: Range is <0.5. May create empty groups.'
    
    def refineSearch(self):
        for a in self.curveGrp:
            if cm.listRelatives(a, p=True):
                self.curveGrp.remove(a)
        for a in self.follicleGrp:
                  
            cm.group(n='group_2_'+str(a), em=True, w=True)         
            x1, y1, z1, x2, y2, z2 = cm.exactWorldBoundingBox(a)  
            x1 = (x1+x2)/2
            y1 = (y1+y2)/2
            z1 = (z1+z2)/2           
            x1 = abs(x1)
            y1 = abs(y1)
            z1 = abs(z1)

            for b in self.curveGrp:
                x1c, y1c, z1c, x2c, y2c, z2c = cm.exactWorldBoundingBox(b)
                x1c = abs(x1c)
                y1c = abs(y1c)
                z1c = abs(z1c)
                diffx1=x1c-x1
                diffy1=y1c-y1
                diffz1=z1c-z1
                if diffx1<self.Dist and diffx1>-self.Dist and diffy1<self.Dist and diffy1>-self.Dist and diffz1<self.Dist and diffz1>-self.Dist:
                    if cm.listRelatives(b, p=False):
                        print b, 'has no parent'
                        cm.parent(b, 'group_2_'+str(a))
                    else: 
                        pass
                        
    def search(self):
        for a in self.follicleGrp:   
            cm.group(n='group_'+str(a), em=True, w=True)  
            x1, y1, z1, x2, y2, z2 = cm.exactWorldBoundingBox(a)  
            x1 = (x1+x2)/2
            y1 = (y1+y2)/2
            z1 = (z1+z2)/2
            
            x1 = abs(x1)
            y1 = abs(y1)
            z1 = abs(z1)

            for b in self.curveGrp:
                x1c, y1c, z1c, x2c, y2c, z2c = cm.exactWorldBoundingBox(b)
                x1c = abs(x1c)
                y1c = abs(y1c)
                z1c = abs(z1c)
                diffx1=x1c-x1
                diffy1=y1c-y1
                diffz1=z1c-z1
                if diffx1<self.Dist and diffx1>-self.Dist and diffy1<self.Dist and diffy1>-self.Dist and diffz1<self.Dist and diffz1>-self.Dist:
                    if cm.listRelatives(b, p=False):
                        print b, 'Has no parent'
                        cm.parent(b, 'group_'+str(a))
        more = 0               
        for c in self.curveGrp:
            if cm.listRelatives(c, p=False):
                more = 1
        if more==1:
            self.Dist += (self.Dist*.8)
            print '***Refining search.'
            
            new.refineSearch()
    def parentChecker(self):
        for b in self.curveGrp:
            if cm.listRelatives(b, p=True):
                cm.select(b, add=True)
            else: 
                print '***Error: A curve is not parented.'

    def parentToFollicle(self):
        follicleNo = 0
        for a in self.follicleGrp:
            follicleNo+=1
            cm.parent('group_'+str(a), a)
            cm.select('group_'+str(a), add=True) 
            cm.parent('group_2_'+str(a), a)
            cm.select('group_2_'+str(a), add=True)     
    def assignHairSystem(self):
        follicleNo = 0
        for a in self.follicleGrp:
            follicleNo+=1
            cm.select('group_'+str(a), add=True)    
            cm.select('group_2_'+str(a), add=True) 
        
    def cleanUpGrps(self):
        cm.select('group_*')
        for i in cm.ls(sl=True):
            cm.rename(i, 'done')
        
    def setDist(self, val):
        self.Dist = val 
        
    def deleteEmptyGrps(self):
        transforms =  cmds.ls(type='transform')
        deleteList = []
        for tran in transforms:
            if cmds.nodeType(tran) == 'transform':
                children = cmds.listRelatives(tran, c=True) 
                if children == None:
                    print '%s, has no childred' %(tran)
                    deleteList.append(tran)
            
        cmds.delete(deleteList)
        
new = hairMap()
new.cleanUpGrps()  
new.deleteEmptyGrps()
new.shortDistance()
new.setDist(.75)
new.search()
new.parentToFollicle()


new.parentChecker()
new.assignHairSystem()

cm.select('group_*')
for i in cm.ls(sl=True):
    cm.rename(i, 'done')
