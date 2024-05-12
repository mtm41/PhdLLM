import os
import json
from Category_FE import Process, Registry, System, File, Misc, Synchronisation, Resource, Crypto, Network, Ole, Services, __notification__, Certificate, UI
from PIL import Image

class LoaderFromLLM:

    categories = {}

    def __init__(self):
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
        filesPath = 'modified'

        for entry in os.listdir(filesPath):
            with open(filesPath + '/' + entry, 'r') as llmReport:
                rgbData = []
                apiCallRecord = llmReport.readline()
                while apiCallRecord:
                    try:
                        category = apiCallRecord.split(',')[0]
                        if category == 'Ui':
                            category = 'UI'
                        api = apiCallRecord.split(',')[1]
                        arguments = apiCallRecord.split(',')[2:]
                        feature = {
                                    'api': api,
                                    'return_value': '',
                                    'arguments': arguments,
                                    'flags': arguments
                        }
                        
                        print('Starting')
                        category_Obj = self.getCategoryObject(category)
                        category_encoded = category_Obj.id_dec
                        #print(category_encoded)
                        #print(api)
                        
                        api_encoded = category_Obj.encodeAPI(feature)
                        #print('API analysis done')
                        if category in ['Misc', 'Synchronisation', 'Resource', 'Ole', '__notification__', 'Certificate']:
                            print('category with arguments based on appearances')
                            arguments_encoded = category_Obj.encodeArgLLM(feature)
                        else:
                            arguments_encoded = category_Obj.encodeArgLLM(arguments)
                        #print(api_encoded)
                        #print(arguments)
                        print(arguments_encoded)
                        rgbData.append(int(category_encoded, base=16))
                        rgbData.append(int(api_encoded, base=16))
                        rgbData.append(int(arguments_encoded, base=16))
                        apiCallRecord = llmReport.readline()
                    except Exception as ex:
                        print('Exception: {}'.format(ex))
                    finally:
                        apiCallRecord = llmReport.readline()
                # We have every RGB value for the sample, we can build the image now
                while len(rgbData) < (900*3):
                    rgbData.append(0)
                    rgbData.append(0)
                    rgbData.append(0)
                colors_rgb = bytes(rgbData)
                img = Image.frombytes('RGB', (int(self.x), int(self.y)), colors_rgb)
                img.save('images/{}.png'.format(entry))


if __name__ == '__main__':
    loader = LoaderFromLLM()
    loader.convertToImages()