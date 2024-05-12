from sklearn.feature_extraction import FeatureHasher
import numpy as npy
#from Category_FE import Process, Registry, System, File, Misc, Synchronisation, Resource, Crypto, Network, Ole, Services, __notification__, Certificate, Ui


name = 'api'
arguments = 'arguments'
flags = 'flags'
regKey = 'regkey'
functionName = 'function_name'
filepath = 'filepath'
strings = 'string'
algorithm_identifier = 'algorithm_identifier'
service_name = 'service_name'
module_name = 'module_name'

class Process():
    category = 'Process'
    apiCalls = []
    apiCallName = ''
    apiCallArguments = ''

    def getCategory(self):
        return self.category

    def __init__(self, apiObj):
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)
    
    def __init__(self):
        pass

    def encodeApi(self, apiObj):
        apiCallName = 'Not Found'
        apiCallArguments = 'Not Found'
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiObj)

    def encodeArg(self, argumentsObj):
        arguments = 'Not Found'
        if flags in argumentsObj:
            arguments = [argumentsObj[flags]]
            hasher = FeatureHasher(n_features=1, dtype=npy.ubyte)
            hashed_feature = hasher.transform(arguments).toarray()
        
            if hashed_feature[0][0] >= 256:
                hashed_feature[0][0] = 0
            arguments = hashed_feature[0][0]
        else:
            hasher = FeatureHasher(n_features=1, dtype=npy.ubyte)
            hashed_feature = hasher.transform(argumentsObj).toarray()
        
            if hashed_feature[0][0] >= 256:
                hashed_feature[0][0] = 0
            arguments = hashed_feature[0][0]
        return {flags: arguments}

class Registry():
    category = 'Registry'
    apiCalls = []
    apiCallName = ''
    apiCallArguments = ''
    regKeys = []

    def getCategory(self):
        return self.category


    def __init__(self, apiObj):
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def __init__(self):
        pass

    def encodeApi(self, apiObj):
        apiCallName = 'Not Found'
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def encodeArg(self, argumentsObj):
        arguments = 'Not Found'
        if regKey in argumentsObj:
            registryKey = argumentsObj[regKey]
            if not registryKey in self.regKeys:
                self.regKeys.append(registryKey)
            arguments = registryKey
        
        return {'RegistryKey': arguments}

class System():
    category = 'System'
    apiCalls = []
    apiCallName = ''
    apiCallArguments = ''
    functionNames = []

    def getCategory(self):
        return self.category


    def __init__(self, apiObj):
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def __init__(self):
        pass

    def encodeApi(self, apiObj):
        apiCallName = 'Not Found'
        apiCallArguments = 'Not Found'
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def isPath(self, possiblePath):
        isPath = False
        if str(possiblePath).__contains__('\\') or str(possiblePath).__contains__('/'):
            isPath = True

        return isPath
    
    def extractFileName(self, path):
        pathSplit = path.split('\\')
        fileName = pathSplit[len(pathSplit) - 1]

        return fileName
    
    def encodeArg(self, argumentsObj):
        arguments = 'Not Found'
        if functionName in argumentsObj:
            #print('function found')
            if (self.isPath(argumentsObj[functionName])):
                 fileName = self.extractFileName(argumentsObj[functionName])
                 argumentsObj[functionName] = fileName
            function = argumentsObj[functionName]
            if not function in self.functionNames:
                self.functionNames.append(function)
            arguments = function
        elif module_name in argumentsObj:
            #print('module found')
            if (self.isPath(argumentsObj[module_name])):
                 fileName = self.extractFileName(argumentsObj[module_name])
                 argumentsObj[module_name] = fileName
            module = argumentsObj[module_name]
            if not module in self.functionNames:
                self.functionNames.append(module)
            arguments = module
        
        return {module_name: arguments}

