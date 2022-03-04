from ncclient import manager
from pprint import pprint
import xmltodict
import xml.dom.minidom
import re


SLOT_MASK = 0x1F800000
PORT_MASK = 0x0007F000

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
                portData['id'] = portNo
                portData['name'] = cards[cardNo]['ports'][portNo]
                treeData['items'][i]['children'].append(portData)
        i += 1

    return treeData

m = manager.connect(host='10.240.70.69',port=830,username='admin',password='AdMiN123', hostkey_verify=False)
#m = manager.connect(host='10.5.128.207',port=830,username='admin',password='AdMiN123', hostkey_verify=False)
#schema=m.get_schema('AclCfg')
#print (schema)
'''
netconf_filter = """
<filter type="subtree">
<IfCfgs xmlns="urn.utstar:uar:IfCfg" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"/>
</filter>
"""
'''
'''
netconf_filter = """
<EthPortStats xmlns="urn.utstar:uar:EthPortStat">
    <EthPortStat>
        <IfIndex></IfIndex>
    </EthPortStat>
</EthPortStats>
"""

running_config = m.get_config("running", filter = ( 'subtree', netconf_filter))

running_config_xml = xmltodict.parse(running_config.xml)["nc:rpc-reply"]["data"]["EthPortStats"]["EthPortStat"]
#print(xml.dom.minidom.parseString(str(running_config)).toprettyxml())
for intf in running_config_xml:
    # \\\interface=538446336
    intf_num = int(intf['IfIndex'][13:])
    slot = (intf_num & SLOT_MASK) >> 23
    port = (intf_num & PORT_MASK) >> 12
    print (f'eth {slot+1}.{port+1}')

'''
'''
netconf_filter = """
<MOs xmlns="urn.utstar:uar:MO">
    <MO>
    </MO>
</MOs>
"""
'''
'''
>>> netconf_filter = """
... <if xmlns="http://chinaunicom.com/yang/interface/chinaunicom-interface-common">
... </if>
... """
>>> netconf_filter = """
... <if xmlns="http://chinaunicom.com/yang/interface/chinaunicom-interface-common">
... <interfaces>
... <interface>
    <ip xmlns="http://chinaunicom.com/yang/interface/chinaunicom-interface-l2l3common">
    </ip>
... </interface>
... </interfaces>
... </if>
... """
<?xml version="1.0" ?>
<nc:rpc-reply xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:1edfeb47-01ce-45cd-ae73-e7870e4a7bee">
        <data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <if xmlns="http://chinaunicom.com/yang/interface/chinaunicom-interface-common">
                        <interfaces>
                                <interface>
                                        <name>mgmt0/0/0/0</name>
                                        <ip xmlns="http://chinaunicom.com/yang/interface/chinaunicom-interface-l2l3common">
                                                <ipv4-address-list>
                                                        <ipv4-address>10.240.70.69/24</ipv4-address>
                                                        <secondry-use>mast</secondry-use>
                                                </ipv4-address-list>
                                        </ip>
                                </interface>
                                <interface>
                                        <name>loopback65534</name>
                                        <ip xmlns="http://chinaunicom.com/yang/interface/chinaunicom-interface-l2l3common">
                                                <ipv4-address-list>
                                                        <ipv4-address>140.188.217.64/32</ipv4-address>
                                                        <secondry-use>mast</secondry-use>
                                                </ipv4-address-list>
                                        </ip>
                                </interface>
                        </interfaces>
                </if>
        </data>
</nc:rpc-reply>

copy from netconf browser
  <filter type="subtree">
    <if:if xmlns:l2l3if="http://chinaunicom.com/yang/interface/chinaunicom-interface-l2l3common"
           xmlns:if="http://chinaunicom.com/yang/interface/chinaunicom-interface-common">
      <if:interfaces>
        <if:interface>
          <l2l3if:ip/>
        </if:interface>
      </if:interfaces>
    </if:if>
  </filter>
'''
#if is the prefix from schema
netconf_filter = """
<if xmlns="http://chinaunicom.com/yang/interface/chinaunicom-interface-common">
<interfaces>
<interface/>
</interfaces>
</if>
"""

running_config = m.get_config("running", filter = ( 'subtree', netconf_filter))

running_config_xml = xmltodict.parse(running_config.xml)["nc:rpc-reply"]["data"]["MOs"]["MO"]
#print(xml.dom.minidom.parseString(str(running_config)).toprettyxml())
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
        card[id]['name'] = rec['SpecId'][6:]

    if ( 'T1Port' in rec['SpecId']):
        matchObj = re.match('(.*)=(\d*)(.*)=(\d*)(.*)=(\d*)(.*)=(\d*)', rec['Fid'])
        id = int(matchObj.group(2))
        portNo = int(matchObj.group(6))
        card[id]['ports'][portNo] = f'eth {id}.{portNo}'

print (card)
print (cardToTreeData(card))
m.close_session()


'''
    <?xml version="1.0" encoding="utf-8"?>
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="12">
  <get-config>
    <source>
      <running/>
    </source>
    <filter type="subtree">
      <EthPortStat:EthPortStats xmlns:EthPortStat="urn.utstar:uar:EthPortStat">
        <EthPortStat:EthPortStat>
          <EthPortStat:IfIndex/>
        </EthPortStat:EthPortStat>
      </EthPortStat:EthPortStats>
    </filter>
  </get-config>
</rpc>

<filter type="subtree">
    <EthPortStats xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" >
    <EthPortStat>
        <IfIndex></IfIndex>
    </EthPortStat>
    </EthPortStats>
</filter>

<top xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <EthPortStats xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" >
    <EthPortStat>
        <IfIndex></IfIndex>
    </EthPortStat>
    </EthPortStats>
</top>
'''