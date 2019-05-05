# This script provides an approach to use random forest algorithm
# to the Housing Prices competition on Kaggle

import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
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

    # split train sets
    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state = 1)
    
    # Define the model. Set random_state to 1
    rf_model = RandomForestRegressor(random_state=1)

    # fit the model to train set
    rf_model.fit(train_X, train_y)

    # calculate the mean absolute error of the Random Forest model on the validation data
    melb_preds = rf_model.predict(val_X)
    rf_val_mae = mean_absolute_error(val_y, melb_preds)

    print("Validation MAE for Random Forest Model: {}".format(rf_val_mae))

        
if __name__ == '__main__':
    main()

