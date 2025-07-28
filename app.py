import gradio as gr
from fastapi import FastAPI

app = FastAPI()

with gr.Blocks() as interface:
    gr.Markdown("# EstrelaBet Churn Prediction")
    with gr.Tab("Instructions"):
        pass
    with gr.Tab("Single prediction"):
        with gr.Row():
            with gr.Column():
                user_id = gr.Textbox(label='user_id')
                session_id = gr.Textbox(label='session_id')
                timestamp = gr.Textbox(label='timestamp')
                date = gr.Textbox(label='date')
                hour = gr.Textbox(label='hour')
                day_of_week = gr.Textbox(label='day_of_week')
                is_weekend = gr.Textbox(label='is_weekend')
                is_holiday = gr.Textbox(label='is_holiday')
                game_type = gr.Textbox(label='game_type')
                sport_type = gr.Textbox(label='sport_type')
            with gr.Column():
                country = gr.Textbox(label='country')
                device_type = gr.Textbox(label='device_type')
                payment_method = gr.Textbox(label='payment_method')
                user_age = gr.Textbox(label='user_age')
                account_age_days = gr.Textbox(label='account_age_days')
                vip_tier = gr.Textbox(label='vip_tier')
                campaign_type = gr.Textbox(label='campaign_type')
                bet_amount = gr.Textbox(label='bet_amount')
                win_amount = gr.Textbox(label='win_amount')
                net_result = gr.Textbox(label='net_result')
            with gr.Column():
                session_length_minutes = gr.Textbox(label='session_length_minutes')
                games_played = gr.Textbox(label='games_played')
                bonus_used = gr.Textbox(label='bonus_used')
                deposit_amount = gr.Textbox(label='deposit_amount')
                withdrawal_amount = gr.Textbox(label='withdrawal_amount')
                previous_session_gap_hours = gr.Textbox(label='previous_session_gap_hours')
                lifetime_deposits = gr.Textbox(label='lifetime_deposits')
                lifetime_bets = gr.Textbox(label='lifetime_bets')
                avg_bet_size = gr.Textbox(label='avg_bet_size')
        run_button = gr.Button("Run prediction")
        output = gr.Textbox(label="Prediction result", interactive=False)
    with gr.Tab("Batch predict"):
        with gr.Column():
            input_file = gr.File(label="Upload file to be processed", file_types=[".csv"], interactive=True)
            run_button = gr.Button("Run prediction")
        with gr.Column():
            output_file = gr.File(label="Download file with predictions", interactive=False)


app = gr.mount_gradio_app(app, interface, path="/app")