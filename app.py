from flask import Flask, request, render_template
#from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
import numpy as np 
# Load the Random Forest CLassifier model
file_name = "model_file.p"
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    temp_array = list()    
    if request.method == 'POST':
        latitude = str(request.form['latitude'])
        longitude = str(request.form['longitude'])
        minimum_nights = int(request.form['minimum_nights'])
        availability_365 = int(request.form['availability_365'])
        calculated_host_listings_count = int(request.form['calculated_host_listings_count'])
        #number_of_reviews = int(request.form['number_of_reviews'])
        reviews_per_month = float(request.form['reviews_per_month'])
        
        neighbourhood=request.form['neighbour']
        if(neighbourhood=='Bronx'):
            temp_array = temp_array + [1,0,0,0,0]     
        elif (neighbourhood=='Brooklyn'):
            temp_array = temp_array + [0,1,0,0,0] 
        elif (neighbourhood=='Manhattan'):
            temp_array = temp_array + [0,0,1,0,0] 
        elif (neighbourhood=='Queens'):
            temp_array = temp_array + [0,0,0,1,0] 
        elif (neighbourhood=='Staten_Island'):
            temp_array = temp_array + [0,0,0,0,1] 

        room=request.form['room']
        if(room=='Entire_home_apt'):
            temp_array = temp_array + [1,0,0]        
        elif (room=='Private_room'):
            temp_array = temp_array + [0,1,0]   
        elif (room=='Shared_room'):
            temp_array = temp_array + [0,0,1]   

        #temp_array = temp_array + [Minimum_Nights, Availability,Host_Listing, Reviews,Reviews_by_Month ]
        
        temp_array = [latitude,longitude,minimum_nights,reviews_per_month,calculated_host_listings_count,availability_365]+ temp_array 
        
        data = np.array([temp_array])
        my_prediction = int((model.predict(data).reshape(1,-1))[0])
    #     prediction = regressor.predict([['latitude', 'longitude', 'minimum_nights', 'number_of_reviews',
    #    'reviews_per_month', 'calculated_host_listings_count',
    #    'availability_365', 'Bronx', 'Brooklyn', 'Manhattan', 'Queens',
    #    'Staten Island', 'Entire home/apt', 'Private room', 'Shared room']])
        return render_template("result.html", my_prediction=my_prediction )#lower_limit = my_prediction-5, upper_limit = my_prediction+5,data=data)

if __name__ == "__main__":
    app.run(debug=True)