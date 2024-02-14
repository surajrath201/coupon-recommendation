import create_model
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS

#create a flash app for backend
app = Flask(__name__)
#runs cors for smooth connection of frontend to backend
CORS(app)

#function to predict coupon acceptance oupn certain input
def predict(model, destination, passenger, weather, temperature, time, coupon, expiration, age, maritalStatus, hasChildren, 
            bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, dist15, dist25, direction):
    
    data = [[conversion_dic[destination], conversion_dic[passenger], conversion_dic[weather], 
         temperature, conversion_dic[time], conversion_dic[coupon], 24, age, 
         conversion_dic[maritalStatus], hasChildren, conversion_dic[bar], 
         conversion_dic[coffeeHouse], conversion_dic[carryAway], conversion_dic[restaurantLess20],
         conversion_dic[restaurant20To50], dist15, dist25, direction]]
    result_1 = {"type": coupon, "dist15": dist15, "dist25": dist25, 
                "expiration": "1d" if expiration == 24 else "2hr", "accepted": model.predict(data)[0]}
    return result_1

#conversion dictionary to convert string input to respective integer
#this is the same conversion through which model is trained
conversion_dic = {"No Urgent Place": 1, "Work": 2, "Home": 0,
                  "Alone": 0, "Friend(s)": 1, "Kid(s)": 2, "Partner" :3,
                  "Sunny":2, "Snowy":1, "Rainy":0,
                  "7AM": 4, "6PM": 3,"10AM": 0 ,"2PM": 2, "10PM": 1,
                  "Coffee House":2 ,"Restaurant(<20)":4, "Carry out & Take away":1,
                  "Restaurant(20-50)": 3, "Bar":0, 
                  "Married partner" :1,"Single": 2, "Unmarried partner": 3,
                  "Divorced": 0 , "Widowed": 4,
                  "never" : 4, "less1": 3, "1~3": 0 , "4~8": 1 , "gt8":23}


