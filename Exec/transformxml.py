'''
import os
import xmltodict
import js2xml
import json as JSON

def jsonToXml(json_path):
    
    #传入json文件，输出xml文件信息
    
    
    convertXml=''
    with open(json_path,encoding='utf-8-sig', errors='ignore') as f:
        #JSON.dumps(f.read(), ensure_ascii=False)
        jsDict = f.read()
    try:
        convertXml=js2xml.parse(jsDict,encoding='utf-8')
    except:
        convertXml=js2xml.parse({'request':jsDict},encoding='utf-8')
    return convertXml
jsons_path=r'F:\toppic_zf\FB_CB_1_html\toppic_prsm_cutoff\data_js\prsms/'
for js in os.listdir(jsons_path):
    if js.endswith('.json'):
        file_path=jsons_path+js
        tmp=jsonToXml(file_path)
        f=open(file_path.split('.')[0]+'.xml','w',encoding='gbk')
        #print(file_path.split('.')[0]+'.xml')
        f.write(tmp)
        f.close()
'''
import os
from json import loads
import dicttoxml
from xml.dom.minidom import parseString


def jsonToXml(json_path, xml_path):
    #@abstract: transfer json file to xml file
    #json_path: complete path of the json file
    #xml_path: complete path of the xml file
    with open(json_path,'r',encoding='UTF-8')as json_file:
        load_dict=loads(json_file.read())
    #print(load_dict)
    my_item_func = lambda x: 'Annotation'
    xml = dicttoxml(load_dict,custom_root='Annotations',item_func=my_item_func,attr_type=False)
    dom = parseString(xml)
    #print(dom.toprettyxml())
    #print(type(dom.toprettyxml()))
    with open(xml_path,'w',encoding='UTF-8')as xml_file:
        xml_file.write(dom.toprettyxml())
        
def json_to_xml(json_dir, xml_dir):
    #transfer all json file which in the json_dir to xml_dir
    if(os.path.exists(xml_dir)==False):
        os.makedirs(xml_dir)
    dir = os.listdir(json_dir)
    for file in dir:
        file_list=file.split(".")
        if(file_list[-1] == 'json'):
            jsonToXml(os.path.join(json_dir,file),os.path.join(xml_dir,file_list[0]+'.xml'))  
if __name__ == '__main__':
    #trandfer singal file
    #j_path = "F:/work/jsontoxml/json/test.json"
    #x_path = "F:/work/jsontoxml/json/test.xml"
    #jsonToXml(j_path,x_path)

    #transfer multi files
    j_dir = "D:\\toppic_zf\\FB_CB_1_html\\toppic_prsm_cutoff\\data_js\\prsms\\"
    x_dir = "F:\\toppic_zf\\FB_CB_1_html\\toppic_prsm_cutoff\\data_xml\\prsms\\"
    json_to_xml(j_dir, x_dir)
