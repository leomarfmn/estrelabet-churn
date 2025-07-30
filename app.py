import gradio as gr
from fastapi import FastAPI
from utils import single_prediction, batch_prediction

app = FastAPI()

with gr.Blocks() as interface:
    gr.Markdown("# EstrelaBet Churn Prediction")
    with gr.Tab("Instructions"):
        pass
    with gr.Tab("Single prediction"):
        inputs = []
        with gr.Row():
            with gr.Column():
                inputs.append(gr.Textbox(label='user_id'))
                inputs.append(gr.Textbox(label='session_id'))
                inputs.append(gr.Textbox(label='timestamp'))
                inputs.append(gr.Textbox(label='date'))
                inputs.append(gr.Number(label='hour', minimum=0, maximum=23, value=0))
                inputs.append(gr.Number(label='day_of_week', minimum=0, maximum=6, value=0))
                inputs.append(gr.Checkbox(label='is_weekend'))
                inputs.append(gr.Checkbox(label='is_holiday'))
                inputs.append(gr.Dropdown(label='game_type', choices=['casino', 'sports', 'poker', 'bingo'], allow_custom_value=True))
                inputs.append(gr.Dropdown(label='sport_type', choices=['football', 'basketball', 'tennis', 'other'], allow_custom_value=True))
            with gr.Column():
                inputs.append(gr.Dropdown(label='country', choices=['BR', 'US', 'UK', 'DE', 'other'], allow_custom_value=True))
                inputs.append(gr.Dropdown(label='device_type', choices=['mobile', 'desktop', 'tablet'], allow_custom_value=True))
                inputs.append(gr.Dropdown(label='payment_method', choices=['credit_card', 'debit_card', 'pix', 'bank_transfer'], allow_custom_value=True))
                inputs.append(gr.Number(label='user_age', minimum=18, maximum=100, value=25))
                inputs.append(gr.Number(label='account_age_days', minimum=0, value=30))
                inputs.append(gr.Dropdown(label='vip_tier', choices=['bronze', 'silver', 'gold', 'platinum'], allow_custom_value=True))
                inputs.append(gr.Dropdown(label='campaign_type', choices=['welcome', 'deposit', 'retention', 'none'], allow_custom_value=True))
                inputs.append(gr.Number(label='bet_amount', minimum=0, value=0, step=0.01))
                inputs.append(gr.Number(label='win_amount', minimum=0, value=0, step=0.01))
                inputs.append(gr.Number(label='net_result', value=0, step=0.01))
            with gr.Column():
                inputs.append(gr.Number(label='session_length_minutes', minimum=0, value=0))
                inputs.append(gr.Number(label='games_played', minimum=0, value=0))
                inputs.append(gr.Checkbox(label='bonus_used'))
                inputs.append(gr.Number(label='deposit_amount', minimum=0, value=0, step=0.01))
                inputs.append(gr.Number(label='withdrawal_amount', minimum=0, value=0, step=0.01))
                inputs.append(gr.Number(label='previous_session_gap_hours', minimum=0, value=0, step=0.1))
                inputs.append(gr.Number(label='lifetime_deposits', minimum=0, value=0, step=0.01))
                inputs.append(gr.Number(label='lifetime_bets', minimum=0, value=0))
                inputs.append(gr.Number(label='avg_bet_size', minimum=0, value=0, step=0.01))
        run_button_single_prediction = gr.Button("Run prediction")
        output = gr.Textbox(label="Prediction result", interactive=False)
    with gr.Tab("Batch prediction"):
        with gr.Column():
            input_file = gr.File(label="Upload file to be processed", file_types=[".csv"], interactive=True)
            run_button_batch_prediction = gr.Button("Run prediction")
        with gr.Column():
            output_file = gr.File(label="Download file with predictions", interactive=False)

    # Button click functions  
    run_button_single_prediction.click(fn=single_prediction, inputs=inputs, outputs=output)
    run_button_batch_prediction.click(fn=batch_prediction, inputs=input_file, outputs=output_file)

app = gr.mount_gradio_app(app, interface, path="/app")