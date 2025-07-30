import pandas as pd
import numpy as np
import joblib
from constants_and_templates import BINNING_FEATURES, CATEGORICAL_COLUMNS, SINGLE_PREDICTION_OUTPUT_TEMPLATE

def single_prediction(*args):
    # Call the prediction function
    churn_prediction, churn_probability, clv_to_date, clv_tier, campaign_type = run_prediction(*args)

    # Format the output
    output = SINGLE_PREDICTION_OUTPUT_TEMPLATE.format(
        churn_prediction=churn_prediction,
        churn_probability=churn_probability,
        clv_to_date=clv_to_date,
        clv_tier=clv_tier,   
        campaign_type=campaign_type
    )
    return output



def batch_prediction(input_file):
    output_file = run_prediction(input_file)
    return output_file



def run_prediction(*args):
    # Check if first argument is a file path (batch prediction)
    if len(args) == 1 and isinstance(args[0], str):
        prediction_type = "batch"
        input_file = args[0]
        df = pd.read_csv(input_file)
    
    # Single prediction case - create dataframe from inputs
    else:
        prediction_type = "single"
        # Create dataframe from inputs
        columns = [
            'user_id', 'session_id', 'timestamp', 'date', 'hour', 'day_of_week',
            'is_weekend', 'is_holiday', 'game_type', 'sport_type', 'country', 'device_type',
            'payment_method', 'user_age', 'account_age_days', 'vip_tier',
            'campaign_type', 'bet_amount', 'win_amount', 'net_result',
            'session_length_minutes', 'games_played', 'bonus_used',
            'deposit_amount', 'withdrawal_amount', 'previous_session_gap_hours',
            'lifetime_deposits', 'lifetime_bets', 'avg_bet_size'
        ]
        df = pd.DataFrame([args], columns=columns)
    
    # Create features and score users
    df = create_features(df)
    with open('best_xgb_model.pkl', 'rb') as f:
                churn_model = joblib.load(f)
    df['predicted_churn_proba'] = churn_model.predict_proba(df[churn_model.feature_names_in_])[:, 1]
    df['predicted_churn'] = churn_model.predict(df[churn_model.feature_names_in_])

    # Define campaign
    df['success_rate'] = np.where(df['predicted_churn_proba'] > 0.8, 0.15,
                     np.where(df['predicted_churn_proba'] > 0.6, 0.2,
                     np.where(df['predicted_churn_proba'] > 0.3, 0.275, 0)))
    df['campaign_budget'] = df['success_rate'] * df['clv_real']
    df['campaign'] = np.where(df['campaign_budget'] > 375, 'vip_account_manager',
                 np.where(df['campaign_budget'] > 137.5, 'phone_outreach',
                 np.where(df['campaign_budget'] > 100, 'bonus_offer',
                 np.where(df['campaign_budget'] > 25, 'automated_email', 'no_action'))))

    if prediction_type == "single":
        churn_prediction = df['predicted_churn'].values[0]
        churn_probability = df['predicted_churn_proba'].values[0]
        clv_to_date = df['clv_real'].values[0]
        clv_tier = df['clv_tier'].values[0]
        campaign_type = df['campaign'].values[0]
        return churn_prediction, churn_probability, clv_to_date, clv_tier, campaign_type
    else:
        # Save the predictions to a new file
        output_file = 'scored_dataset.csv'
        df.to_csv(output_file, index=False)
        return output_file



