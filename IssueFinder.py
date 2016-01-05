import re
import string
import random
import array
import datetime
import time
import glob
import os
import sys
import getopt
import xlwt
import xml.etree.ElementTree as et
import json
from string import atoi
from xlwt import *
from decimal import Decimal
#from datetime import datetime, date, timedelta
from time import strptime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


###################################################################
#issue_dict = {
#        'issue_type':None,
#        'issue_app':None,
#        'issue_create_time':None,
#        'issue_root_cause':None,
#        'issue_location':None
#    }
##################################################################
total_logfile_num = 0
issue_count_dict={}
id = 1
###################################################################
def UpdateDataToExcel():
    time_stamp = time.strftime("%Y-%m-%d-%H%M%S", time.localtime())
    ReportFile = 'report\IssueReport_'+time_stamp+'.xls'

    # Define Fond & Style for excel subject slot for JIRA
    font_subject_jira = Font()
    font_subject_jira.name = 'Arial'
    font_subject_jira.bold = True
    font_subject_jira.colour_index = 1
    font_subject_jira.outline = True
    pattern_subject_jira = xlwt.Pattern()
    pattern_subject_jira.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern_subject_jira.pattern_fore_colour = 18
    alignment_subject_jira = xlwt.Alignment()
    alignment_subject_jira.horz = xlwt.Alignment.HORZ_CENTER
    alignment_subject_jira.vert = xlwt.Alignment.VERT_CENTER
    borders_subject_jira = Borders()
    borders_subject_jira.left = 1
    borders_subject_jira.right = 1
    borders_subject_jira.top = 1
    borders_subject_jira.bottom = 1
    style_subject = XFStyle()
    style_subject.font = font_subject_jira
    style_subject.pattern = pattern_subject_jira
    style_subject.alignment = alignment_subject_jira
    style_subject.borders = borders_subject_jira
    # Define Fond & Style for excel data slot
    font_data = Font()
    font_data.name = 'Arial'
    borders_data = Borders()
    borders_data.left = 1
    borders_data.right = 1
    borders_data.top = 1
    borders_data.bottom = 1
    style_data = XFStyle()
    style_data.font = font_data
    style_data.borders = borders_data

    file_handle = xlwt.Workbook()
    # Generate sheet JIRA for JIRA issue list with CR mapping
    sheet_handle_report = file_handle.add_sheet('report')
    # Update subject
    sheet_handle_report.write(0, 0, 'ID', style_subject)
    sheet_handle_report.col(0).width = 2000
    sheet_handle_report.write(0, 1, 'IssueType', style_subject)
    sheet_handle_report.col(1).width = 5000
    sheet_handle_report.write(0, 2, 'IssueAPP', style_subject)
    sheet_handle_report.col(2).width = 5000
    sheet_handle_report.write(0, 3, 'IssueCreateTime', style_subject)
    sheet_handle_report.col(3).width = 5000
    sheet_handle_report.write(0, 4, 'IssueRootCause', style_subject)
    sheet_handle_report.col(4).width = 5000
    sheet_handle_report.write(0, 5, 'IssueLocation', style_subject)
    sheet_handle_report.col(5).width = 5000
    # Skip one column
    #sheet_handle_report.write(0, 5, 'TA Name', style_subject)
    #sheet_handle_report.col(5).width = 5000
    #sheet_handle_report.write(0, 6, 'Total', style_subject)
    #sheet_handle_report.col(6).width = 2000
    #sheet_handle_report.write(0, 7, 'Pass', style_subject)
    #sheet_handle_report.col(7).width = 2000
    #sheet_handle_report.write(0, 8, 'Fail', style_subject)
    #sheet_handle_report.col(8).width = 2000
    # Update TB data
    row = 1
    for ID in issue_count_dict.keys():
        sheet_handle_report.write(row, 0, ID, style_data)
        sheet_handle_report.write(row, 1, issue_count_dict[ID]['issue_type'], style_data)
        sheet_handle_report.write(row, 2, issue_count_dict[ID]['issue_app'], style_data)
        sheet_handle_report.write(row, 3, issue_count_dict[ID]['issue_create_time'], style_data)
        sheet_handle_report.write(row, 4, issue_count_dict[ID]['issue_root_cause'], style_data)
        sheet_handle_report.write(row, 5, issue_count_dict[ID]['issue_location'], style_data)
        row = row + 1
    # Update TA data
    #row = 1
    #for TA in Dict_TASummary.keys():
    #    sheet_handle_report.write(row, 5, TA, style_data)
    #   sheet_handle_report.write(row, 6, Dict_TASummary[TA]['Total'], style_data)
    #    sheet_handle_report.write(row, 7, Dict_TASummary[TA]['Pass'], style_data)
    #    sheet_handle_report.write(row, 8, Dict_TASummary[TA]['Fail'], style_data)
    #    row = row + 1

    file_handle.save(ReportFile)


