import time
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import numpy as np


class KNNClassifier:
    """k-NN classifier, binary version, implemented in the sklearn Python library"""

    def __init__(self, subsets):
        self.subsets = subsets

    def classifyKNN(self, k):
        """Classify a vector using the k-NN classifier"""


        # Init KNN classifier
        clf_knn = KNeighborsClassifier(n_neighbors=k)
        print(len(self.subsets), len(self.subsets[0]), len(self.subsets[0][0]))
        for i in range(len(self.subsets[0])):
            if len(self.subsets[0][i]) != 159:
                print(len(self.subsets[0][i]))
        X = np.array(self.subsets[0], dtype=int).reshape(len(self.subsets[0]), 159)
        y = np.array([0] * len(self.subsets[0]), dtype=int)

        X_test = np.array(self.subsets[1][0], dtype=int).reshape(1, 159)
        print(len(self.subsets))
        
        # Train with KNN classifier
        print("Training...")
        start_time = time.time()
        clf_knn.fit(X, y)
        end_time = time.time()
        time_diff = end_time - start_time
        total_time = time_diff
        print(f"Score : {clf_knn.score(X, y)}")
        print(f"Train done in {time_diff} seconds \n")

        # Predict with KNN classifier
        print("Predicting...")
        start_time = time.time()
        predictions = clf_knn.predict(X_test)
        end_time = time.time()
        time_diff = end_time - start_time
        total_time += time_diff
        print(predictions)
        print(f"Predict done in {time_diff} seconds \n")

        print(f"All tasks ended in {total_time} seconds")



