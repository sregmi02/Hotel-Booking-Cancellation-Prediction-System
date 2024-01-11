from .decision_tree import DecisionTree
import numpy as np
from collections import Counter

class RandomForest:
    def __init__(self, n_trees=10, max_depth=10, min_samples_split=100, n_features=None):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.n_features = n_features
        self.trees = []

   
    def _sample(self, X, y):
        n_rows, n_cols = X.shape
        # sampling the dataset with replacements
        sample = np.random.choice(a = n_rows, size = n_rows, replace = True)
        samples_x = X[sample]
        samples_y = y[sample]
        return samples_x,samples_y
    
    
    def train_model(self, X, y):
        i =0
        if len(self.trees)>0:
            self.trees=[]
        tree_built=0
        while tree_built < self.n_trees:
            print("-----------------------------")
            print("Iteration: {0}".format(i))
            tree = DecisionTree(n_features = self.n_features,
                min_samples_split = self.min_samples_split,
                max_depth = self.max_depth)
            sample_x, sample_y = self._sample(X, y)
            tree.train_model(sample_x, sample_y)
            self.trees.append(tree)
            tree_built += 1
            i += 1
      
    
    def predict(self, X, n_features):
        self.n_features = n_features
        labels = []
        counter = 0
        for tree in self.trees:
            counter += 1
            print("------------------------------")
            print("Tree:{0}".format(counter))
            labels.append(tree.predict(X, n_features))
        labels = np.swapaxes(a = labels, axis1 = 0, axis2 = 1)
        predictions = []
        for preds in labels:
            counter = Counter(preds)
            predictions.append(counter.most_common(1)[0][0])
        return predictions