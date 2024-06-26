import re
import json


# Get the language code from the language name
def get_language_code(language_name):
    language_mapping = {
        "Chinese": "zh",
        "Chinese (traditional)": "zh-Hant",
        "Chinese (Hongkong traditional)": "zh-Hant-hk",
        "Chinese (Taiwan traditional)": "zh-Hant-tw",
        "Tswana": "tn",
        "Vietnamese": "vi",
        "Inuktitut": "iu",
        "Italian": "it",
        "Indonesian": "id",
        "Hindi": "hi",
        "English": "en",
        "English (UK)": "en-gb",
        "English (US)": "en-us",
        "Hiri": "ho",
        "Hebrew": "he",
        "Spanish": "es",
        "Modern Greek": "el",
        "Ukrainian": "uk",
        "Urdu": "ur",
        "Turkmen": "tk",
        "Turkish": "tr",
        "Tigrinya": "ti",
        "Tahitian": "ty",
        "Tagalog": "tl",
        "Tongan": "to",
        "Thai": "th",
        "Tamil": "ta",
        "Telugu": "te",
        "Slovenian": "sl",
        "Slovak": "sk",
        "Swati": "ss",
        "Esperanto": "eo",
        "Samoan": "sm",
        "Sango": "sg",
        "Southern Sotho": "st",
        "Swedish": "sv",
        "Japanese": "ja",
        "Twi": "tw",
        "Quechua": "qu",
        "Portuguese": "pt",
        "Portuguese (Brazilian)": "pt-br",
        "Portuguese (European)": "pt-pt",
        "Punjabi": "pa",
        "Norwegian": "no",
        "Norwegian Bokmål": "nb",
        "South Ndebele": "nr",
        "Burmese": "my",
        "Bengali": "bn",
        "Mongolian": "mn",
        "Marshallese": "mh",
        "Macedonian": "mk",
        "Malayalam": "ml",
        "Marathi": "mr",
        "Malay": "ms",
        "Luba-Katanga": "lu",
        "Romanian": "ro",
        "Lithuanian": "lt",
        "Latvian": "lv",
        "Lao": "lo",
        "Kwanyama": "kj",
        "Croatian": "hr",
        "Kannada": "kn",
        "Kikuyu": "ki",
        "Czech": "cs",
        "Catalan": "ca",
        "Dutch": "nl",
        "Korean": "ko",
        "Haitian Creole": "ht",
        "Gujarati": "gu",
        "Georgian": "ka",
        "Greenlandic": "kl",
        "Khmer": "km",
        "Ganda": "lg",
        "Kongo": "kg",
        "Finnish": "fi",
        "Fijian": "fj",
        "French": "fr",
        "Russian": "ru",
        "Ndonga": "ng",
        "German": "de",
        "Tatar": "tt",
        "Danish": "da",
        "Tsonga": "ts",
        "Chuvash": "cv",
        "Persian": "fa",
        "Bosnian": "bs",
        "Polish": "pl",
        "Bislama": "bi",
        "North Ndebele": "nd",
        "Bashkir": "ba",
        "Bulgarian": "bg",
        "Azerbaijani": "az",
        "Arabic": "ar",
        "Afrikaans": "af",
        "Albanian": "sq",
        "Abkhazian": "ab",
        "Ossetian": "os",
        "Ewe": "ee",
        "Estonian": "et",
        "Aymara": "ay",
        "Chinese (classical)": "lzh",
        "Amharic": "am",
        "Central Kurdish": "ckb",
        "Welsh": "cy",
        "Galician": "gl",
        "Hausa": "ha",
        "Armenian": "hy",
        "Igbo": "ig",
        "Northern Kurdish": "kmr",
        "Lingala": "ln",
        "Northern Sotho": "nso",
        "Chewa": "ny",
        "Oromo": "om",
        "Shona": "sn",
        "Somali": "so",
        "Serbian": "sr",
        "Swahili": "sw",
        "Xhosa": "xh",
        "Yoruba": "yo",
        "Zulu": "zu",
        "Tibetan": "bo",
        "Hokkien": "nan",
        "Wuyue Chinese": "wuu",
        "Cantonese": "yue",
        "Southwestern Mandarin": "cmn",
        "Uighur": "ug",
        "Nigerian Fulfulde": "fuv",
        "Hungarian": "hu",
        "Kamba": "kam",
        "Dholuo": "luo",
        "Kinyarwanda": "rw",
        "Umbundu": "umb",
        "Wolof": "wo"
    }

    # Return the language code or a default value if not found
    return language_mapping.get(language_name, "Unknown Language Code")


# Extract the rationale and translation from the response (json)
def extract_json_from_response(target_language, response):
    # Remove the "```" from the response
    response = response.replace("```", "")
    # Remove the initial text before the json
    response = re.sub(r".*\s*{", '{', response, count=1)
    response_data = json.loads(response)
    rationale = response_data["rationale"]
    translation = response_data[f"{target_language} translation (proofread)"]

    return rationale, translation


# Extract the rationale and translation from the response (content)
def extract_content_from_response(target_language, response):
    if "(" in target_language and ")" in target_language:
        target_language = target_language.replace("(", "\(")
        target_language = target_language.replace(")", "\)")
    # Define the regex patterns
    rationale_pattern = rf'Rationale:\n(.*?)(?:{target_language} translation \(proofread\):|$)'
    translation_pattern = rf'{target_language} translation \(proofread\):(.*?)$'

    # Extract the rationale
    rationale_match = re.search(rationale_pattern, response, re.DOTALL)
    rationale = rationale_match.group(1).strip() if rationale_match else None

    # Extract the Vietnamese translation (proofread)
    translation_match = re.search(translation_pattern, response, re.DOTALL)
    translation = translation_match.group(1).strip().strip("```").strip() if translation_match else None

    return rationale, translation
