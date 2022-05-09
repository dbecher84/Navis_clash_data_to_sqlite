

import datetime
import xml.etree.ElementTree as ET

#path='C:\\Users\\Derek.Becher\\Desktop\\test\\clashes_in_sql\\00.01 Structural vs Architectural.xml'
#path='C:\\Users\\Derek.Becher\\Desktop\\test\\clashes_in_sql\\navis_output\\'

#test = ['00.01 Structural vs Architectural.xml', '02.06 Equipment vs Plumbing.xml']

#tree = ET.parse(path)
#root = tree.getroot()

clash_list = []

def read_tests(number, test_file):
    '''searches xml file for clash information and adds to a list.
       number: clash test number
       test_file: path to test file'''
    tree = ET.parse(test_file)
    #root = tree.getroot()
    
    for node in tree.iter('clash_result'):
        #print ('\\n')
        clash_info = []
        elem_present = []
        for elem in node.iter():
            #elem_present = []
            #clash_items = [elem.get('clash_guid'), elem.get('clash_id'), elem.get('status'), elem.get('group_name'),
                           #elem.get('date_created'), elem.get('element_1_guid'), elem.get('element_2_guid'),
                           #elem.get('export_date'), elem.get('test_id')]
            #if elem.tag=='clashresult':
                #clash_items = [elem.get('clash_guid'), elem.get('name'), elem.get('status')]
                #for item in clash_items:    
                    #lash_info.append(item)
                #print (clash_info)
            if elem.tag=='clash_guid':
                c_guid = elem.text
                #print (c_guid)           
            if elem.tag=='clash_id':
                c_id = elem.text
                #print (c_id)
            if elem.tag=='status':
                stat = elem.text
                #print (stat)
            if elem.tag=='group_name':
                g_name = elem.text
                #print (g_name)
            if elem.tag=='date_created':
                d_created = elem.text
                #print (d_created)
            if elem.tag=='element_1_guid':
                e1guid = elem.text
                #print (e1guid)
            if elem.tag=='element_2_guid':
                e2guid = elem.text
                #print (e1guid)
            if elem.tag=='export_date':
                e_date = elem.text
                #print (e_date)
            if elem.tag=='test_id':
                t_id = elem.text
                #print (t_id)
            if elem.tag=='assigned_to':
                if elem.text != None:
                    at_id = elem.text
                else:
                    at_id = "No_Assignee"

        #items_to_append = [c_guid, c_id, stat, e1guid, e2guid, g_name, d_created, at_id, e_date, t_id]

        ##use to exclude clashes in approved folder (these are not real clashes)
        if g_name.lower() != "approved":
            items_to_append = [c_guid, c_id, stat, e1guid, e2guid, g_name, d_created, at_id, e_date, t_id]
            for item in items_to_append:
                clash_info.append(item)
                
            clash_list.append(clash_info)
        
        #now = datetime.datetime.now()
        #clash_report_date = now.strftime('%Y.%m.%d')
        #clash_info.append(results_date)

        #clash_info.append(number)
    
        #clash_list.append(clash_info)
    
