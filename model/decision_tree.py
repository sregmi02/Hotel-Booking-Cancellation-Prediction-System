import numpy as np
from collections import Counter

class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None,information_gain=None,value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.information_gain=information_gain
        self.value = value
    
    def print_attributes(self):
        #this method prints the attributes of the given node
        print("Feature to be split: "+(self.feature))
        print("Threshold of split: "+(self.threshold))
        print("Left child: "+(self.left))
        print("Right child: "+(self.right))
        print("Information Gain: "+(self.information_gain))
        print("Value at current node: "+(self.value))


class DecisionTree:
    def __init__(self, n_features, min_samples_split=50, max_depth =15):
        self.min_samples_split=min_samples_split
        self.max_depth=max_depth
        self.n_features=n_features
        
        
    def _entropy(self, y):
        count = np.bincount(np.array(y,dtype=np.int64))
        #probabilities of all the value in the class label
        pb = count / len(y) 
        #initializing entropy
        entropy = 0
        #calculating entropy for all values
        for i in pb:
            if i > 0:
                entropy += i*np.log2(i)
        return -(entropy)
        
    def _information_gain(self, parent_node, left_child_node, right_child_node):
        # calculating number of probabilities of left and right child
        left_childs = len(left_child_node)/len(parent_node)
        right_childs = len(right_child_node)/len(parent_node)
        # calculating entropy for left, right and parent nodes
        parent_entropy = self._entropy(parent_node)
        left_entropy = self._entropy(left_child_node)
        right_entropy = self._entropy(right_child_node)        
        # calculating information gain
        information_gain = parent_entropy - ((left_entropy*left_childs)+(right_entropy*right_childs))
        return information_gain
    
    def _calculate_best_split(self,feature,label):
        # initializing the values
        best_split = {
        "feature_index": None,
        "threshold": None,
        "left": None,
        "right": None,
        "information_gain": -1
        }
        best_information_gain = -1
        (_,columns) = feature.shape
        # calculating best split
        for i in range(columns):
            # selecting specific input feature column
            x_current = feature[:,i]
            for threshold in np.unique(x_current):
                # creating dataset by concatenating X and y
                dataset = np.concatenate((feature,label.reshape(1,-1).T),axis=1)
                # splitting dataset into two halfs (left and right) based on rows
                dataset_left = np.array([row for row in dataset if row[i] <= threshold])
                dataset_right = np.array([row for row in dataset if row[i] > threshold])
                # selecting best information gain
                if (len(dataset_left)>0) and (len(dataset_right)>0):
                    y = dataset[:,-1]
                    y_left = dataset_left[:,-1]
                    y_right = dataset_right[:,-1]
                    # calculating information gain
                    information_gain = self._information_gain(y,y_left,y_right)
                    if (information_gain > best_information_gain):
                        best_split = {
                            "feature_index":i,
                            "threshold":threshold,
                            "left":dataset_left,
                            "right":dataset_right,
                            "information_gain":information_gain
                        }
                        best_information_gain = information_gain
        if best_split["feature_index"] is not None:
            print("Splitted Column: {0}".format(self.n_features[best_split['feature_index']]))
        return best_split
    
    def _grow_tree(self, X, y, depth=0):
        num_rows, num_cols = X.shape
        print("-----------------------------")
        print("At Level {0}:".format(depth))
        print("Number of instances of X: {0}".format(num_rows))
        print("Number of columns to split in X: {0}".format(num_cols))
        print("------------------------------")
        # condition1 checks whether there is number of rows greater than or equal to minimun samples to split
        condition1 = (num_rows >= self.min_samples_split)
        # condition2 checks whether the current depth is less than or equal to max depth defined
        condition2 = (depth < self.max_depth)
        # checking both conditions to build the tree
        if condition1 and condition2:
           #selecting the best split of the current depth
            splitted_data = self._calculate_best_split(X,y)
           # checking whether the best split given by the data is pure or not 
            if (splitted_data['information_gain']) > 0:
              # using recursion to determine left and right child of the tree
              # left child split
                new_depth = depth+1
                print("Left Split to level: {0}".format(new_depth))
                X_left = splitted_data['left'][:,:-1]
                y_left = splitted_data['left'][:,-1]
                left_child = self._grow_tree(X_left,y_left,new_depth)
              # right child split
                print("Right Split to level: {0}".format(new_depth))
                X_right = splitted_data['right'][:,:-1]
                y_right = splitted_data['right'][:,-1]
                right_child = self._grow_tree(X_right,y_right,new_depth)
              # after calculating returning the data to the previous iteration of recursion
                return Node(
                      feature = splitted_data['feature_index'],
                      threshold = splitted_data['threshold'],
                      left = left_child,
                      right = right_child,
                      information_gain = splitted_data['information_gain'])
        # returning the most common target value for the leaf node
        return Node(value=Counter(y).most_common(1)[0][0])
              
      
    def fit(self,X,y):
        print("-----------------------------")
        print("Training Process Strated.")
        self.root = self._grow_tree(X,y)


    def _predict(self,x,tree):
        if tree.value !=None:
            print(int(tree.value))
            return tree.value
        feature = x[tree.feature]
        #print("Tree Feature:{0}".format(tree.feature))
        #go to left
        if feature<= tree.threshold:
            print("Left Split:{0} <= {1}".format(self.n_features[tree.feature],tree.threshold))
            return self._predict(x = x, tree = tree.left)
        if feature > tree.threshold:
            print("Right Split:{0} > {1}".format(self.n_features[tree.feature],tree.threshold))
            return self._predict(x = x, tree = tree.right)
     
                 
    def predict(self,X, n_features):
        self.n_features = n_features
        return [self._predict(x,self.root) for x in X]
    
              