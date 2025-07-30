SINGLE_PREDICTION_OUTPUT_TEMPLATE = """
    Churn Prediction: {churn_prediction}
    Churn Probability: {churn_probability}
    CLV to date: {clv_to_date}
    CLV tier: {clv_tier}
    Campaign type: {campaign_type}
    """

CUSTOM_CSS = """
    /* Remove footer */
    .footer {display: none !important}
    footer {display: none !important}
    .gradio-footer {display: none !important}
    #footer {display: none !important}
    [class*="footer"] {display: none !important}
    .wrap.svelte-ymc0vz {visibility: hidden !important}
"""

INSTRUCTIONS = """
This app predicts customer churn probability and recommends retention campaigns based on user data.

## Single Prediction
Should be used to predict a single data point. Fill in the fields and press "Run prediction".

## Batch Prediction
Use this tab to process multiple users at once. Upload a CSV file with the same format as the provided training file and press "Run prediction". The output will be a file with predictions, campaign recommendations, and the features created.

## Output Interpretation
### Churn Prediction
- **0**: User is not likely to churn
- **1**: User is likely to churn

### Campaign Recommendations
Based on churn risk and CLV, the app recommends:
- **vip_account_manager**: High-value customers (budget > R$375)
- **phone_outreach**: Medium-high value customers (budget > R$137.50)
- **bonus_offer**: Medium value customers (budget > R$100)
- **automated_email**: Low-medium value customers (budget > R$25)
- **no_action**: Low-value or low-risk customers

## Developer Information
[LinkedIn](https://www.linkedin.com/in/leomar-fonseca/)  
[GitHub](https://github.com/leomarfmn)
"""