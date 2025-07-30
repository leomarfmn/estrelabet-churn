BINNING_FEATURES = [
    'user_age', 'account_age_days', 'bet_amount', 'win_amount', 'net_result',
    'session_length_minutes', 'games_played', 'deposit_amount', 
    'withdrawal_amount', 'lifetime_deposits', 'lifetime_bets', 'avg_bet_size'
]

CATEGORICAL_COLUMNS = ['game_type', 'sport_type', 'country', 'device_type', 'payment_method', 'vip_tier', 'campaign_type']

SINGLE_PREDICTION_OUTPUT_TEMPLATE = """
    Churn Prediction: {churn_prediction}
    Churn Probability: {churn_probability}
    CLV to date: {clv_to_date}
    CLV tier: {clv_tier}
    Campaign type: {campaign_type}
    """