def create_features(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(['user_id', 'timestamp'], inplace=True)
    
    # Calculate company net result
    df['company_net_result'] = df['bet_amount'] - df['win_amount']
    
    # CLV real
    if len(df) > 1:
        df['clv_real'] = df.groupby('user_id')['company_net_result'].cumsum()
    else:
        df['clv_real'] = df['company_net_result']
    
    # Create CLV tiers
    df['clv_tier'] = np.where(df['clv_real'] < 1000, 'bronze',
                     np.where(df['clv_real'] < 2000, 'silver',
                     np.where(df['clv_real'] < 5500, 'gold',
                     np.where(df['clv_real'] < 10000, 'platinum', 'diamond'))))
    
    # Frequency encoding
    for feature in CATEGORICAL_COLUMNS:
        with open(f'serialized_files/{feature}_frequency_mappings.pkl', 'rb') as f:
            frequency_mappings = joblib.load(f)
        df[f'frequency_encoded_{feature}'] = df[feature].map(frequency_mappings[feature])
    
    # One-hot encoded columns
    # Day of week
    df['day_of_week_1.0'] = np.where(df['day_of_week'] == 1.0, 1, 0)
    df['day_of_week_2.0'] = np.where(df['day_of_week'] == 2.0, 1, 0)
    df['day_of_week_3.0'] = np.where(df['day_of_week'] == 3.0, 1, 0)
    df['day_of_week_4.0'] = np.where(df['day_of_week'] == 4.0, 1, 0)
    df['day_of_week_5.0'] = np.where(df['day_of_week'] == 5.0, 1, 0)
    df['day_of_week_6.0'] = np.where(df['day_of_week'] == 6.0, 1, 0)
    df['day_of_week_nan'] = np.where(df['day_of_week'].isna(), 1, 0)
    
    # Is weekend
    df['is_weekend_1.0'] = np.where(df['is_weekend'] == 1.0, 1, 0)
    df['is_weekend_nan'] = np.where(df['is_weekend'].isna(), 1, 0)
    
    # Is holiday
    df['is_holiday_1.0'] = np.where(df['is_holiday'] == 1.0, 1, 0)
    df['is_holiday_nan'] = np.where(df['is_holiday'].isna(), 1, 0)
    
    # Bonus used
    df['bonus_used_1.0'] = np.where(df['bonus_used'] == 1.0, 1, 0)
    df['bonus_used_nan'] = np.where(df['bonus_used'].isna(), 1, 0)
    
    # Game type
    df['game_type_casino_slots'] = np.where(df['game_type'] == 'casino_slots', 1, 0)
    df['game_type_live_dealer'] = np.where(df['game_type'] == 'live_dealer', 1, 0)
    df['game_type_poker'] = np.where(df['game_type'] == 'poker', 1, 0)
    df['game_type_roulette'] = np.where(df['game_type'] == 'roulette', 1, 0)
    df['game_type_sports_betting'] = np.where(df['game_type'] == 'sports_betting', 1, 0)
    df['game_type_nan'] = np.where(df['game_type'].isna(), 1, 0)
    
    # Sport type
    df['sport_type_basketball'] = np.where(df['sport_type'] == 'basketball', 1, 0)
    df['sport_type_football'] = np.where(df['sport_type'] == 'football', 1, 0)
    df['sport_type_golf'] = np.where(df['sport_type'] == 'golf', 1, 0)
    df['sport_type_hockey'] = np.where(df['sport_type'] == 'hockey', 1, 0)
    df['sport_type_soccer'] = np.where(df['sport_type'] == 'soccer', 1, 0)
    df['sport_type_tennis'] = np.where(df['sport_type'] == 'tennis', 1, 0)
    df['sport_type_nan'] = np.where(df['sport_type'].isna(), 1, 0)
    
    # Country
    df['country_BR'] = np.where(df['country'] == 'BR', 1, 0)
    df['country_CA'] = np.where(df['country'] == 'CA', 1, 0)
    df['country_DE'] = np.where(df['country'] == 'DE', 1, 0)
    df['country_ES'] = np.where(df['country'] == 'ES', 1, 0)
    df['country_FR'] = np.where(df['country'] == 'FR', 1, 0)
    df['country_IT'] = np.where(df['country'] == 'IT', 1, 0)
    df['country_MX'] = np.where(df['country'] == 'MX', 1, 0)
    df['country_UK'] = np.where(df['country'] == 'UK', 1, 0)
    df['country_US'] = np.where(df['country'] == 'US', 1, 0)
    df['country_nan'] = np.where(df['country'].isna(), 1, 0)
    
    # Device type
    df['device_type_mobile'] = np.where(df['device_type'] == 'mobile', 1, 0)
    df['device_type_tablet'] = np.where(df['device_type'] == 'tablet', 1, 0)
    df['device_type_nan'] = np.where(df['device_type'].isna(), 1, 0)
    
    # Payment method
    df['payment_method_credit_card'] = np.where(df['payment_method'] == 'credit_card', 1, 0)
    df['payment_method_crypto'] = np.where(df['payment_method'] == 'crypto', 1, 0)
    df['payment_method_debit_card'] = np.where(df['payment_method'] == 'debit_card', 1, 0)
    df['payment_method_e_wallet'] = np.where(df['payment_method'] == 'e_wallet', 1, 0)
    df['payment_method_nan'] = np.where(df['payment_method'].isna(), 1, 0)
    
    # VIP tier
    df['vip_tier_diamond'] = np.where(df['vip_tier'] == 'diamond', 1, 0)
    df['vip_tier_gold'] = np.where(df['vip_tier'] == 'gold', 1, 0)
    df['vip_tier_platinum'] = np.where(df['vip_tier'] == 'platinum', 1, 0)
    df['vip_tier_silver'] = np.where(df['vip_tier'] == 'silver', 1, 0)
    df['vip_tier_nan'] = np.where(df['vip_tier'].isna(), 1, 0)
    
    # Campaign type
    df['campaign_type_free_spins'] = np.where(df['campaign_type'] == 'free_spins', 1, 0)
    df['campaign_type_none'] = np.where(df['campaign_type'] == 'none', 1, 0)
    df['campaign_type_reload_bonus'] = np.where(df['campaign_type'] == 'reload_bonus', 1, 0)
    df['campaign_type_welcome_bonus'] = np.where(df['campaign_type'] == 'welcome_bonus', 1, 0)
    df['campaign_type_nan'] = np.where(df['campaign_type'].isna(), 1, 0)
    
    # Binning numerical features
    for feature in BINNING_FEATURES:
        with open(f'serialized_files/{feature}_medians.pkl', 'rb') as f:
            feature_medians = joblib.load(f)
        df[feature] = df[feature].fillna(feature_medians[feature])
        with open(f'serialized_files/{feature}_bin_edges.pkl', 'rb') as f:
            feature_bin_edges = joblib.load(f)
        df[f"binning_{feature}"] = pd.cut(df[feature], bins=feature_bin_edges[feature], labels=False)
    
    # Create loss indicator
    df['loss'] = np.where(df['net_result'] < 0, 1, 0)
    df['net_result'] = df['net_result'].abs()
    
    # After hours
    df['after_hours'] = df['hour'].between(0, 6).astype(int)
    
    return df