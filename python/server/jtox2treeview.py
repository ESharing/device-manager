import json
import sys
#from copy import deepcopy
import copy

def generateSchemas(inputJtoXTree, modules):
  generatedSchemas = []
  no = 0
  for schemaRootNodeName in inputJtoXTree.keys(): 
    schemaRootNode = {}
    #moduleName = schemaRootNodeName.split(':')[0]
    #schemaRootNode["id"] = f'{no}'
    schemaRootNode["id"] = schemaRootNodeName
    #schemaRootNode["name"] = moduleName
    schemaRootNode["name"] = schemaRootNodeName
    #schemaRootNode["prefix"] = modules[moduleName][0]
    #schemaRootNode["namespace"] = modules[moduleName][1]
    schemaRootNode["children"] = []
    makeOneSchemaTree(inputJtoXTree[schemaRootNodeName][1],schemaRootNode["children"],schemaRootNodeName) #the container node
    generatedSchemas.append(schemaRootNode) 
    no += 1

  return generatedSchemas

'''
  "tree": {
    "chinaunicom-interface-common:if": [
      "container",
====makeOneSchemaTree===
      {
        "interfaces": [
          "container",
          {
            "interface": [
              "list",
              {
                "name": [
'''
#def makeOneSchemaTree(node, generatedTreeArray,idLevel):
def makeOneSchemaTree(node, generatedTreeArray,fartherName):
  no = 0
  for itemName in node.keys():
    # type is container or list
    if (node[itemName][0] in ["container","list"] ) :      
      newNode = {}
      newNode["id"] = fartherName + "\\" + itemName
      #newNode["id"] = f'{idLevel}.{no}'
      #newNode["id"] = f'{no}'
      newNode["name"] = itemName
      newNode["children"] = []
      makeOneSchemaTree(node[itemName][1], newNode["children"], newNode["id"])
      if ( len(newNode["children"]) == 0 ):
        del newNode["children"]
      generatedTreeArray.append(newNode)
      no += 1
