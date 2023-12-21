import time
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score
import numpy as np
import sys
import json
#np.set_printoptions(threshold=sys.maxsize)



class Classifier:

    def __init__(self, subsets):
        self.subsets = subsets

    def prep_data(self, task):
        print(f"---------------- Task {task} ----------------")
        # Task_i is when subset_i is used as test set and the others as training set
        X_train = []
        y_train = []
        X_test = []
        y_test = []
        for i in range(5):
            if i == task - 1:
                for vector in self.subsets[i]:
                    X_test.append(vector[:-1])
                    y_test.append(vector[-1:])
            else:
                for vector in self.subsets[i]:
                    X_train.append(vector[:-1])
                    y_train.append(vector[-1:])

        X_train = np.array(X_train, dtype=int)
        y_train = np.array(y_train, dtype=int).ravel()
        X_test = np.array(X_test, dtype=int)
        y_test = np.array(y_test, dtype=int).ravel()
        
        return X_train, y_train, X_test, y_test


    def classifyKNN(self, k):
        """Classify a vector using the k-NN classifier"""
        print(f"---------------- KNN classifier with k = {k} ----------------")

        # Init KNN classifier
        clf_knn = KNeighborsClassifier(n_neighbors=k)         

        # Prepare data for training and testing
        total_time = 0
        for task in range(1, 6): # Task 1 to 5
            X_train, y_train, X_test, y_test = self.prep_data(task)
        
            # Train with KNN classifier
            print("Training . . .")
            print(f"X_train : {X_train}")
            print(f"y_train : {y_train}")

            start_time = time.time()
            clf_knn.fit(X_train, y_train)
            end_time = time.time()
            time_diff = end_time - start_time
            total_task_time = time_diff
            print(f"Train done in {time_diff} seconds \n")

            # Predict with KNN classifier
            print("Predicting . . .")
            print(f"X_test : {X_test}")
            print(f"y_test : {y_test}")

            start_time = time.time()
            y_pred = clf_knn.predict(X_test)
            end_time = time.time()
            time_diff = end_time - start_time
            total_task_time += time_diff
            print(f"Prediction : {y_pred}")
            print(f"Predict done in {time_diff} seconds \n")

            print(f"Task {task} ended in {total_task_time} seconds")

            # Evaluate the KNN classifier
            print("Evaluating . . .")
            PREC_knn = precision_score(y_test, y_pred, average='macro')
            REC_knn = recall_score(y_test, y_pred, average='macro')
            F1_knn = f1_score(y_test, y_pred, average='macro')
        
            print(f"Precision : {PREC_knn}")
            print(f"Recall : {REC_knn}")
            print(f"F1 score : {F1_knn} \n")

            total_time += total_task_time
        
        print(f"All tasks ended in {total_time} seconds")

    def classifyMNB(self):
        """Classify a vector using Multinoial Naive Bayes classifier"""
        print("---------------- Multinomial Naive Bayes classifier ----------------")

        # Init Multinomial Naive Bayes classifier
        clf_mnb = MultinomialNB()

        # Prepare data for training and testing
        total_time = 0
        for task in range(1, 6):
            X_train, y_train, X_test, y_test = self.prep_data(task)

            # Train with Multinomial Naive Bayes classifier
            print("Training . . .")
            print(f"X_test : {X_test}")
            print(f"y_test : {y_test}")
            
            start_time = time.time()
            clf_mnb.fit(X_train, y_train)
            end_time = time.time()
            time_diff = end_time - start_time
            total_task_time = time_diff
            print(f"Train done in {time_diff} seconds \n")

            # Predict with Multinomial Naive Bayes classifier
            print("Predicting . . .")
            print(f"X_test : {X_test}")
            print(f"y_test : {y_test}")
            
            start_time = time.time()
            y_pred = clf_mnb.predict(X_test)
            end_time = time.time()
            time_diff = end_time - start_time
            total_task_time += time_diff
            print(f"Prediction : {y_pred}")
            print(f"Predict done in {time_diff} seconds \n")

            print(f"Task {task} ended in {total_task_time} seconds")

            # Evaluate the Multinomial Naive Bayes classifier
            print("Evaluating . . .")
            PREC_knn = precision_score(y_test, y_pred, average='macro')
            REC_knn = recall_score(y_test, y_pred, average='macro')
            F1_knn = f1_score(y_test, y_pred, average='macro')
        
            print(f"Precision : {PREC_knn}")
            print(f"Recall : {REC_knn}")
            print(f"F1 score : {F1_knn} \n")

            total_time += total_task_time

        print(f"All tasks ended in {total_time} seconds")

        print(y_pred)

    def predict_attack(self, training_vectors, testing_vectors, classifier, k=4):
        """Predict if a vector is an attack or not"""

        # Prepare data for training and testing
        X_train = []
        y_train = []
        X_test = []

        for vector in training_vectors:
            X_train.append(vector[:-1])
            y_train.append(vector[-1:])
        for vector in testing_vectors:
            X_test.append(vector[:-1])

        X_train = np.array(X_train, dtype=int)
        y_train = np.array(y_train, dtype=int).ravel()
        X_test = np.array(X_test, dtype=int)

        print("- Number of training vectors : ", len(X_train))
        print("- First vector of the training vectors : \n", X_train[0])

        print("- Number of training labels : ", len(y_train))
        print("- Label of the training labels : \n", y_train)

        print("- Number of testing vectors : ", len(X_test))
        print("- First vector of the testing vectors : \n", X_test[0])

        # KNN classifier
        if classifier == "KNN":
            print(f"---------------- KNN classifier with k = {k} ----------------")
            # Init KNN classifier
            clf_knn = KNeighborsClassifier(n_neighbors=k)

            print("-------------------- Training --------------------")
            # Train with KNN classifier
            start_timer = time.time()
            clf_knn.fit(X_train, y_train)
            end_timer = time.time()
            time_diff = end_timer - start_timer
            print(f"Train done in {time_diff} seconds \n")

            print("------------------- Predicting -------------------")
            print("CAUTION : This may take a while (30MIN ~ 1H) . . . ")
            date_time = time.localtime()
            date_time = f"{date_time.tm_hour}:{date_time.tm_min}:{date_time.tm_sec}"
            print("Started at " + date_time)
            # Predict with KNN classifier
            start_timer = time.time()
            proba = clf_knn.predict_proba(X_test)
            end_timer = time.time()
            time_diff = end_timer - start_timer
            print(f"Predict done in {time_diff} seconds \n")
            print(f"Order : {clf_knn.classes_}")
            print(f"Probabilities : {proba}")

            return proba
        
        elif classifier == "MNB":
            print("---------------- Multinomial Naive Bayes classifier ----------------")
            # Init Multinomial Naive Bayes classifier
            clf_mnb = MultinomialNB()

            print("-------------------- Training --------------------")
            # Train with Multinomial Naive Bayes classifier
            start_timer = time.time()
            clf_mnb.fit(X_train, y_train)
            end_timer = time.time()
            time_diff = end_timer - start_timer
            print(f"Train done in {time_diff} seconds \n")


            print("------------------- Predicting -------------------")
            date_time = time.localtime()
            date_time = f"{date_time.tm_hour}:{date_time.tm_min}:{date_time.tm_sec}"
            print("Started at " + date_time)
            # Predict with Multinomial Naive Bayes classifier
            start_timer = time.time()
            proba = clf_mnb.predict_proba(X_test)
            end_timer = time.time()
            time_diff = end_timer - start_timer
            print(f"Predict done in {time_diff} seconds \n")
            print(f"Order : {clf_mnb.classes_}")
            print(f"Probabilities : {proba}")

            return proba

    def make_json_res(self, proba, method, appName):
        """Make a json file with the results"""
        print("---------------- Making json file ----------------")

        json_res = {"preds": [], "probs": [], "names": []}
        for i in range(len(proba)):
            if proba[i][0] > proba[i][1]:
                json_res["preds"].append("Normal")
                json_res["probs"].append(proba[i].tolist())
            elif proba[i][0] <= proba[i][1]:
                json_res["preds"].append("Attack")
                json_res["probs"].append(proba[i].tolist())

        names = ["DENOUE", "QUERE"]
        version = 1
        json_res["names"] = names
        json_res["method"] = method
        json_res["appName"] = appName
        json_res["version"] = version
        
        # Write json file
        with open(f"defi1/res/{names[0]}_{names[1]}_{appName}_{version}.json", "w") as f:
            json.dump(json_res, f, indent=4)
        return json_res






