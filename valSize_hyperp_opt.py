import random
import os
import cv2
import glob
# import gdcm
import numpy as np
import pandas as pd
# import seaborn as sns
import matplotlib.pyplot as plt


# from tqdm.notebook import tqdm
# from joblib import Parallel, delayed

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras

modelName = 'ValSize_opt'


"""
test = cv2.imread('resources/10006_1459541791.png')
test2 = cv2.imread('resources/10006_462822612.png')
plt.imshow(test)
plt.show()
plt.imshow(test2)
plt.show()
"""

df = pd.read_csv('train.csv')
#dfCC = df[df['view'] == 'CC']
#dfCC = dfCC.reset_index()

#dfMLO = df[df['view'] == 'MLO']
#dfMLO = dfMLO.reset_index()

# X_train = np.array([ cv2.imread(f'resources/{dfCC["patient_id"][i]}_{dfCC["image_id"][i]}.png') for i in dfCC.index ])
# y_train = np.array(dfCC['cancer'].to_list())

# Xy_balanced = [ (cv2.imread(f'resources/{dfCC["patient_id"][i]}_{dfCC["image_id"][i]}.png'), dfCC['cancer'][i]) for i in dfCC.index ]

# Xy_balanced = [ (cv2.imread(f'resources/{dfMLO["patient_id"][i]}_{dfMLO["image_id"][i]}.png'), dfCC['cancer'][i]) for i in dfCC.index ]

Xy_balanced = [ (cv2.imread(f'resources/{df["patient_id"][i]}_{df["image_id"][i]}.png'), df['cancer'][i]) for i in df.index ]


valSize=[100,1000,2000]

train_acc = []
val_acc = []

for i in valSize:
    X_val = [ x[0] for x in Xy_balanced[:i] ]
    y_val = [ x[1] for x in Xy_balanced[:i] ]
    Xy_balanced = Xy_balanced[i:]
    nCancer = len([ i for i in Xy_balanced if i[1] == 1])
    print(len(Xy_balanced))
    while nCancer/len(Xy_balanced) < 0.4 :
        nL = Xy_balanced.copy()
        for x in Xy_balanced:
            if x[1] == 1:
                nL.append(x)
        Xy_balanced = nL.copy()
        nCancer = len([ i for i in Xy_balanced if i[1] == 1])

    print(len(Xy_balanced))

    random.shuffle(Xy_balanced)

    X_trainL = [ x[0] for x in Xy_balanced ]
    y_trainL = [ x[1] for x in Xy_balanced ]

    X_train = X_trainL[:2000]
    y_train = y_trainL[:2000]

    X_train = np.array(X_train)
    y_train = np.array(y_train)


    # X_val = np.array(X_trainL[60000:])
    # y_val = np.array(y_trainL[60000:])

    X_val = np.array(X_val)
    y_val = np.array(y_val)



    model = keras.models.Sequential([
        keras.layers.Input([256, 256, 3]),
        keras.layers.Conv2D(50, 3, activation="relu"),
        keras.layers.MaxPooling2D(pool_size=2),
        keras.layers.BatchNormalization(),
        keras.layers.Conv2D(40, 3, activation="relu"),
        keras.layers.BatchNormalization(),
        keras.layers.Flatten(),
        keras.layers.Dense(2, activation="softmax")
    ])

    model.summary() 

    model.compile(loss="sparse_categorical_crossentropy",
                optimizer=keras.optimizers.legacy.Adam(),
                metrics=["accuracy"])

    history = model.fit(X_train, y_train, epochs=5, batch_size=4,
                        validation_data=(X_val, y_val))

    train_acc.append(history.history['accuracy'])
    val_acc.append(history.history['val_accuracy'])

plt.figure()
for i in range(len(train_acc)):
    plt.plot(train_acc[i], label=f'train acc (ValSize=%d%%)' % (valSize[i]/2000))
    plt.plot(val_acc[i], label=f'val acc (ValSize=%d%%)' % (valSize[i]/2000))
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Training and Validation Accuracy')
plt.savefig('accuracy_plot.png')
plt.show()



'''
X_train = X_trainL[20000:40000]
y_train = y_trainL[20000:40000]
X_train = np.array(X_train)
y_train = np.array(y_train)


history2 = model.fit(X_train, y_train, epochs=5, batch_size=4, 
        validation_data=(X_val, y_val))

model.save(f'{modelName}-2')
print(history2)

X_train = X_trainL[40000:]
y_train = y_trainL[40000:]
X_train = np.array(X_train)
y_train = np.array(y_train)


history3 = model.fit(X_train, y_train, epochs=5, batch_size=4, 
        validation_data=(X_val, y_val))

model.save(f'{modelName}-3')
print(history3)

pd.DataFrame(history.history).plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1)
plt.savefig("keras_learning_curves_plot.png")
plt.show()

pd.DataFrame(history2.history).plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1)
plt.savefig("keras_learning_curves_plot2.png")
plt.show()

pd.DataFrame(history3.history).plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1)
plt.savefig("keras_learning_curves_plot3.png")
plt.show()

'''