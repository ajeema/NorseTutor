import openai
from config import Config

openai.api_key = Config.OPENAI_API_KEY

def get_system_prompt_for_difficulty(difficulty):
    if difficulty <= 1:
        return ("Du er en norsk språklærer. Snakk veldig enkelt og tydelig.")
    elif difficulty <= 3:
        return ("Du er en norsk språklærer. Bruk korte setninger og enkle ord. "
                "Gi vennlig veiledning på uttale.")
    elif difficulty <= 5:
        return ("Du er en norsk språklærer. Bruk setninger om dagligdagse temaer. "
                "Gi subtile tips om intonasjon og uttale.")
    else:
        return ("Du er en norsk språklærer. Snakk om mer komplekse emner. "
                "Gi detaljerte tilbakemeldinger om uttale, tonefall og setningsflyt.")

def generate_llm_response(user_input, difficulty, conversation_history):
    system_prompt = get_system_prompt_for_difficulty(difficulty)
    messages = [{"role": "system", "content": system_prompt}] + conversation_history + [{"role": "user", "content": user_input}]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()
