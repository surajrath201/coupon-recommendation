#check the ipynb file for more information on Data preprocessing and EDA
#importing the necessary packages
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pickle


def create():
    #read the csv file
    df = pd.read_csv("in-vehicle-coupon-recommendation.csv")

    #remove the columns as per the EDA
    #check the ipynb file for more information on Data preprocessing and EDA
    df.drop(columns=["car", "toCoupon_GEQ5min", "direction_opp", "occupation", "gender", "income", "education"], inplace = True)

    #drop the duplicates row and drop the rows wil null vlaues
    df = df.drop_duplicates()
    df.dropna(inplace = True)
    
    #change the expiration time to hr
    for i, row in df.iterrows():
        
        if df.at[i, "expiration"].endswith("h"):
            df.at[i, "expiration"] = int(df.at[i, "expiration"][:1])
        else :
            df.at[i, "expiration"] = int(df.at[i, "expiration"][:1]) * 24
    df["expiration"] = df["expiration"].astype(int)

    #standandise the data
    df["age"] = np.where(df["age"] == '50plus', 50, df["age"])
    df["age"] = np.where(df["age"] == 'below21', 18, df["age"])
    df["age"] = df["age"].astype(int)

    # renaming the output columns "Y" to "coupon_accepted" and correcting the spelling of passenger
    df.rename({"Y" : "coupon_accepted", "passanger" : "passenger"}, axis = 1, inplace = True)

    #change the encoding of the text attributes
    columns = ['destination','passenger','time','coupon', 'weather','maritalStatus', 'Bar', 'CoffeeHouse', 'CarryAway',
        'RestaurantLessThan20', 'Restaurant20To50']
    for col in columns:
        df[col] = df[col].astype('category')
        df[col] = df[col].cat.codes
        df[col] = df[col].astype('int')

    

    # we separate the input and target variables
    x = df.drop('coupon_accepted', axis = 1)
    y = df.coupon_accepted

    #Now, we use standard scaler from sklearn to normalize our data
    scale = StandardScaler()
    x = scale.fit_transform(x)

    #Now, we divide our dataset into traning and testing set
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 1)


    # we used a random forest classifier to classify the data 
    # in this model we achieved the best accuracy among the other 5 models we created
    model = RandomForestClassifier()
    #train the model with hyperparameters we achieved the best accuracy
    model = RandomForestClassifier(bootstrap = True,
                               max_features = 'auto',
                               min_samples_leaf = 1,
                               min_samples_split = 10,
                               n_estimators = 800, 
                               max_depth = None).fit(x_train, y_train)
    
    filename = "model.pickle"

    # save model
    pickle.dump(model, open(filename, "wb"))

    print("Model trained and saved successfully")
    