import os
import gradio as gr
from utils.translate.translate_deepl import translate_by_deepl_api
from utils.translate.translate_volcengine import translate_by_volcengine_api
from utils.translate.translate_hkbu_chatgpt import translate_by_hkbu_chatgpt_api
from utils.translate.translate_openai import translate_by_openai_api
from utils.translate.translate_google import translate_by_google_api
from utils.translate.translate_baichuan import translate_by_baichuan_api
from utils.translate.translate_zhipuai import translate_by_zhipuai_api
from dotenv import load_dotenv

load_dotenv()
passcode_key = os.getenv("PASSCODE_KEY")


def translate_text(source_language, target_language, original_text, tone_of_voice, industry, model, passcode):
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
    translated_text = ""
    if model == "DeepL":
        translated_text = translate_by_deepl_api(source_language, target_language, original_text)
    elif model == "Volcengine":
        translated_text = translate_by_volcengine_api(source_language, target_language, original_text)
    elif model == "HKBU ChatGPT (gpt-35-turbo-16k)":
        translation_sample, translated_text = translate_by_hkbu_chatgpt_api(
            source_language, target_language, original_text, tone_of_voice, industry, "gpt-35-turbo-16k"
        )
    elif model == "HKBU ChatGPT (gpt-4-turbo)":
        translation_sample, translated_text = translate_by_hkbu_chatgpt_api(
            source_language, target_language, original_text, tone_of_voice, industry, "gpt-4-turbo"
        )
    elif model == "OpenAI (gpt-3.5-turbo-1106)":
        translation_sample, translated_text = translate_by_openai_api(
            source_language, target_language, original_text, tone_of_voice, industry, "gpt-3.5-turbo-1106"
        )
    elif model == "OpenAI (gpt-4-0125-preview)":
        translation_sample, translated_text = translate_by_openai_api(
            source_language, target_language, original_text, tone_of_voice, industry, "gpt-4-0125-preview"
        )
    elif model == "Google Gemini (gemini-pro)":
        translation_sample, translated_text = translate_by_google_api(
            source_language, target_language, original_text, tone_of_voice, industry
        )
    elif model == "Baichuan AI (Baichuan2)":
        translation_sample, translated_text = translate_by_baichuan_api(
            source_language, target_language, original_text, tone_of_voice, industry
        )
    elif model == "Zhipu AI (glm-3-turbo)":
        translation_sample, translated_text = translate_by_zhipuai_api(
            source_language, target_language, original_text, tone_of_voice, industry, "glm-3-turbo"
        )
    elif model == "Zhipu AI (glm-4)":
        translation_sample, translated_text = translate_by_zhipuai_api(
            source_language, target_language, original_text, tone_of_voice, industry, "glm-4"
        )

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
            choices=["DeepL", "Volcengine", "HKBU ChatGPT (gpt-35-turbo-16k)", "HKBU ChatGPT (gpt-4-turbo)",
                     "OpenAI (gpt-3.5-turbo-1106)", "OpenAI (gpt-4-0125-preview)", "Google Gemini (gemini-pro)",
                     "Baichuan AI (Baichuan2)", "Zhipu AI (glm-3-turbo)", "Zhipu AI (glm-4)"],
            value="OpenAI (gpt-3.5-turbo-1106)"
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
