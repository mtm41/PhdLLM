import os
import json

for file in os.listdir('D:\\repos\\reports\\Downloaded\\reports\\ALL_1\\final_windows'):
    print(file)
    with open('D:\\repos\\reports\\Downloaded\\reports\\ALL_1\\final_windows\\' + file, 'r+') as reportFile:
        report = json.load(reportFile)
        try:
            processes = report['behavior']['processes']
            tid_count = 0
            not_tid = 0
            modifiedProcesses = []
            for process in processes:
                modifedCalls = []
                for call in process['calls']:
                    if 'tid' not in call:
                        not_tid += 1
                        call["tid"] = 0
                        modifedCalls.append(call)
                        #print('This call does NOT have tid key')
                        #print(call)
                    else:
                        #print('This call does have a tid key')
                        tid_count += 1
                        modifedCalls.append(call)
                process['calls'] = modifedCalls
                modifiedProcesses.append(process)
                print('Added {} tids to this report'.format(not_tid))
            processes = modifiedProcesses
            report['behavior']['processes'] = processes
            reportFile.seek(0)
            reportFile.truncate()
            json.dump(report, reportFile)
        except Exception as ex:
            with open('D:\\repos\\reports\\Downloaded\\reports\\bad_report.txt', 'a') as registry:
                registry.writelines(file) 