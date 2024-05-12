import json
from re import search
from importlib_metadata import files
from numpy.lib.function_base import average, median
import pandas as pd
import sys, getopt
#from PIL import Image
import numpy
import os
#from Category_FE import Process, Registry, System, File, Misc, Synchronisation, Resource, Crypto, Network, Ole, Services, __notification__, Certificate, Ui
from Category_FE_LLM import Process, Registry, System, File, Misc, Synchronisation, Resource, Crypto, Network, Ole, Services, __notification__, Certificate, Ui

class LoaderReports:

    def __init__(self, filespath, outputDirectory, x, y):
        self.filespath = filespath
        self.outputDirectory = outputDirectory
        self.x = x
        self.y = y
        self.categories = {}

    def getCategoryObject(self, categoryType):
        searchedCategory = None
        if categoryType in self.categories:
            searchedCategory = self.categories[categoryType]
        else:
            category_Obj = globals()[categoryType]()
            searchedCategory = category_Obj
            self.categories[categoryType] = category_Obj
        
        return searchedCategory                    

    def convertToImages(self):
        try:
            print('running')
            for entry in os.listdir(self.filespath):
                bad_file = False
                self.categories = {}
                self.categories.clear()
                filepath = os.path.join(self.filespath, entry)
                if os.path.isfile(filepath):
                    with open(filepath, 'r', encoding="utf8") as file:
                        rgbData = []
                        print(filepath)
                        jsonData = json.load(file)
                        if 'behavior' in jsonData:
                            processes = jsonData['behavior']['processes']
                            if len(processes) > 0:
                                for process in processes:
                                    calls = process['calls']
                                    if len(calls) > 0:
                                        for call in calls:
                                            try:
                                                category = str(call['category']).capitalize()
                                                feature = {
                                                    'api': call['api'],
                                                    'return_value': call['return_value'],
                                                    'arguments': call['arguments'] if 'arguments' in call else {},
                                                    'flags': call['flags'] if 'flags' in call else {'flags': 'Not Found'}
                                                }
                                                category_Obj = self.getCategoryObject(category)
                                                debug = True
                                                category_encoded = category_Obj.category
                                                #print('CATEGORY: ' + category + ',' + category_encoded)
                                                if debug == True:
                                                    #print(feature)
                                                    category_Obj.encodeApi(feature)
                                                    #print(category_Obj.apiCallName)
                                                    #print(category_Obj.apiCallArguments)
                                                    reportId = entry.split('.')[0]

                                                    with open('./summarized/{}_summarized.json'.format(reportId), 'a', encoding="utf8") as summarizedFile:
                                                        apiRecord = category_encoded + ',' + str(category_Obj.apiCallName) + ',' + str(category_Obj.apiCallArguments)
                                                        summarizedFile.writelines(apiRecord.replace('\'','"') + '\n')
                                            except Exception as ex:
                                                #print(call)
                                                print('Exception related to file categories: {}'.format(ex))
                                                #exit(1)
                        else:
                            bad_file = True

                    #if not bad_file:
                        # We have every RGB value for the sample, we can build the image now
                    #    while len(rgbData) < (900*3):
                    #        rgbData.append(0)
                    #        rgbData.append(0)
                    #        rgbData.append(0)
                    #    colors_rgb = bytes(rgbData)
                    #    img = Image.frombytes('RGB', (int(self.x), int(self.y)), colors_rgb)
                    #    img.save('images/Second_Dataset/Test/{}.png'.format(filepath.split('\\')[6].split('.')[0]))
        except Exception as ex:
            print('Exception: {}'.format(ex))
                        

def main():
    filespath = ''
    outputDirectory = ''
    x = 0
    y = 0

    try:
        args, opts = getopt.getopt(sys.argv,"hi:o:x:y", ["--ifile=", "--dir=", "--XDimension", "--YDimension"])
    except getopt.GetoptError:
        print('LoaderJson.py -i <inputDir> -o <outputDirectory> -x <XDimension> -y <YDimension>')
        sys.exit(2)
    
    count = 0
    for opt in opts:
        if opt == '-h':
            print('Loader.py -i <inputDir> -o <outputDirectory> -x <XDimension> -y <YDimension>')
            sys.exit()
        elif opt in ("-i", "--inputDir"):
            filespath = opts[count+1]
        elif opt in ("-o", "--outputDirectory"):
            outputDirectory = opts[count+1]
        elif opt in ("-x", "--XDimension"):
            x = opts[count+1]
        elif opt in ("-y", "--YDimension"):
            y = opts[count+1]
        count += 1
    print(filespath)
    loaderJson = LoaderReports(filespath, outputDirectory, x, y)
    loaderJson.convertToImages()

if __name__ == '__main__':
    main()
    