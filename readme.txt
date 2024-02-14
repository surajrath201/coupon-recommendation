### This file contains list of contents in phase 3 folder and steps to run the project ###

### content of the folder

# in-vehicle-coupon-recommendation : the csv file contaning the traning data
# project_phase_1_2                : ipynb file contaning each and every step of data preprocessing, EDA and 
			                   creating different model and evaluating them.
# create_model.py                  : python file to create the model with best accuracy 
						 and store the model as model.pickle
# model.pickle 			     : pre-trained model stored as a refrence
# main.py				     : python backend file which
# homepage.html 			     : html file to run the frontend
# style.css				     : css file of the html
# script.js				     : js file for the html


#### To run the ipynb file and py file install the following modules

- pandas
- numpy
- sklearn
- tensorflow
- matplotlib
- pickle
- seaborn
- pandas_profiling
- flask
- flask_cors


####  If you want to observe step by step data preprocessing and EDA
	run the project_phase_1_2 file and go through each step of the process.
	The ipynb file also contain five model that are trained and evaluated.The 
	model having best accuracy score is selected.

#### To run the project
	1. Start the backend by running the "main.py" file.
	   Uncomment the create_model line (line 197) to create the model again
	   OR use the pre trained model already provided
	2. Run the homepage.html to start the frontend
	3. Project is ready to run, input the values in frontend and view the result



