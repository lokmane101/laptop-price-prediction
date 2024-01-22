**Laptop Price Prediction**
This project aims to predict laptop prices based on various specifications. The model can be useful for both buyers, to get an estimate of the price before purchasing, and sellers, to set a competitive price for their products.

**Data Collection**
The data was collected through web scraping from a local e-commerce website. Due to the limited amount of data, an additional dataset was added from Kaggle to enhance the model’s performance.

**Data Preparation**
Each dataset was cleaned separately using Exploratory Data Analysis (EDA) techniques. The cleaned datasets were then prepared for modeling using a preprocessing script.

**Model Selection**
Several regression models were applied to the data, including Random Forest, Lasso Regression, Ridge Regression, Linear Regression, and AdaBoost. After calculating the Mean Squared Error (MSE) and R²-score for each model, the Gradient Boosting model was found to provide the best performance.

**Deployment**
The model was deployed using a Streamlit interface. This allows users to input the specifications of a laptop and receive a predicted price.

**Future Work**
The performance of the model could be further improved by adding more data. Additionally, there are plans to commercialize the project in the future.
