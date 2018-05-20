import numpy as np
import sys, time, glob, os, ntpath, cv2, numpy
from skimage.feature import hog

def featureExtraction(img):
    start = time.clock()


    #blocks = blockshaped(img)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (700, 500))
    scale_cell = (16, 16)#(img.shape[0]//100, img.shape[1]//100) # (32, 32)
    #crop_img = img[y:y+h, x:x+w]
    fHOG1 = hog(img, orientations=8, pixels_per_cell=scale_cell)
    namesHOG = ['hog']
    print(scale_cell, (img.shape[0], img.shape[1]), 'len', len(fHOG1))

    t6 = time.clock()

    print("Total time: {0:.2f}".format(t6-start))

    fv = fHOG1
    fNames = namesHOG

    return fv, fNames

def getFeaturesFromFile(fileName, PLOT = False):
    img = cv2.imread(fileName, cv2.IMREAD_COLOR)    # read image
    [F, N] = featureExtraction(img)            # feature extraction
    return F

if __name__ == '__main__':
    from sklearn.linear_model import SGDClassifier #16/16
    from sklearn.neighbors.nearest_centroid import NearestCentroid # 15/16
    from sklearn.neighbors import KNeighborsClassifier #11/16
    #clf = SGDClassifier(loss="hinge", penalty="l2")
    clf = SGDClassifier()
    dataset_directory = r'C:\Users\Jiravat\Desktop\git\DocKeeper\documentClassification\dataset' #r'D:\dataset\rvl-cdip\images'
    train_x = []
    train_y = []
    num_train = 271#271
    train = open('train1.txt')
    for _ in range(num_train):
        line = train.readline()
        path, category = line.split()
        print(path)
        hog_feature = getFeaturesFromFile(os.path.join(dataset_directory, path))
        train_x.append(hog_feature)
        train_y.append(category)
        #clf.partial_fit(hog_feature, category)

    clf.fit(train_x, train_y)

    test_x = []
    test_y = []
    num_test = 16
    correct = 0
    test = open('test1.txt')
    for _ in range(num_test):
        line = test.readline()
        path, category = line.split()
        test_x.append(getFeaturesFromFile(os.path.join(dataset_directory, path), False))
        test_y.append(category)

    predict_y = clf.predict(test_x)
    correct=0
    for i in range(num_test):
        if test_y[i] == predict_y[i]:
            correct+=1
    print(correct, '/', num_test)
    print(test_y)
    print(predict_y)