import os
import json

for file in os.listdir('/mnt/d/repos/reports/Downloaded/realTest/'):
    with open('/mnt/d/repos/reports/Downloaded/realTest/' + file, 'r') as reportFile:
        report = json.load(reportFile)
        platform = report["info"]["platform"]
        if platform in ('windows', 'linux'):
            with open('platform.txt', 'a') as platformRegistry:
                platformRegistry.writelines(str(file) + ' ' + str(platform) + '\n')
        else:
            with open('platform.txt', 'a') as platformRegistry:
                platform = report["info"]["machine"]["platform"]
                platformRegistry.writelines(str(file) + ' ' + str(platform) + '\n')