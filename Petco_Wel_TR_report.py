import xlrd as xd
import datetime as dt
from testrail import create_testcase,create_run,update_run,send_report
from variables import Wellness,ph_project_id


#Get current date
date = dt.date.today()
curdt = str(date.strftime("%m")+date.strftime("%d")+date.strftime("%Y"))


#Get filename and description
filename = Wellness['proj_name'] +'_Test_results_' + curdt
filedescp = Wellness['proj_name'] + ' test results for the prod release on date ' + curdt


# get data from excel
wb = xd.open_workbook(Wellness['fpath'])
wb_sheet = wb.sheet_by_index(0)
testcasename = []
testcaseresult = []
trellolink = []
testcomments = []
testcasestatus =[]

# get data from excel into lists
for i in range (1, wb_sheet.nrows):
    rowdata = wb_sheet.row(i)
    trellolink.append(rowdata[1].value)
    testcasename.append(rowdata[2].value)
    testcaseresult.append(rowdata[3].value)
    testcasestatus.append(rowdata[4].value)
    testcomments.append(rowdata[5].value)

# Map teststatus to 1= Pass, 2= Fail ,3= Blocked
testcasestatus = [1 if i=='Pass' else 5 if i=='Fail' else 2 if i=='Blocked' else 'invalid value' for i in testcasestatus]

#Testrail trigger for creating tests, including them in test runs ,updating the testrun and sending the report
for i in range (0,len(testcasename)):
    create_testcase(testcasename[i],trellolink[i],testcaseresult[i],Wellness['section_id'])
print (str(len(testcasename)) +' Testcases created!')

create_run (filename,filedescp,ph_project_id,Wellness['suite_id'],Wellness['milestone_id'])
print ('Test run created!')

for i in range (0,len(testcasename)):
    update_run(i,testcomments,testcasestatus[i])
print ('Test run updated!')

send_report(Wellness['report_id'])
print ('Test report sent!')
