import numpy as np
import sys, time, glob, os, ntpath, cv2
from skimage.feature import hog
import pickle
import pandas as pd

def featureExtraction(img, PLOT = False):
    #start = time.clock()

    #blocks = blockshaped(img)

    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.resize(img, (700, 500))
    scale_cell = (16, 16)#(img.shape[0]//100, img.shape[1]//100) # (32, 32)
    #crop_img = img[y:y+h, x:x+w]
    fHOG1 = hog(img, orientations=8, pixels_per_cell=scale_cell)
    namesHOG = ['hog']
    #print(scale_cell, (img.shape[0], img.shape[1]), 'len', len(fHOG1))

    #t6 = time.clock();

    #print("Total time: {0:.2f}".format(t6-start))

    fv = fHOG1
    fNames = namesHOG

    return fv, fNames


def getFeaturesFromFile(fileName, PLOT = False):
    img = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)  #cv2.IMREAD_COLOR)    # read image
    #print(img.shape)
    [F, N] = featureExtraction(img, PLOT)            # feature extraction
    return F#, N

if __name__ == '__main__':
    from sklearn.linear_model import SGDClassifier
    from sklearn.neighbors.nearest_centroid import NearestCentroid
    from sklearn.neighbors import KNeighborsClassifier
    #clf = SGDClassifier(loss="hinge", penalty="l2")

    new_dataset=0

    if new_dataset:
        dataset_directory = r'C:\Users\Jiravat\Desktop\git\DocKeeper\documentClassification\dataset' #r'D:\dataset\rvl-cdip\images'
        X = []
        y = []
        num_train = 2112#2106#363
        train = open('train_clean.txt')
        for i in range(num_train):
            line = train.readline()
            path, category = line.split()
            print(i, path)
            hog_feature = getFeaturesFromFile(os.path.join(dataset_directory, path))
            #print(hog_feature.shape)
            X.append(hog_feature)
            y.append(category)
            #clf.partial_fit(hog_feature, category)

        X = np.array(X)
        y = np.array(y)

        with open('X.pickle', 'wb') as handle:
            pickle.dump(X, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open('y.pickle', 'wb') as handle:
            pickle.dump(y, handle, protocol=pickle.HIGHEST_PROTOCOL)

    else:
        with open('X.pickle', 'rb') as handle:
            X = pickle.load(handle)
        with open('y.pickle', 'rb') as handle:
            y = pickle.load(handle)

    from sklearn.model_selection import train_test_split
    # from sklearn import cross_validation
    X_train_data, X_test_data, y_train_data, y_test_data = train_test_split(X, y, test_size=0.3,
                                                                         stratify=y)
    # print(X_train, X_test, y_train, y_test)
    num_test = len(y_test_data)
    print('x.shape', X.shape)
    print('train size:', len(y_train_data))
    print('test size', num_test)
    print('train class count:', len(np.unique(y_train_data)))
    print('test class count:', len(np.unique(y_test_data)))
    # break
    k_fold_tune=0
    if k_fold_tune:
        from sklearn.model_selection import KFold
        from sklearn.metrics import f1_score
        kf = KFold(n_splits=5)
        print('kf.get_n_splits', kf.get_n_splits(X_train_data))
        kf_round_i = 0
        alphas = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1e0, 1e1]  # learning rate
        n_neighbors_list=[1,2,3,4,5,6]
        sgd_eval = []
        nearestcentroid_eval = []
        knear_eval = []
        for train_index, test_index in kf.split(X_train_data):
            X_train, X_test = X_train_data[train_index], X_train_data[test_index]
            y_train, y_test = y_train_data[train_index], y_train_data[test_index]

            alphas_score = []
            for alpha in alphas:
                print('_________sgd________alpha',alpha)
                start = time.clock()

                sgd = SGDClassifier(alpha=alpha)
                sgd.fit(X_train, y_train)
                predict_y = sgd.predict(X_test)
                print("Total time: {0:.2f}".format(time.clock()-start))

                f1Score = f1_score(y_test, predict_y, average='macro')
                print(f1Score)  #F1 Score = 2*(Recall * Precision) / (Recall + Precision)
                alphas_score.append(f1Score)
            max_alphas_score = max(alphas_score)
            max_alphas = alphas[alphas_score.index(max_alphas_score)]
            print(alphas_score, max_alphas_score, max_alphas)
            sgd_eval.append(alphas_score)

            print('_________NearestCentroid________')
            start = time.clock()
            nearestCentroid = NearestCentroid()
            nearestCentroid.fit(X_train, y_train)

            predict_y = nearestCentroid.predict(X_test)
            print("Total time: {0:.2f}".format(time.clock()-start))

            f1Score = f1_score(y_test, predict_y, average='macro')
            print(f1Score)
            nearestcentroid_eval.append([f1Score])

            n_neighbors_list_score = []
            for n_neighbor in n_neighbors_list:
                print('_________KNeighborsClassifier________')
                start = time.clock()
                kneighbors = KNeighborsClassifier(n_neighbors=n_neighbor)
                kneighbors.fit(X_train, y_train)
                predict_y = kneighbors.predict(X_test)
                print("Total time: {0:.2f}".format(time.clock()-start))

                f1Score = f1_score(y_test, predict_y, average='macro')
                print(f1Score)
                n_neighbors_list_score.append(f1Score)
            max_n_neighbors_list_score = max(n_neighbors_list_score)
            max_n_neighbors = n_neighbors_list[n_neighbors_list_score.index(max_n_neighbors_list_score)]
            print(n_neighbors_list_score, max_n_neighbors_list_score, max_n_neighbors)
            knear_eval.append(n_neighbors_list_score)

            kf_round_i+=1
            print('------------end'*2,kf_round_i,'------------'*2)
            print('------------end'*2,kf_round_i,'------------'*2)

        sgd_eval = np.asarray(sgd_eval)
        np.savetxt("sgd_eval.csv", sgd_eval, delimiter=",")
        knear_eval = np.asarray(knear_eval)
        np.savetxt("knear_eval.csv", knear_eval, delimiter=",")
        nearestcentroid_eval = np.asarray(nearestcentroid_eval)
        np.savetxt("nearestcentroid_eval.csv", nearestcentroid_eval, delimiter=",")

    test_acc=1
    if test_acc:
        from sklearn.metrics import f1_score
        sgd_score=[]
        nearestcentroid_score=[]
        kneighbors_score=[]
        n_round=10
        for round_i in range(1, n_round+1):
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=round_i,
                                                                                    stratify=y)
            print('_________sgd________round_',round_i)
            start = time.clock()

            sgd = SGDClassifier(alpha=1e-5)
            sgd.fit(X_train, y_train)
            predict_y = sgd.predict(X_test)
            print("Total time: {0:.2f}".format(time.clock()-start))

            f1Score = f1_score(y_test, predict_y, average='macro')
            print(f1Score)  #F1 Score = 2*(Recall * Precision) / (Recall + Precision)
            sgd_score.append(f1Score)

            print('_________NearestCentroid________round_', round_i)
            start = time.clock()
            nearestCentroid = NearestCentroid()
            nearestCentroid.fit(X_train, y_train)

            predict_y = nearestCentroid.predict(X_test)
            print("Total time: {0:.2f}".format(time.clock()-start))

            f1Score = f1_score(y_test, predict_y, average='macro')
            print(f1Score)
            nearestcentroid_score.append(f1Score)

            print('_________KNeighborsClassifier________round_', round_i)
            start = time.clock()
            kneighbors = KNeighborsClassifier(n_neighbors=1)
            kneighbors.fit(X_train, y_train)
            predict_y = kneighbors.predict(X_test)
            print("Total time: {0:.2f}".format(time.clock()-start))

            f1Score = f1_score(y_test, predict_y, average='macro')
            print(f1Score)
            kneighbors_score.append(f1Score)

        round_score = [[sgd_score[i], nearestcentroid_score[i], kneighbors_score[i]]for i in range(n_round)]
        round_score = np.asarray(round_score)
        np.savetxt("round_score.csv", round_score, delimiter=",")
