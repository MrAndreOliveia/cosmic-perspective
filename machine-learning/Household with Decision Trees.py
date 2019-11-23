# This script provides an approach to use decision trees on the
# Housing Prices competition on Kaggle

import os
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

print("Setup Complete")


def load_data(file_shortname):
    file_name = file_shortname + '.' + 'csv' 	
    file_path = os.path.join(os.path.expanduser('~'),'Downloads','home-data-for-ml-course',file_name)
    #a = print(file_path)

    if os.path.exists(file_path) == True:
        dataset = pd.read_csv(file_path)
        shape = str(dataset.shape)
        print('Dataset ' + file_shortname + ' created with shape ' + shape)
        #print(dataset.head())
    else:	
        sys.exit               
    return dataset

def get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y):
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)
    model.fit(train_X, train_y)
    preds_val = model.predict(val_X)
    mae = mean_absolute_error(val_y, preds_val)
    return(mae)

def main():
    
    #### STEP 1 Build a model ####
    # load data
    home_data = load_data('train') 
    
    # drop missing values
    #home_data = home_data.dropna(axis=0)   
    #print(home_data)
    
    # select prediction target
    y = home_data.SalePrice

    # select list of features
    feature_names = ['LotArea','YearBuilt','1stFlrSF','2ndFlrSF','FullBath','BedroomAbvGr','TotRmsAbvGrd']   
    
    # create X
    X = home_data[feature_names]
    #print(X.describe())
    #print(X.head())

    # select model
    #for model reproducibility, set a numeric value for random_state when specifying the model
    iowa_model = DecisionTreeRegressor(random_state=1)

    # fit the model
    iowa_model.fit(X, y)

    # make predictions
    predictions = iowa_model.predict(X)
    print(predictions)

 
    #### STEP 2 Model validation ####
    # split train sets
    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state = 1)
    
    # specify model    
    iowa_model = DecisionTreeRegressor(random_state=1)

    # fit model with the training data.
    iowa_model.fit(train_X, train_y)

    # predict with all validation observations
    val_predictions = iowa_model.predict(val_X) 
  
    # inspect predictions    
    print(iowa_model.predict(train_X.head()))   # print the top few validation predictions   
    print(iowa_model.predict(val_X.head()))   # print the top few actual prices from validation data

    # calculate the Mean Absolute Error in the validation data
    val_mae = mean_absolute_error(val_y, val_predictions)
    print(val_mae)
 
    
    #### STEP 3 Model Underfitting and Overfitting ####
    
    # find optimal number of leaf nodes for decision tree 
    candidate_max_leaf_nodes = [5, 10, 15, 20, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 500]       
    for i in candidate_max_leaf_nodes:
        my_mae = get_mae(i, train_X, val_X, train_y, val_y)
        print("Max leaf nodes: %d  \t\t Mean Absolute Error:  %d" %(i, my_mae))

    scores = {leaf_size: get_mae(leaf_size, train_X, val_X, train_y, val_y) for leaf_size in candidate_max_leaf_nodes}
    best_tree_size = min(scores, key=scores.get)
    print(best_tree_size)

    # fit the model with best_tree_size. Fill in argument to make optimal size
    final_model = DecisionTreeRegressor(max_leaf_nodes=best_tree_size, random_state=1)

    # fit the final model
    final_model.fit(X, y)
    
    # make final predictions
    final_predictions = final_model.predict(X)
    print(final_predictions)
    
    # get Mean Absolute Error for final model
    final_mae = mean_absolute_error(y, final_predictions)
    print(final_mae)
        
if __name__ == '__main__':
    main()
