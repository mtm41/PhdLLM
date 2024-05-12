from cgi import test
import sys
from Resnet import ResNetTypeI
from Resnet import ResNetTypeII
from sklearn.model_selection import KFold
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score
from matplotlib.colors import ListedColormap
from tensorflow.compat.v1.keras.models import Sequential
from tensorflow.compat.v1.keras.models import Model
from tensorflow.compat.v1.keras.layers import Conv2D
from tensorflow.compat.v1.keras.layers import MaxPooling2D
from tensorflow.compat.v1.keras.layers import GlobalAveragePooling2D
from tensorflow.compat.v1.keras.layers import Flatten
from tensorflow.compat.v1.keras.layers import Dropout
from tensorflow.compat.v1.keras.layers import Dense
from tensorflow.compat.v1.keras.optimizers import SGD
from tensorflow.compat.v1.keras.callbacks import ModelCheckpoint 
from sklearn.model_selection import KFold
from tensorflow.compat.v1.keras.applications import InceptionV3
import tensorflow.compat.v1 as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

class Trainer:

    def __init__(self, train_dataset, test_dataset, real_test_dataset):
        self.train = train_dataset
        self.test = test_dataset
        self.realtest = real_test_dataset
        

    # Using self defined model
    def modelDefinition(self, filters, filterSize, kernel, learningRate, x, y):
        print('Starting model definition')
        self.train.classes
        self.train.class_indices
        with tf.device("/gpu:0"):
            model = Sequential()

            # Defining filters of 3x3 for convulational layer
            # Using ReLU as activation function
            model.add(Conv2D(filters[0], filterSize, activation='relu', kernel_initializer=kernel, input_shape=(x, y, 3)))

            # Using MaxPooling for the pooling layer
            model.add(MaxPooling2D((2,2)))
            model.add(Conv2D(filters[1], filterSize, activation='relu', kernel_initializer=kernel))
            model.add(Conv2D(filters[2], filterSize, activation='relu', kernel_initializer=kernel))
            model.add(Conv2D(filters[3], filterSize, activation='relu', kernel_initializer=kernel))
            model.add(Conv2D(filters[4], filterSize, activation='relu', kernel_initializer=kernel))
            model.add(Conv2D(filters[5], filterSize, activation='relu', kernel_initializer=kernel))
            #model.add(Conv2D(filters[6], filterSize, activation='relu', kernel_initializer=kernel))
            model.add(MaxPooling2D((2,2)))

            # Flatten the model for obtaining features
            model.add(Flatten())
            model.add(Dropout(0.6)) # Maybe disable dropout, add kfold cross validation, random_state to 0?
            # Create a hidden fully connected layer with 100 nodes
            model.add(Dense(4096, activation='relu', kernel_initializer=kernel))
            model.add(Dense(2, activation='sigmoid'))

            # Compile model
            opt = SGD(lr=learningRate, momentum=0.9)
            model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])

            self.model = model

    # Using Google Inception pre-trained model
    def modelDefinitionInception(self, kernel, learningRate):
        print('Starting Inception V3 definition')
        base_model = InceptionV3(include_top=False, weights=None, input_shape=(30, 30, 3))

        x = base_model.output
        x = GlobalAveragePooling2D()(x)

        predictions = Dense(2, activation='softmax')(x)

        model = Model(inputs=base_model.input, outputs=predictions)
        opt = SGD(lr=learningRate, momentum=0.9)

        model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
        
        self.model = model

    # Using ResNet34 model (ResnetTypeI), but can implement other resnet types (ResNetTypeII)
    def modelDefinitionRestNet34(self, learningRate, layer_params):
        print('Starting ResNet34 definition')
        opt = SGD(lr=learningRate, momentum=0.9)
        model = ResNetTypeII(layer_params=layer_params)
        model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

        self.model = model

    def modelEvaluation(self, nFolds, matrix, classes, epochs):
        print('Starting model evaluation')
        scores, histories = list(), list()
        kfold = KFold(4, shuffle=True, random_state=1)
        
        #print(self.train.classes)
        #print(self.train.next())
        print("CLASES")
                    
        with open('testClasses1.txt', 'a') as testFile:
            for index in range(0, len(self.test.classes)):
                value = self.test.classes[index]
                testFile.write(str(value) + '\n')
        #print(self.test.next())
        # Defining callbacks in order to improve memory consumption
        callbacks = [
            ModelCheckpoint(
                filepath="D:\ckpy-{epoch}", save_freq="epoch"
            )
        ]
        if nFolds > 0:
            for train_index, test_index in kfold.split(self.train):
                print('starting k fold')
                print(train_index)
                print(test_index)
                print('showing dataset')
                print(self.train)
                x_train,x_test = self.train[train_index], self.train[test_index]
                y_train,y_test = self.test.values[train_index], self.test.values[test_index]
                history = self.model.fit(x_train, epochs=epochs, validation_data=y_train, verbose=1, shuffle=True)
                _, acc = self.model.evaluate(x_test, y_test, verbose=1)
                print('> %.3f' % (acc * 100.0))
        else:
            # steps per epoch = 2000
            history = self.model.fit(self.train, epochs=epochs, validation_data=self.test, verbose=1, shuffle=True)
            
            # Evaluate model
            #_, acc = self.model.evaluate(self.test, verbose=1)
            print(self.realtest)
            _, acc = self.model.evaluate(self.realtest, verbose=1)
            print('> %.3f' % (acc * 100.0))

            if (matrix):
                # Predict validation data
                #y_pred = self.model.predict_classes(self.test, verbose=1)
                y_pred = self.model.predict_classes(self.realtest, verbose=1)
                print('Predictions')
                with open('testPred1.txt', 'a') as testFile:
                    for index in range(0, len(y_pred)):
                        value = y_pred[index]
                        testFile.write(str(value) + '\n')
                print(y_pred)
                #print(self.test)
                
                labels = tf.constant(classes, dtype = tf.int32)
                predictions = tf.constant(y_pred, dtype = tf.int32)

                confMatrix = tf.math.confusion_matrix(predictions=y_pred, labels=self.realtest.classes)

                print("Confusion matrix")
                print(self.realtest.classes)
                print(confMatrix)
                print(confusion_matrix(self.realtest.classes, y_pred))
                

        print("Loss curve")

        history_dict = history.history
        print(history_dict)

        loss_values = history_dict['loss']
        val_loss_values = history_dict['val_loss']
        plt.plot(loss_values,'b', label='Training Loss')
        plt.plot(val_loss_values, 'r', label='Validation Loss')
        plt.title(label='Loss Curve')
        plt.show()
        print(history_dict)
        accuracy_values = history_dict['acc']
        val_accuracy_values = history_dict['val_acc']
        plt.plot(accuracy_values, 'b', label='Training Accuracy')
        plt.plot(val_accuracy_values, 'r', label='Validation Accuracy')
        plt.title(label='Accuracy Curve')
        plt.show()

        accuracy = history_dict['acc']
        val_accuracy = history_dict['val_acc']

        epochs = range(1, len(loss_values) + 1)
        fig, ax = plt.subplots(1, 2, figsize=(14, 6))
        #
        # Plot the model accuracy vs Epochs
        #
        ax[0].plot(epochs, accuracy, 'bo', label='Training accuracy')
        ax[0].plot(epochs, val_accuracy, 'b', label='Validation accuracy')
        ax[0].set_title('Training & Validation Accuracy', fontsize=16)
        ax[0].set_xlabel('Epochs', fontsize=16)
        ax[0].set_ylabel('Accuracy', fontsize=16)
        ax[0].legend()
        #
        # Plot the loss vs Epochs
        #
        ax[1].plot(epochs, loss_values, 'bo', label='Training loss') 
        ax[1].plot(epochs, val_loss_values, 'b', label='Validation loss')
        ax[1].set_title('Training & Validation Loss', fontsize=16)
        ax[1].set_xlabel('Epochs', fontsize=16)
        ax[1].set_ylabel('Loss', fontsize=16)
        ax[1].legend()
        #for train_ix, test_ix in kfold.split(self.train):
            # Fit model
            #history = self.model.fit(train)

        


    def visualizeResults(self):
        X_set, y_set = self.X_test, self.Y_test
        X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
        plt.contourf(X1, X2, self.classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
                    alpha = 0.75, cmap = ListedColormap(('red', 'green', 'blue', 'brown')))
        plt.xlim(X1.min(), X1.max())
        plt.ylim(X2.min(), X2.max())
        for i, j in enumerate(np.unique(y_set)):
            plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                            c = ListedColormap(('red', 'green', 'blue', 'brown'))(i), label = j)
        plt.title('SVM (Test set)')
        plt.xlabel('Pe_imports')
        plt.ylabel('File_read')
        plt.legend()
        plt.show()

    def visualize(self):
        print('Printing Results...')
        plt.scatter(self.X_train[:,0], self.X_train[:,1])
        support_vector_indices = self.classifier.support_
        print('Vector indices {}'.format(support_vector_indices))
        support_vectors_per_class = self.classifier.n_support_
        support_vectors = self.classifier.support_vectors_
        print('Using {} features per class'.format(support_vectors_per_class))
        plt.scatter(support_vectors[:,0], support_vectors[:,1], color='red')
        plt.title('SVM with pe_imports and file_read features')
        plt.xlabel('pe_imports')
        plt.ylabel('file_read')
        plt.show()