def ParseCapellaLog(filepath):
    global issue_count_dict
    valid_flag = False
    global id 
    with file(filepath) as f:
        lines = f.readlines()
        for ln in lines:
            issue_dict = {}                          
            if re.match('\d',ln) and re.search("am_crash",ln):
                if len(re.findall('\[(.*)\]',ln))==1:
                    issue_pro =  re.findall('\[(.*)\]',ln)[0].split(',')
                    issue_dict['issue_type']  = "Force Close"
                    issue_dict['issue_app'] = issue_pro[2]
                    issue_dict['issue_create_time'] = ln[0:17]
                    issue_dict['issue_root_cause'] = str(issue_pro[4:])
                    issue_dict['issue_location']  = filepath
                    issue_count_dict[id]=issue_dict
                    id+=1

            if re.match('\d',ln) and re.search("am_anr",ln):
                if len(re.findall('\[(.*)\]',ln))==1:                        
                    issue_pro =  re.findall('\[(.*)\]',ln)[0].split(',')
                    issue_dict['issue_type'] = "ANR"
                    issue_dict['issue_app'] = issue_pro[2]
                    issue_dict['issue_create_time'] = ln[0:17]
                    issue_dict['issue_root_cause'] = str(issue_pro[4:])
                    issue_dict['issue_location'] = filepath
                    issue_count_dict[id]=issue_dict
                    id+=1

            if re.match('\d',ln) and re.search("boot_progress_start",ln) and atoi(ln.split()[-1])>1000:                
                issue_dict['issue_type'] = "FWR"
                issue_dict['issue_app']  = "Framework"
                issue_dict['issue_create_time'] = ln[0:17]
                issue_dict['issue_root_cause'] = ln.split()[-1]
                issue_dict['issue_location'] = filepath
                issue_count_dict[id]=issue_dict
                id+=1                
    print "\tFile parsed success"

###################################################################
def GoThroughFolder(rootdir):
    global total_logfile_num

    for root, subFolder_list, subfiles_list in os.walk(rootdir):
        # Go though subfile list
        for subfile in subfiles_list:
            file = os.path.join(root,subfile)
            # Analysis capella log, not in crash log folder
            if re.match("capella_event.*", subfile) or re.match("logcat_event.*",subfile) and root.find('Crash_') == -1:
                total_logfile_num = total_logfile_num + 1
                print "log (%d): %s" % (total_logfile_num, file)
                ParseCapellaLog(file)

###################################################################
def usage():
    print "Please check IssueFinder  script usage:\n"
    print "     python IssueFinder.py {logPath}"
    print "         -h|--help       :   print help message"

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError:
        usage()
        sys.exit()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
            
    logPath = args[0]
    
    global total_logfile_num
    
    start_time = time.strftime("%Y-%m-%d %X", time.localtime())
    
    pathArr = []
    if logPath:
        pathArr = logPath.split(',')
    else:
        try:
            tree = et.parse('parser_config.xml')
            root = tree.getroot()
            for log in root.findall('log'):
                pathArr.append(log.get('path'))
        except Exception as e:
            print "[Exception] "+str(e)

    for path in pathArr:
        path = path.strip()
        print "============================================================"
        print "Start parsing path: %s" % path
        print "============================================================"
        GoThroughFolder(path)


    print "Write parsed data to excel..."
    UpdateDataToExcel()   

    end_time = time.strftime("%Y-%m-%d %X", time.localtime())
    print "Start Time: %s" % start_time
    print "End Time: %s" % end_time
    print "Total file number: %d" %total_logfile_num
    print "Total valid issue number: %d" %len(issue_count_dict)
###################################################################
###################################################################
if __name__ == "__main__":
    main()