class File():
    category = 'File'
    apiCalls = []
    apiCallName = ''
    apiCallArguments = ''
    filePathMeaning = []
    fileMeaning = []

    def getCategory(self):
        return self.category


    def __init__(self, apiObj):
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def __init__(self):
        pass

    def encodeApi(self, apiObj):
        apiCallName = 'Not Found'
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def checkPath(self, filepath):
        firstPart = filepath.split('\\')[:2]
        firstPart = firstPart[0] + '\\' + firstPart[1]
        if not firstPart in self.filePathMeaning:
            self.filePathMeaning.append(firstPart)
        directory = firstPart
        print('directory: {}'.format(directory))
        fileExtension = 'Not Found'
        firstPart = filepath.split('\\')
        firstPart_1 = firstPart[len(firstPart) - 1]
        firstPart = firstPart_1.split('.')
        if str(filepath).find('.') > 0:
            # Checking if there is a file in the path
            if len(firstPart) > 1:
                possibleFileType = ''
                for extension in firstPart[1:]:
                    possibleFileType += '.{}'.format(extension)
                if not possibleFileType in self.fileMeaning and len(possibleFileType) >= 2:
                    self.fileMeaning.append(possibleFileType)
                fileExtension = possibleFileType

        return {'Directory': directory, 'FileExtension': fileExtension}

    def encodeArg(self, argumentsObj):
        arguments = {'Not Found'}

        if filepath in argumentsObj:
            path = argumentsObj[filepath]
            try:
                arguments = self.checkPath(path)
            except Exception as ex:
                print(ex)
        elif 'dirpath' in argumentsObj:
            path = argumentsObj['dirpath']
            try:
                arguments = self.checkPath(path)
            except Exception as ex:
                print(ex)
        
        return arguments


class Misc():
    category = 'MISC'
    apiCalls = []
    apiCallName = ''
    apiCallArguments = ''
    appearances = {}

    def getCategory(self):
        return self.category


    def __init__(self, apiObj):
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def __init__(self):
        self.appearances = {}

    def encodeApi(self, apiObj):
        apiCallName = 'Not Found'
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def encodeArg(self, argumentsObj):
        arguments = 0
        if self.apiCallName in self.appearances.keys():
            self.appearances[self.apiCallName] += 1
        else:
            self.appearances[self.apiCallName] = 1
        arguments = self.appearances[self.apiCallName]
        
        return {'Appearances': arguments}
    
    def clear(self):
        self.appearances = {}


class Synchronisation():
    category = 'sync'
    apiCalls = []
    apiCallName = ''
    apiCallArguments = ''
    appearances = {}

    def getCategory(self):
        return self.category


    def __init__(self, apiObj):
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def __init__(self):
        self.appearances = {}

    def encodeApi(self, apiObj):
        apiCallName = 'Not Found'
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def encodeArg(self, argumentsObj):
        arguments = 0
        if self.apiCallName in self.appearances.keys():
            self.appearances[self.apiCallName] += 1
        else:
            self.appearances[self.apiCallName] = 1
        arguments = self.appearances[self.apiCallName]
        
        return {'Appearances': arguments}
    
    def clear(self):
        self.appearances = {}

class Ui():
    category = 'UI'
    apiCalls = []
    apiCallName = ''
    apiCallArguments = ''

    def getCategory(self):
        return self.category


    def __init__(self, apiObj):
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)


    def __init__(self):
        pass

    def encodeApi(self, apiObj):
        apiCallName = 'Not Found'
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def encodeArg(self, argumentsObj):
        arguments = 'Not Found'
        if strings in argumentsObj:
            arguments =  [{'Strings': argumentsObj[strings]}]
            hasher = FeatureHasher(n_features=1, dtype=npy.ubyte)
            hashed_feature = hasher.transform(arguments).toarray()
            if hashed_feature[0][0] >= 256:
                hashed_feature[0][0] = 0
            arguments = {'Strings': hashed_feature[0][0]}
        
        return arguments

class Resource():
    category = 'Resource'
    apiCalls = []
    apiCallName = ''
    apiCallArguments = ''
    appearances = {}

    def getCategory(self):
        return self.category


    def __init__(self, apiObj):
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def __init__(self):
        self.appearances = {}

    def encodeApi(self, apiObj):
        apiCallName = 'Not Found'
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def encodeArg(self, argumentsObj):
        arguments = 0
        if self.apiCallName in self.appearances.keys():
            self.appearances[self.apiCallName] += 1
        else:
            self.appearances[self.apiCallName] = 1
        arguments = self.appearances[self.apiCallName]
        
        return {'Appearances': arguments}
    
    def clear(self):
        self.appearances = {}