# Api call for collecting the data from frontend
# and sending the relevant ouput(coupon predicted by our model)
@app.route('/submit-form', methods=['POST'])
def predict_coupon():

    #read the data from request
    data = request.get_json()
    destination = data.get('destination')
    passenger = data.get('passenger')
    age = data.get("age")
    maritalStatus = data.get("maritalStatus")
    hasChildren = data.get("hasChildren")
    bar = data.get("bar")
    coffeeHouse = data.get("coffeeHouse")
    carryAway = data.get("carryAway")
    restaurantLess20 = data.get("restaurantLess20")
    restaurant20To50 = data.get("restaurant20To50")

    # load the saved model 
    filename = "model.pickle"
    model = pickle.load(open(filename, "rb"))

    #let assume the weather is sunny and temperature is 80
    #and time when the user booked the car is 10AM
    weather = "Sunny"
    temperature = 80
    time = "10AM"


    #List for saving each result
    result = []

    #check for each coupon separately with two restaurant 
    #one with distance greater than 15 min other with 25 min and
    #with expiration 1 day and 2 hr
    #coffee house coupon check with restaurant 1 with expiration 1 day
    result.append(predict(model, destination, passenger, weather, temperature, time, "Coffee House", 24, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 0, 1))

    #coffee house coupon check with restaurant 1 with expiration 2 hour
    result.append(predict(model, destination, passenger, weather, temperature, time, "Coffee House", 2, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 0, 1))

    #coffee house coupon check with restaurant 2 with expiration 1 day
    result.append(predict(model, destination, passenger, weather, temperature, time, "Coffee House", 24, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 1, 1))

    #coffee house coupon check with restaurant 2 with expiration 2 hour
    result.append(predict(model, destination, passenger, weather, temperature, time, "Coffee House", 2, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 1, 1))


    #Bar coupon check with restaurant 1 with expiration 1 day
    result.append(predict(model, destination, passenger, weather, temperature, time, "Bar", 24, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 0, 1))

    #Bar coupon check with restaurant 1 with expiration 2 hour
    result.append(predict(model, destination, passenger, weather, temperature, time, "Bar", 2, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 0, 1))

    #Bar coupon check with restaurant 2 with expiration 1 day
    result.append(predict(model, destination, passenger, weather, temperature, time, "Bar", 24, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 1, 1))

    #Bar coupon check with restaurant 2 with expiration 2 hour
    result.append(predict(model, destination, passenger, weather, temperature, time, "Bar", 2, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 1, 1))


    #Carry out & Take away coupon check with restaurant 1 with expiration 1 day
    result.append(predict(model, destination, passenger, weather, temperature, time, "Carry out & Take away", 24, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 0, 1))

    #Carry out & Take away coupon check with restaurant 1 with expiration 2 hour
    result.append(predict(model, destination, passenger, weather, temperature, time, "Carry out & Take away", 2, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 0, 1))

    #Carry out & Take away coupon check with restaurant 2 with expiration 1 day
    result.append(predict(model, destination, passenger, weather, temperature, time, "Carry out & Take away", 24, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 1, 1))

    #Carry out & Take away coupon check with restaurant 2 with expiration 2 hour
    result.append(predict(model, destination, passenger, weather, temperature, time, "Carry out & Take away", 2, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 1, 1))


    #Restaurant(<20) coupon check with restaurant 1 with expiration 1 day
    result.append(predict(model, destination, passenger, weather, temperature, time, "Restaurant(<20)", 24, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 0, 1))

    #Restaurant(<20) coupon check with restaurant 1 with expiration 2 hour
    result.append(predict(model, destination, passenger, weather, temperature, time, "Restaurant(<20)", 2, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 0, 1))

    #Restaurant(<20) coupon check with restaurant 2 with expiration 1 day
    result.append(predict(model, destination, passenger, weather, temperature, time, "Restaurant(<20)", 24, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 1, 1))

    #Restaurant(<20) coupon check with restaurant 2 with expiration 2 hour
    result.append(predict(model, destination, passenger, weather, temperature, time, "Restaurant(<20)", 2, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 1, 1))


    #Restaurant(20-50) coupon check with restaurant 1 with expiration 1 day
    result.append(predict(model, destination, passenger, weather, temperature, time, "Restaurant(20-50)", 24, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 0, 1))

    #Restaurant(20-50) coupon check with restaurant 1 with expiration 2 hour
    result.append(predict(model, destination, passenger, weather, temperature, time, "Restaurant(20-50)", 2, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 0, 1))

    #Restaurant(20-50) coupon check with restaurant 2 with expiration 1 day
    result.append(predict(model, destination, passenger, weather, temperature, time, "Restaurant(20-50)", 24, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 1, 1))

    #Restaurant(20-50) coupon check with restaurant 2 with expiration 2 hour
    result.append(predict(model, destination, passenger, weather, temperature, time, "Restaurant(20-50)", 2, age, maritalStatus,
                        hasChildren, bar, coffeeHouse, carryAway, restaurantLess20, restaurant20To50, 1, 1, 1))

    #count the accepted_coupon 
    accepted_count = 0
    for item in result:
        if item["accepted"] == 1:
            accepted_count += 1
    total_count = len(result)

    #acceptance rate per coupon type
    coupon_type = ["Coffee House", "Restaurant(<20)", "Carry out & Take away", "Restaurant(20-50)", "Bar"]
    coupon_count = [0, 0, 0, 0, 0]
    for i, name in enumerate(coupon_type):
        for item in result:
            if item['accepted'] == 1 and item['type'] == name:
                coupon_count[i] += 1
    

    #filter out the accpeted coupon
    result = list(filter(lambda x: x['accepted'] == 1, result))
    #change the result to accomodate json type
    for item in result:
        item['accepted'] = int(item['accepted'])
    

    # prepare the response data to send to frontend
    response_data = {
        'message': 'coupon acceptance percentage predicted',
        'bar' : [accepted_count, total_count - accepted_count],
        'labels': ["acceptance", "rejection"],
        'result' : result,
        'couponType' : coupon_type,
        'couponCount' : coupon_count
        }

    return jsonify(response_data), 201


if __name__ == '__main__':
    
    #create the model
    #the below model is created after data preproceesing and EDA analysis
    #and comapring 5 model. The model with best accuracy is selected
    # A demo model is created and saved already in the module
    #uncomment the following to create a new model
    #create_model.create()  

    #run the backend flask app
    app.run()