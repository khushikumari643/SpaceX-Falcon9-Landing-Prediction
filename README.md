# SpaceX-Falcon9-Landing-Prediction
This project aims to predict the success of SpaceX rocket launches and landings using historical flight data. By analyzing various mission parameters, we develop and evaluate machine learning models to classify whether a launch will result in a successful landing.
Table of Contents
Problem Statement
Data Sources
Methodology
Exploratory Data Analysis (EDA) & Key Insights
Predictive Modeling
Results
Installation
Usage
Future Work
Problem Statement
SpaceX has revolutionized space travel with its reusable rocket technology. Predicting the success of a rocket landing is crucial for mission planning, resource allocation, and optimizing future designs. This project tackles the challenge of building a robust prediction system using historical data.

Data Sources
Wikipedia (Web Scraped): Initial flight data (Flight No., Date, Time, Launch Site, Payload, Payload Mass, Orbit, Customer, Launch Outcome, Booster Landing) was extracted using web scraping techniques.
IBM Pre-processed Dataset: A more structured dataset containing features engineered for machine learning, including FlightNumber, PayloadMass, Orbit, LaunchSite, Flights, GridFins, Reused, Legs, LandingPad, Block, ReusedCount, Serial, and Class (the target variable for success/failure).
Methodology
1. Data Collection & Preprocessing
Web Scraping: Utilized requests and BeautifulSoup to scrape historical launch data from Wikipedia.
Data Integration: Combined web-scraped data with a pre-processed IBM dataset.
Data Cleaning: Handled missing values and standardized data formats.
Feature Engineering:
Created a binary Class variable (1 for successful landing, 0 for failure).
Applied one-hot encoding to categorical features (Orbit, LaunchSite, LandingPad, Serial) using pandas.get_dummies.
Scaled numerical features using StandardScaler to normalize their range and prevent dominance by features with larger values.
Database: Loaded processed data into an SQLite database for efficient querying and storage.
2. Exploratory Data Analysis (EDA) & Key Insights
Flight Number vs. Success: A strong positive correlation was observed between increasing FlightNumber and higher success rates, indicating SpaceX's continuous improvement.
Payload Mass vs. Launch Site: CCAFS SLC 40 and KSC LC 39A demonstrated versatility in handling a wide range of payload masses, including the heaviest. VAFB SLC 4E primarily supported lighter payloads.
Orbit Success Rates: Specific orbits (e.g., ES-L1, GEO, HEO, SSO) showed 100% success, while others (GTO, ISS) had moderate success, and SO had 0% success, highlighting orbital challenges.
Yearly Success Trend: The overall success rate has steadily increased since 2013, reaching peak performance in later years.
Geospatial Visualization: Utilized Folium to map launch sites and visually represent success/failure outcomes, showing geographical concentrations and site-specific performance.
3. Predictive Modeling
Train-Test Split: Data was split into 80% training and 20% testing sets to ensure robust model evaluation.
Model Selection: Four common classification algorithms were implemented:
Logistic Regression
Support Vector Machine (SVM)
Decision Tree Classifier
K-Nearest Neighbors (KNN)
Hyperparameter Tuning: GridSearchCV with 10-fold cross-validation was used to optimize hyperparameters for each model, maximizing their performance.
Model Convergence: Adjusted max_iter for Logistic Regression to ensure convergence.
Results
All models were evaluated based on their test set accuracy after hyperparameter tuning:

Logistic Regression: Test Accuracy: 0.833
Support Vector Machine (SVM): Test Accuracy: 0.833
Decision Tree Classifier: Test Accuracy: 0.611
K-Nearest Neighbors (KNN): Test Accuracy: 0.778
Best Performing Models: Logistic Regression and SVM achieved the highest test accuracy of approximately 83.3% for predicting SpaceX launch success.

Installation
To run this project, you'll need the following Python libraries. You can install them using pip:

pip install -r requirements.txt
Usage
Clone this repository.
Open the Jupyter Notebook (e.g., SpaceX_Launch_Prediction.ipynb).
Run all cells sequentially to perform data collection, preprocessing, EDA, model training, and evaluation.
Explore the visualizations and model performance metrics.
Future Work
Experiment with more advanced machine learning models (e.g., Random Forests, Gradient Boosting).
Incorporate more complex feature engineering.
Implement deep learning models for sequence data (if time-series features are expanded).
Deploy the best-performing model as a web service for real-time predictions.