class Crypto():
    category = 'Crypto'
    apiCalls = []
    apiCallName = ''
    apiCallArguments = ''
    appearances = {}

    def getCategory(self):
        return self.category


    def __init__(self, apiObj):
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def __init__(self):
        pass

    def encodeApi(self, apiObj):
        apiCallName = 'Not Found'
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def encodeArg(self, argumentsObj):
        arguments = 'Not Found'

        if algorithm_identifier in argumentsObj:
            print('Algorithm detected')
            algorithm = argumentsObj[algorithm_identifier]
            arguments = {'algorithm': algorithm}
        
        return arguments

class Network():
    category = 'Network'
    apiCalls = []
    apiCallName = ''
    apiCallArguments = ''
    appearances = {}

    def getCategory(self):
        return self.category


    def __init__(self, apiObj):
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def __init__(self):
        pass

    def encodeApi(self, apiObj):
        apiCallName = 'Not Found'
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def encodeArg(self, argumentsObj):
        arguments = {
            'hostname_communication': False,
            'used_port': "not found",
            'method': "not found",
            'post_data': "not found"
        }
        if 'hostname' in argumentsObj:
            arguments['hostname_communication'] = True
        if 'port' in argumentsObj:
            arguments['used_port'] = argumentsObj['port']
        if 'http_method' in argumentsObj:
            arguments['method'] = argumentsObj['http_method']
        if 'post_data' in argumentsObj:
            arguments['post_data'] = argumentsObj['post_data']

        return arguments

class Ole():
    category = 'OLE'
    apiCalls = []
    apiCallName = ''
    apiCallArguments = ''
    appearances = {}

    def getCategory(self):
        return self.category


    def __init__(self, apiObj):
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def __init__(self):
        self.appearances = {}

    def encodeApi(self, apiObj):
        apiCallName = 'Not Found'
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def encodeArg(self, argumentsObj):
        arguments = 0
        if self.apiCallName in self.appearances.keys():
            self.appearances[self.apiCallName] += 1
        else:
            self.appearances[self.apiCallName] = 1
        arguments = self.appearances[self.apiCallName]
        
        return {'Appearances': arguments}

    def clear(self):
        self.appearances = {}

class Services():
    category = 'Services'
    apiCalls = []
    apiCallName = ''
    apiCallArguments = ''
    services = []
    appearances = {}

    def getCategory(self):
        return self.category


    def __init__(self, apiObj):
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def __init__(self):
        pass

    def encodeApi(self, apiObj):
        apiCallName = 'Not Found'
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def encodeArg(self, argumentsObj):
        arguments = ''

        if service_name in argumentsObj:
            service = argumentsObj[service_name]
            if not service in self.services:
                self.services.append(service)
            arguments = service

        return {'serviceName': arguments}

class __notification__():
    category = 'Notification'
    apiCalls = []
    apiCallName = ''
    apiCallArguments = ''
    appearances = {}

    def getCategory(self):
        return self.category


    def __init__(self, apiObj):
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def __init__(self):
        self.appearances = {}

    def encodeApi(self, apiObj):
        apiCallName = 'Not Found'
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def encodeArg(self, argumentsObj):
        arguments = 0
        if self.apiCallName in self.appearances.keys():
            self.appearances[self.apiCallName] += 1
        else:
            self.appearances[self.apiCallName] = 1
        arguments = self.appearances[self.apiCallName]
        
        return {'Appearances': arguments}

    def clear(self):
        self.appearances = {}

class Certificate():
    category = 'Certificate'
    apiCalls = []
    apiCallName = ''
    apiCallArguments = ''
    appearances = {}

    def getCategory(self):
        return self.category


    def __init__(self, apiObj):
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def __init__(self):
        self.appearances = {}

    def encodeApi(self, apiObj):
        apiCallName = 'Not Found'
        if name in apiObj:
            apiCallName = apiObj[name]
            if apiCallName not in self.apiCalls:
                self.apiCalls.append(apiCallName)
        if arguments in apiObj:
            apiCallArguments = apiObj[arguments]
        
        self.apiCallName = apiCallName
        self.apiCallArguments = self.encodeArg(apiCallArguments)

    def encodeArg(self, argumentsObj):
        arguments = 0
        if self.apiCallName in self.appearances.keys():
            self.appearances[self.apiCallName] += 1
        else:
            self.appearances[self.apiCallName] = 1
        arguments = self.appearances[self.apiCallName]
        
        return {'Appearances': arguments}
    
    def clear(self):
        self.appearances = {}