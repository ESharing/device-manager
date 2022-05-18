import logging
from typing import ItemsView
from ncclient import manager
from jtox2treeview import *
import xmltodict
import xml.dom.minidom
import re

# netconf connect list
currentConns = {}
nodeSchema = {}
schemaStore = {}
SLOT_MASK = 0x1F800000
PORT_MASK = 0x0007F000

logging.basicConfig(
       level=logging.INFO,
   )

netconf_filter_MO = """
<MOs xmlns="urn.utstar:uar:MO">
    <MO>
    </MO>
</MOs>
"""
def getNetconfConnection(node_ip,p=830,user='admin',pw='AdMiN123'):
    if ( node_ip in currentConns and currentConns[node_ip].connected) :
        #print ('getSchemas connection existed')
        return currentConns[node_ip]
    else:        
        currentConns[node_ip] = manager.connect(host=node_ip,port=p,username=user,password=pw,hostkey_verify=False)
        #manager.set_logger_level(currentConns[node_ip], logging.DEBUG)
        return currentConns[node_ip]

def cardToTreeData(cards):
    treeData = {'items':[]}
    i = 0
    sortedCardNo = sorted(cards.keys())
    for cardNo in sortedCardNo:
        cardData = {}
        cardData['id'] = cardNo
        cardData['name'] = cards[cardNo]['name']
        treeData['items'].append(cardData)
        portNum = len(cards[cardNo]['ports']) 
        if ( portNum > 0 ):
            treeData['items'][i]['children'] = []
            sortedPortNo = sorted(cards[cardNo]['ports'])
            for portNo in sortedPortNo:
                portData = {}
                portData['id'] = f'{cardNo}.{portNo}'
                portData['name'] = cards[cardNo]['ports'][portNo]
                treeData['items'][i]['children'].append(portData)
        i += 1

    return treeData

#m = manager.connect(host='10.5.128.207',port=830,username='admin',password='AdMiN123',hostkey_verify=False)
def getSchemas(node_ip, ne_type):
    if ne_type not in nodeSchema:
        nodeSchema[ne_type] = {}
        schemaStore[ne_type] = {}
        nodeSchema[ne_type]['items'] = getSchemasFromFile(ne_type)
    return nodeSchema[ne_type]

def getSchemasFromFile(ne_type):
  with open(sys.path[0] + '/cucc-yang/jtox.json') as f:
  #with open('.\cucc-yang\jtox-if-acl.json') as f:
    schemaStore[ne_type] = json.load(f)
  #schemaStore[ne_type] = copy.deepcopy(data)
  #schemaModule = data["modules"]
  return generateSchemas(schemaStore[ne_type]["tree"], schemaStore[ne_type]["modules"])
  #print (data["modules"].keys())
'''    
    m = getNetconfConnection(node_ip)
    NE_Type = 'UNKNOWN'
    modules = []
    if ( ne_type.find('UT') != -1):
            NE_Type = 'urn.utstar'
    if ( ne_type.find('CUCC') != -1):
            NE_Type = 'chinaunicom'

    for capability in m.server_capabilities:
        if ( NE_Type in capability):
            try:
                moduleName = capability[capability.index('=')+1 : capability.index('&')]
            except:
                continue
            modules.append(moduleName)
    modules.sort()
    schemas = {'items':[]}
    i = 0
    for moduleName in modules:
        #print(moduleName)
        treeNode = {}
        treeNode['id'] = i
        treeNode['name'] = moduleName
        schemas['items'].append(treeNode)
        i += 1
    return schemas
'''

def getObjects(node_ip, ne_type):
    m = getNetconfConnection(node_ip)
    
    ''' currently, only use UT's MO to get card and interface
    NE_Type = 'UNKNOWN'
    modules = []
    if ( ne_type.find('UT') != -1):
            NE_Type = 'urn.utstar'
    if ( ne_type.find('CUCC') != -1):
            NE_Type = 'chinaunicom'
    '''

    running_config = m.get_config("running", filter = ( 'subtree', netconf_filter_MO))

    running_config_xml = xmltodict.parse(running_config.xml)["nc:rpc-reply"]["data"]["MOs"]["MO"]

    card = {}
    for rec in running_config_xml:
        # Fid \\s=X\\c=1 SpecId T1CardXXX ; 
        # Fid \\s=X\\c=1\\j=X\\p=1 SpecId T1PortXXX ; 

        # initial card resource 
        if ( 's=' in rec['Fid'] and 'c=' in rec['Fid']):
            matchObj = re.match('(.*)s=(\d*)(.*)', rec['Fid'])
            id = int(matchObj.group(2))
            if id not in card: 
                card[id] = {}
                card[id]['ports'] = {}

        if ( 'T1Card' in rec['SpecId']):
            matchObj = re.match('(.*)=(\d*)(.*)=(\d*)', rec['Fid'])
            id = int(matchObj.group(2))
            card[id]['name'] = 'Slot' + matchObj.group(2) + ' ' + rec['SpecId'][6:]

        if ( 'T1Port' in rec['SpecId']):
            matchObj = re.match('(.*)=(\d*)(.*)=(\d*)(.*)=(\d*)(.*)=(\d*)', rec['Fid'])
            id = int(matchObj.group(2))
            portNo = int(matchObj.group(6))
            card[id]['ports'][portNo] = f'eth {id}.{portNo}'

#    print (cardToTreeData(card))
    return (cardToTreeData(card))
#    m.close_session()

