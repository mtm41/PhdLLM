import numpy as np
import tensorflow as tf
import pathlib
from scipy import misc

class LoaderDataFromImg:

    def __init__(self, batch_size, imagesPathTrain, imagesPathValidation, imagesPathTest, classes, x, y):
        self.batch_size = batch_size
        #imagesPath = pathlib.Path(imagesPath)
        #train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        #    './images2',
        #    labels='inferred')
            #validation_split=0.2,
            #subset='training',
            #seed=123,
            #image_size=(327,327),
            #batch_size=self.batch_size)
        #train_ds = np.asarray(train_ds.as_numpy_iterator())
        #print(train_ds.shape[0])
        #train_ds = train_ds.reshape(-1, 327, 327, 1)
        #print(train_ds)

        datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
        #datagen = tf.keras.preprocessing.image.ImageDataGenerator()
        self.train_it = datagen.flow_from_directory(imagesPathTrain, classes=classes, target_size=(x,y), shuffle=True, color_mode='rgb', class_mode='categorical')
        self.test_it = datagen.flow_from_directory(imagesPathValidation, classes=classes, target_size=(x,y), shuffle=False, color_mode='rgb', class_mode='categorical')
        self.real_test_it = datagen.flow_from_directory(imagesPathTest, classes=classes, target_size=(x,y), shuffle=False, color_mode='rgb', class_mode='categorical')


    def getTrainDataset(self):
        return self.train_it

    def getTestDataset(self):
        return self.test_it

    def getRealTestDataset(self):
        return self.real_test_it

    def createBatches(self):
        while (True):
            for i in range(0, total, self.batch_size):
                yield(self.images[i:i+batch_size], self.classes[i:i+batch_size])

        print(self.images)
        print(self.classes)

