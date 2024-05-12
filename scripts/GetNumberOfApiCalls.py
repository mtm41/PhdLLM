import getopt
import os
import json
import sys

def main(file):
    try:
        file += '.json'
        print(file)
        with open('/mnt/d/repos/reports/Downloaded/reports/ALL_2/good_dataset/' + file, 'r+') as reportFile:
            report = json.load(reportFile)
            try:
                processes = report['behavior']['processes']
                tid_count = 0
                not_tid = 0
                modifiedProcesses = []
                foundCalls = False
                api_calls_count = 0
                for process in processes:
                    if len(process['calls']) > 0:
                        foundCalls = True
                        print(len(process['calls']))
                        api_calls_count += len(process['calls'])
                with open('/mnt/d/repos/reports/Downloaded/number_api_calls_per_sampleB.csv', 'a') as fileWrite:
                        fileWrite.writelines(str(file) + ',' + str(api_calls_count) + '\n')
                if not foundCalls:
                    with open('/mnt/d/repos/reports/Downloaded/bad_samples.txt', 'a') as fileWrite:
                        fileWrite.writelines(file + '\n')
            except Exception as ex:
                with open('/mnt/d/repos/reports/Downloaded/bad_samples.txt', 'a') as fileWrite:
                        fileWrite.writelines(file + '\n')
    except Exception as ex:
            with open('/mnt/d/repos/reports/Downloaded/number_api_calls_per_sampleB.csv', 'a') as fileWrite:
                        fileWrite.writelines(str(file) + ',Not found' + '\n')

if __name__ == '__main__':
    model = ''
    try:
        args, opts = getopt.getopt(sys.argv,"hf:o", ["--file="])
    except getopt.GetoptError:
        print('Main.py -f <file>')
        sys.exit(2)
    
    count = 0
    for opt in opts:
        if opt == '-h':
            print('Main.py -f <file>')
            sys.exit()
        elif opt in ("-f", "--file"):
            model = opts[count + 1]
        count += 1

    main(model)