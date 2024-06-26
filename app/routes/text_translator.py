import os
import gradio as gr
from supabase import create_client, Client
from dotenv import load_dotenv

from utils.translate.translate_deepl import translate_by_deepl_api
from utils.translate.translate_volcengine import translate_by_volcengine_api
from utils.translate.translate_hkbu_chatgpt import translate_by_hkbu_chatgpt_api
from utils.translate.translate_openrouter import translate_by_openrouter_api
from utils.translate.translate_google import translate_by_google_api
from utils.translate.translate_baichuan import translate_by_baichuan_api
from utils.translate.translate_zhipuai import translate_by_zhipuai_api

load_dotenv()
passcode_key = os.getenv("PASSCODE_KEY")
supabase_url: str = os.environ.get("SUPABASE_URL")
supabase_key: str = os.environ.get("SUPABASE_KEY")

# Create a new Supabase client
supabase: Client = create_client(supabase_url, supabase_key)

# Model Dictionary for Translate by HKBU ChatGPT API
model_dict_translate_by_hkbu_chatgpt_api = {
    "HKBU ChatGPT (gpt-35-turbo)": "gpt-35-turbo",
    "HKBU ChatGPT (gpt-4-turbo)": "gpt-4-turbo"
}

# Model Dictionary for Translate by OpenRouter API
model_dict_translate_by_openrouter_api = {
    "OpenAI (gpt-3.5-turbo-0125)": "openai/gpt-3.5-turbo-0125",
    "OpenAI (gpt-4-turbo-preview)": "openai/gpt-4-turbo-preview"
}

# Model Dictionary for Translate by Zhipu AI API
model_dict_translate_by_zhipuai_api = {
    "Zhipu AI (glm-3-turbo)": "glm-3-turbo",
    "Zhipu AI (glm-4)": "glm-4"
}


def translate_text(source_language, target_language, original_text, tone_of_voice, industry, model, passcode):
    translation_sample = None
    rationale = None
    translated_text = ""
    res_content = None
    translate_time = None
    llm_time = None

    # Check if the passcode is correct
    if passcode != passcode_key:
        return "The passcode is incorrect. Please try again."
    # Check if the source language and target language are the same
    if source_language == target_language:
        return original_text
    # Check if the original text is empty
    if original_text == "":
        return ""
    # Check if the original text is too long
    if len(original_text) > 1000:
        return "The original text is too long. Please enter a text with less than 1000 characters."

    # Generate translated text
    if model == "DeepL":
        translated_text, translate_time = translate_by_deepl_api(source_language, target_language, original_text)
    elif model == "Volcengine":
        translated_text, translate_time = translate_by_volcengine_api(source_language, target_language, original_text)
    elif model in model_dict_translate_by_hkbu_chatgpt_api:
        translation_sample, rationale, translated_text, res_content, translate_time, llm_time = translate_by_hkbu_chatgpt_api(
            source_language, target_language, original_text, tone_of_voice, industry,
            model_dict_translate_by_hkbu_chatgpt_api[model]
        )
    elif model in model_dict_translate_by_openrouter_api:
        translation_sample, rationale, translated_text, res_content, translate_time, llm_time = translate_by_openrouter_api(
            source_language, target_language, original_text, tone_of_voice, industry,
            model_dict_translate_by_openrouter_api[model]
        )
    elif model == "Google Gemini (gemini-pro)":
        translation_sample, rationale, translated_text, res_content, translate_time, llm_time = translate_by_google_api(
            source_language, target_language, original_text, tone_of_voice, industry
        )
    elif model == "Baichuan AI (Baichuan2)":
        translation_sample, rationale, translated_text, res_content, translate_time, llm_time = translate_by_baichuan_api(
            source_language, target_language, original_text, tone_of_voice, industry
        )
    elif model in model_dict_translate_by_zhipuai_api:
        translation_sample, rationale, translated_text, res_content, translate_time, llm_time = translate_by_zhipuai_api(
            source_language, target_language, original_text, tone_of_voice, industry,
            model_dict_translate_by_zhipuai_api[model]
        )

    # Insert the translation record into the database
    supabase.table("translations").insert([
        {
            "source_language": source_language,
            "target_language": target_language,
            "original_text": original_text,
            "tone_of_voice": tone_of_voice,
            "industry": industry,
            "model": model,
            "translate_sample": translation_sample,
            "rationale": rationale,
            "translated_text": translated_text,
            "res_content": res_content,
            "translate_time": translate_time,
            "llm_time": llm_time,
        }
    ]).execute()

    return translated_text


# Interface for Text Translator
text_translator = gr.Interface(
    fn=translate_text,
    inputs=[
        gr.Dropdown(
            label="Source Language",
            choices=["Chinese", "English (UK)", "English (US)", "Vietnamese", "Japanese", "Korean", "French", "German",
                     "Spanish", "Portuguese (Brazilian)", "Portuguese (European)", "Italian", "Dutch", "Polish",
                     "Russian"],
            value="Chinese"
        ),
        gr.Dropdown(
            label="Target Language",
            choices=["Chinese", "English (UK)", "English (US)", "Vietnamese", "Japanese", "Korean", "French", "German",
                     "Spanish", "Portuguese (Brazilian)", "Portuguese (European)", "Italian", "Dutch", "Polish",
                     "Russian"],
            value="Vietnamese"
        ),
        gr.Textbox(
            label="Original Text",
            placeholder="Enter the original text here",
            lines=5,
            max_lines=10
        ),
        gr.Radio(
            label="Tone of Voice",
            choices=["Standard", "Formal", "Informal"],
            value="Standard"
        ),
        gr.Dropdown(
            label="Industry Sector",
            choices=["General Fields", "Academic Papers", "Biomedicine", "Information Technology",
                     "Finance and Economics", "News and Information", "Aerospace", "Mechanical Manufacturing",
                     "Laws and Regulations", "Humanities and Social Sciences"],
            value="General Fields"
        ),
        gr.Dropdown(
            label="Model Provider (Model Name)",
            choices=["DeepL", "Volcengine",
                     "OpenAI (gpt-3.5-turbo-0125)", "OpenAI (gpt-4-turbo-preview)",
                     "HKBU ChatGPT (gpt-35-turbo)", "HKBU ChatGPT (gpt-4-turbo)",
                     "Google Gemini (gemini-pro)"],
            value="OpenAI (gpt-3.5-turbo-0125)"
        ),
        gr.Textbox(
            label="Passcode",
            placeholder="Enter the passcode here",
            type="password",
            lines=1,
            max_lines=1
        )
    ],
    outputs=[
        gr.Textbox(label="Translated Text", lines=5, max_lines=20, show_copy_button=True)
    ],
    title="FloweryTranslator - Text Translator"
)
