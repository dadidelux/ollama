import gradio as gr
import ollama

model= 'llama2:7b-chat-q3_K_L'

def format_history(msg: str, history: list[list[str, str]], system_prompt: str):
    chat_history = [{"role": "system", "content":system_prompt}]
    for query, response in history:
        chat_history.append({"role": "user", "content": query})
        chat_history.append({"role": "assistant", "content": response})  
    chat_history.append({"role": "user", "content": msg})
    return chat_history

def generate_response(msg: str, history: list[list[str, str]], system_prompt: str):
    chat_history = format_history(msg, history, system_prompt)
    response = ollama.chat(model=model, stream=True, messages=chat_history)
    message = ""
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        message += token
        yield message

chatbot = gr.ChatInterface(
                generate_response,
                chatbot=gr.Chatbot(
                        avatar_images=["user.png", "chatbot.webp"],
                        height="64vh"
                    ),
                additional_inputs=[
                    gr.Textbox(
                        """You are a worker that summarizes the contents given to you given a json template below.
                                    {
                            "company_name": "{{company_name}}",
                            "company_services": [
                                "{{service_1}}",
                                "{{service_2}}",
                                "{{service_3}}",
                                ...
                            ],
                            "company_contact_details": {
                                "phone_numbers": {
                                "United States": "{{US_phone_number}}",
                                "Canada": "{{Canada_phone_number}}"
                                },
                                "email_addresses": {
                                "General Inquiries": "{{general_email}}",
                                "Career Opportunities": "{{careers_email}}",
                                "Fraud Reporting": "{{fraud_email}}"
                                },
                                "office_locations": [
                                "{{location_1}}",
                                "{{location_2}}",
                                ...
                                ],
                                "website": "{{website_url}}",
                                "social_media_links": {
                                "Facebook": "{{facebook_link}}",
                                "Instagram": "{{instagram_link}}",
                                "Twitter": "{{twitter_link}}",
                                "LinkedIn": "{{linkedin_link}}"
                                }
                            },
                            "company_history": "{{company_history}}",
                            "job_openings": [
                                "{{job_opening_1}}",
                                "{{job_opening_2}}",
                                ...
                            ],
                            "employee_size": "{{employee_size}}",
                            "key_people": [
                                {
                                "name": "{{person_1_name}}",
                                "title": "{{person_1_title}}"
                                },
                                {
                                "name": "{{person_2_name}}",
                                "title": "{{person_2_title}}"
                                },
                                ...
                            ]
                            }
                        """,
                        label="System Prompt"
                    )
                ],
                title="Open Source LLM" + "model: " +model,
                description="Feel free to ask any question.",
                theme="soft",
                submit_btn="⬅ Send",
                retry_btn="🔄 Regenerate Response",
                undo_btn="↩ Delete Previous",
                clear_btn="🗑️ Clear Chat"
)

chatbot.launch()