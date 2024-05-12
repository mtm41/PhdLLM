#from Loader import Loader
from LoaderDataFromImg import LoaderDataFromImg
from Trainer import Trainer
import sys, getopt
import os
import tensorflow as tf

def main(model):

    # Constraints
    #TEST_SIZE = 0.35
    FILTERS = [32, 64, 128, 256, 512, 1024, 2048]
    FILTER_SIZE = (2, 2)
    # Probar 0.1
    LEARNING_RATE = 0.0001
    RANDOM_STATE = 0
    N_FOLDS = 0
    KERNEL = 'he_uniform'
    LAYER_PARAMS = [2, 2, 2, 2]
    #CLASSES = ["APT", "Crypto", "Locker", "Ransomware", "Shadowbrokers", "Trojan"]
    #CLASSES_IDS = [0, 1, 2, 3, 4, 5]
    CLASSES = ["MALWARE", "BENIGN"]
    CLASSES_IDS = [1, 0]
    EPOCHS = 100
    X = 30
    Y = 30
    imagesPathTrain = 'D:\\repos\\conv2D-malware\\convertReportsToImages\\images\\Second_Dataset\\KFOLD5\\Training'
    imagesPathValidation = 'D:\\repos\\conv2D-malware\\convertReportsToImages\\images\\Second_Dataset\\KFOLD5\\Testing'
    imagesPathTest = 'D:\\repos\\conv2D-malware\\convertReportsToImages\\images\\Second_Dataset\\Test'
    #imagesPathTrain = 'D:\\repos\\conv2D-malware\\convertReportsToImages\\images1\\very_good_dataset\\Training'
    #imagesPathValidation = 'D:\\repos\\conv2D-malware\\convertReportsToImages\\images1\\very_good_dataset\\Testing'

    print("Extracting data from images to train Model")
    loaderDataFromImg = LoaderDataFromImg(1, imagesPathTrain, imagesPathValidation, imagesPathTest, CLASSES, X, Y)
 
    # Prepare the dataset for training
    print("Preparing for training...")
    trainer = Trainer(loaderDataFromImg.getTrainDataset(), loaderDataFromImg.getTestDataset(), loaderDataFromImg.getRealTestDataset())
    matrix = True
    if (model == 'Resnet'):
        trainer.modelDefinitionRestNet34(LEARNING_RATE, LAYER_PARAMS)
        matrix = False
    elif (model == 'Inception'):
        print('Loading Inception')
        trainer.modelDefinitionInception(KERNEL, LEARNING_RATE)
    elif (model == 'Normal'):
        trainer.modelDefinition(FILTERS, FILTER_SIZE, KERNEL, LEARNING_RATE, X, Y)

    # Evaluate defined model
    trainer.modelEvaluation(N_FOLDS, matrix, CLASSES_IDS, EPOCHS)
    
    #if (visualize == True):
    #    trainer.visualizeResults()


def buildLabelVector(classes):
    labelVector = []
    for label in classes.keys():
        interval = classes[label]
        start_interval = int(interval.split("-")[0])
        end_interval = int(interval.split("-")[1])

        while (start_interval <= end_interval):
            labelVector.append(label)
            start_interval += 1

    return labelVector

if __name__ == '__main__':
    model = ''
    try:
        args, opts = getopt.getopt(sys.argv,"hi:o", ["--model="])
    except getopt.GetoptError:
        print('Main.py -m <model>')
        sys.exit(2)
    
    count = 0
    for opt in opts:
        if opt == '-h':
            print('Main.py -m <model>')
            sys.exit()
        elif opt in ("-m", "--model"):
            model = opts[count + 1]
        count += 1

    main(model)