'''
>>> netconf_filter="""    
... <if xmlns="http://chinaunicom.com/yang/interface/chinaunicom-interface-common">
... <interfaces>
... <interface>
... <ip xmlns="http://chinaunicom.com/yang/interface/chinaunicom-interface-l2l3common">
... </ip>
... </interface>
... </interfaces>
... </if>
... """
'''
# http://localhost:8080/api/schema-data?ip=10.240.70.69&type=CUCC&schema-name=chinaunicom-interface-common:if\interfaces\interface\chinaunicom-interface-l2l3common:ip\ipv4-address-list
def makeNetconfFilter(ne_type,schemaName):
    moduleStr = 'modules'
    #split schema name by \
    levelPosition = schemaName.find("\\")
    if levelPosition > -1 :
        currentItem = schemaName[:levelPosition]
        leftItems = schemaName[levelPosition+1:]        
        modulePosition = currentItem.find(":")
        if modulePosition > -1 :
            prefix = currentItem[modulePosition+1:]
            xmlns = schemaStore[ne_type][moduleStr][currentItem[:modulePosition]][1]
            return f'<{prefix} xmlns="{xmlns}">\n {makeNetconfFilter(ne_type,leftItems)}\n</{prefix}>'
        else:
            return f'<{currentItem}>\n {makeNetconfFilter(ne_type,leftItems)}\n</{currentItem}>'
    else : #last level
        modulePosition = schemaName.find(":")
        if modulePosition > -1 :
            # <prefix xmlns="xxx"/> 
            return f'<{schemaName[modulePosition+1:]} xmlns="{schemaStore[ne_type][moduleStr][schemaName[:modulePosition]][1]}"/>\n'
        else:# <prefix/>
            return f'<{schemaName}/>'    

def toUITableData(srcData, dataTable, currentRow, tableName):
    '''
    iterate scrData Items
      if item is list 
        iterate list item
        if item's data type is OrderedDict, recursion
        columnName = itemName
        columnValue = itemValue
    '''

    for key in srcData:
        if key == '@xmlns':
            continue
        value = srcData[key]
        if isinstance(value,dict):
            toUITableData(value, dataTable,currentRow, tableName)
            if key == tableName:
                dataTable.append(currentRow.copy())
                #currentRow = {}
        elif isinstance(value,list):
            for item in value:
                if isinstance(item,dict):
                    toUITableData(item, dataTable,currentRow, tableName)
                if key == tableName:
                    dataTable.append(currentRow.copy())
                    #currentRow = {}
            #rowCount += 1
        else:
            currentRow[key] = value

    return dataTable       

def getTableHeaderByRow(row):
    header = []
    for key in row:
        headerItem = {}
        headerItem['text'] = key
        headerItem['value'] = key
        header.append(headerItem)
    return header

def getSchemaData(node_ip, ne_type, schemaName):
    m = getNetconfConnection(node_ip)
        
    NE_Type = 'UNKNOWN'
    modules = []
    if ( ne_type.find('UT') != -1):
            NE_Type = 'urn.utstar'
    if ( ne_type.find('CUCC') != -1):
            NE_Type = 'chinaunicom'
    
## construct the netconf_filter
    netconf_filter = makeNetconfFilter(ne_type,schemaName)

    namePos = schemaName.rindex('\\')
    tableName = schemaName[namePos+1:]

    running_config = m.get_config("running", filter = ( 'subtree', netconf_filter))
    print(netconf_filter)

    tableData = {}
    tableDataRecords = toUITableData(xmltodict.parse(running_config.xml)['nc:rpc-reply']['data'], [], {}, tableName)
    if len(tableDataRecords) == 0:
        return {}
    else:
        tableData['items'] = tableDataRecords
        tableData['headers'] = getTableHeaderByRow(tableData['items'][0])
    
    return tableData
'''
    return {
        'items':[
            {
                'name': 'KitKat',
                'calories': 518,
                'fat': 26.0,
            },            
        ],
        'headers':[
            {
                'text': 'Dessert (100g serving)',
                'align': 'start',
                'sortable': True,
                'value': 'name',
            },
            { 'text': 'Calories', 'value': 'calories' },
            { 'text': 'Fat (g)', 'value': 'fat' },
        ]}
'''
'''
    running_config = m.get_config("running", filter = ( 'subtree', netconf_filter_MO))

    running_config_xml = xmltodict.parse(running_config.xml)["nc:rpc-reply"]["data"]["MOs"]["MO"]

    card = {}
    for rec in running_config_xml:
        # Fid \\s=X\\c=1 SpecId T1CardXXX ; 
        # Fid \\s=X\\c=1\\j=X\\p=1 SpecId T1PortXXX ; 

        # initial card resource 
        if ( 's=' in rec['Fid'] and 'c=' in rec['Fid']):
            matchObj = re.match('(.*)s=(\d*)(.*)', rec['Fid'])
            id = int(matchObj.group(2))
            if id not in card: 
                card[id] = {}
                card[id]['ports'] = {}

        if ( 'T1Card' in rec['SpecId']):
            matchObj = re.match('(.*)=(\d*)(.*)=(\d*)', rec['Fid'])
            id = int(matchObj.group(2))
            card[id]['name'] = 'Slot' + matchObj.group(2) + ' ' + rec['SpecId'][6:]

        if ( 'T1Port' in rec['SpecId']):
            matchObj = re.match('(.*)=(\d*)(.*)=(\d*)(.*)=(\d*)(.*)=(\d*)', rec['Fid'])
            id = int(matchObj.group(2))
            portNo = int(matchObj.group(6))
            card[id]['ports'][portNo] = f'eth {id}.{portNo}'

#    print (cardToTreeData(card))
    return (cardToTreeData(card))
#    m.close_session()
'''
