import requests as req
import os
import tiktoken
import random
from openai import OpenAI

batchSize = 20 # 20 API calls will be sent to GPT in each request
modifiedAPICallPercentage = 0.1 # Percentage of API calls 

def convertApiToTokens(apiCall):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(apiCall)

    return tokens

def chooseBatches(apiBatchesPerReport):
    nBatches = len(apiBatchesPerReport)
    print('The report has been divided in {} batches'.format(nBatches))

    neededBatches = int(nBatches * modifiedAPICallPercentage)
    print('Needed {} batches'.format(neededBatches))
    chosenIds = []
    
    while(len(chosenIds) < neededBatches):
        randomBatchID = random.randrange(nBatches)
        while(randomBatchID in chosenIds):
            randomBatchID = random.randrange(nBatches)
        chosenIds.append(randomBatchID)

    print('Chosen IDs: {}'.format(chosenIds))
    return chosenIds

def gptModify(apiBatch):
    
    client = OpenAI(
        api_key="secret"
    )
    print(str(apiBatch))
    models = ['gpt-3.5-turbo', 'gpt-4-turbo-preview']
    orders = ["As an assistant, your task is to adjust the system API calls provided by the user. The objective is to maintain the functionality of the original calls while utilizing different API functions, arguments, or order. Remember to adhere to the format: <category of system API call>,<system API call name>,<system API arguments>. Ensure that you employ real Windows system API calls in the same format and use the same keys for the arguments, do not add new keys.",
              "You are a transcriptor which translate batches of Windows system API calls to other set of Windows API system calls that achieve the same purpose. You must follow the format that the user uses for specifying the system API calls, which is category,api,\{arguments\}. Arguments are represented in a JSON object, you are not allowed to change the used keys in the object."]
    try:
        response = client.chat.completions.create(
            model=models[0],
            
            # Idea, use an example of response
            # {
            #        "role": "user",
            #        "content": "System,LdrLoadDll,{\"module_name\": \"ADVAPI32.dll\"}\n"
            #    }
                
            messages=[
                {
                    "role": "system",
                    "content": orders[0]
                },
                {
                    "role": "user",
                    "content": str(apiBatch)
                }
            ]
        )
        apiBatch = response.choices[0].message.content
    except Exception as Ex:
        print(Ex)

    return apiBatch

def convertToApiBatchFormat(apiBatch):
    newApiBatch = []
    splitApiBatch = apiBatch.split('\'')[1:]
    for splitApi in splitApiBatch:
        if len(splitApi) > 5: 
            apiFormatted = splitApi.replace('\\n', '')
            print('Adding {}'.format(apiFormatted))
            newApiBatch.append(apiFormatted)

    return newApiBatch    

summarizedReportsPath = './testSummarized'
modifiedReportsPath = './modified'

tokenSum = 0
fileCount = 0
apiCount = 0
for summarizedReportFile in os.listdir(summarizedReportsPath):
    apiBatchesPerReport = []
    with open(summarizedReportsPath + '/' + summarizedReportFile, 'r') as summarizedReport:
        apiBatch = []
        fileCount += 1
        apiCall = summarizedReport.readline()
        while (apiCall):
            apiCount += 1
            apiBatch.append(apiCall)
            # ApiBatch is full, add it to the hash table and empty
            if (apiCount % batchSize == 0):
                apiBatchesPerReport.append(apiBatch)
                apiBatch = []
            #print(apiCall)
            apiCall = summarizedReport.readline()
            apiCallEncoded = convertApiToTokens(apiCall)        
            #print('Number of tokens: {}'.format(len(apiCallEncoded)))
            tokenSum += len(apiCallEncoded)
        chosenIDBatchesToSendToGPT = chooseBatches(apiBatchesPerReport)
        with open(modifiedReportsPath + '/' + summarizedReportFile, 'a') as modifiedReportFile:
            i = 0
            for apiBatch in apiBatchesPerReport:
                if i in chosenIDBatchesToSendToGPT:
                    print('Batch {} needs to be sent to GPT for its modification!'.format(i))
                    tokens = convertApiToTokens(str(apiBatch))
                    print('Sending {} tokens'.format(len(tokens)))
                    modifiedBatch = gptModify(apiBatch)
                    apiBatch = modifiedBatch
                    print('\n')
                    print(apiBatch)
                    apiBatch = convertToApiBatchFormat(apiBatch)
                    for api in apiBatch:
                        print(api)
                        print(type(api))
                        modifiedReportFile.writelines(api + '\n')
                else:
                    for api in apiBatch:
                        print(api)
                        print(type(api))
                        modifiedReportFile.writelines(api)
                i += 1
median = tokenSum / fileCount
medianPerApi = tokenSum / apiCount
print('Median for {} files is: {}'.format(fileCount, median)) 
print('Median per API in {} calls is: {}'.format(apiCount, medianPerApi))