# EstrelaBet Churn Prediction Project

This app predicts customer churn probability and recommends retention campaigns based on user data.

## Features

### Single Prediction

Predict churn for a single user by filling in the required fields and pressing "Run prediction".

### Batch Prediction

Upload a CSV file with user data to process multiple users at once. The output includes predictions, campaign recommendations, and generated features.

### Output Interpretation

#### Churn Prediction

- **0**: User is not likely to churn.
- **1**: User is likely to churn.

#### Campaign Recommendations

Based on churn risk and CLV, the app recommends:

- **vip_account_manager**: High-value customers (budget > R$375).
- **phone_outreach**: Medium-high value customers (budget > R$137.50).
- **bonus_offer**: Medium value customers (budget > R$100).
- **automated_email**: Low-medium value customers (budget > R$25).
- **no_action**: Low-value or low-risk customers.

## How to Run

1. Navigate to the project folder in your terminal
2. Start the application using Uvicorn:

```
uvicorn app:app --reload
```

3. It is highly recommended to create a virtual enviroment to run the app (use the requirements file)
4. Open the provided URL in your browser to access the app (don't forget to add /app at the end).

## Developer Information

- [LinkedIn](https://www.linkedin.com/in/leomar-fonseca/)
- [GitHub](https://github.com/leomarfmn)
