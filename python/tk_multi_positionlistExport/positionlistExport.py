import sgtk
import maya.cmds as cmds

# load the framework:
wtd_fw = sgtk.platform.import_framework("tk-framework-wtd", "pipeline")
# wtd_fw = self.load_framework("tk-framework-wtd_v0.x.x")
# ppl = wtd_fw.import_module("pipeline")
	
def superPrint(stringInput):
	stringTemp = "%s %s %s" %('#'*10,stringInput,'#'*10)
	print stringTemp

def createPositionlist():
	childrenAndParentsDict, typeDict = getAllParentsAndTypeDict()
	cmds.select(getMainSceneObjects())
	cmds.select(cmds.listRelatives(cmds.ls(type = "locator", allPaths= True) ,parent = True, type = "transform", path = True))
	tempData, tempPath = retrieveDataFromSelection(allParents = childrenAndParentsDict, allTypes = typeDict)
	return tempPath

def getAllParentsAndTypeDict(objectList = None):
	childrenAndParentsDict = {}
	if objectList == None:
		objectList = cmds.listRelatives(cmds.ls(type = "locator", allPaths= True) ,parent = True, type = "transform", path = True)
	typeDict = {}
	parentsDict = {}
	for obj in objectList:
		if obj not in typeDict:
			typeDict[str(obj)] = "Prop"
		tempParent = cmds.listRelatives(obj, parent = True, path = True)
		if tempParent != None:
			typeDict[str(tempParent[0])] = "Set"
			parentsDict[str(obj)] = str(tempParent[0])
		
	for obj in objectList:
		parentList = []
		newChild = obj
		while str(newChild) in parentsDict:
			parent = parentsDict[str(newChild)]
			parentList.append(parent)
			newChild = parent
		childrenAndParentsDict[str(obj)] = parentList
	return childrenAndParentsDict, typeDict
	
def getMainSceneObjects():
	sceneObjects = cmds.listRelatives(cmds.ls(type = "locator", allPaths= True) ,allParents = True, type = "transform", path = True)
	
	mainObjectsList = []
	for obj in sceneObjects:
		if cmds.listRelatives(obj, allParents = True, type = "transform", path = True) == None:
			mainObjectsList.append(obj)
	print mainObjectsList
	return mainObjectsList

def retrieveDataFromSelection(allTypes = None, allParents = None):
	transformDataDict = {}
	selected = cmds.ls(sl = True, allPaths= True)
	print allParents
	print allTypes
	for obj in selected:
		print obj
		print str(obj)
		assetType = None
		parents = []
		if allTypes != None:
			if str(obj) in allTypes:
				assetType = allTypes[str(obj)]
		if allParents != None:
			if str(obj) in allParents:
				print "FOUND in ALLPARENTS"
				parents = allParents[str(obj)]
		tempName, tempOutput = getObjectData(obj, parents = parents, assetType = assetType)
		transformDataDict[tempName] = tempOutput
		
	targetPath = "%spositionlist.txt" %(getDataFolder())
	jsonData = wtd_fw.createJsonPositionList(transformDataDict, targetPath)
	return jsonData, targetPath
	
def getDataFolder():
	targetPath = getFileName()
	print targetPath
	splitPath = targetPath.split("/")
	print splitPath
	name = getAssetName()
	target = "%s/%s/%s/%s/%s/data/" %(splitPath[0],splitPath[1],splitPath[2],splitPath[3],name)
	return target
		
def getFileName():
	return cmds.file(q=True,sceneName=True)
		
def getAssetName():
	quickName = getFileName()
	tempSplit = quickName.split("/")
	if len(tempSplit) > 4:
		return tempSplit[4]
	else:
		return None
		
def getSceneName():
	quickName = getFileName()
	tempSplit = quickName.split("/")
	if len(tempSplit) > 4:
		return tempSplit[4]
	else:
		return None
		
def getParentsOfObject(object):
	return cmds.listRelatives(object, parent = True, path = True)
		
def checkForChildren(object):
	tempChildren = cmds.listRelatives(object, allDescendents = True, type = "locator", path = True)
	if tempChildren != None:
		return False
	return tempChildren
		
def getObjectData(object, parents = [], assetType = None):
	longName = str(object)
	asset = wtd_fw.positionlist.getAssetNameFromObject(longName)	
	name = longName[ longName.find(asset) : ]
	if assetType == None:
		assetType = "prop"
	mainParent = getSceneName()
	parents.append(mainParent)
	animated = ""
	position = cmds.xform(object, ws=True, q=True, t=True)
	rotation = cmds.xform(object, ws=True, q=True, ro=True)
	scale = cmds.xform(object, r=True, q=True, s=True)
	# posModule = wtd_framework.import_module("Positionlist")
	return name, wtd_fw.positionlist.setAssetDict(name, longName, asset, assetType, animated, position, rotation, scale, parents)
		