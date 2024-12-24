import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(verbose=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def classify_text(text):
    prompt = f"""
    Please classify the following news text: "{text}".
    Is it about a terrorism event? Respond with "Yes" or "No" and provide a short explanation.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that classifies news."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == '__main__':
    news_text = "A bomb exploded in the city center, causing multiple casualties."
    result = classify_text(news_text)
    print("Classification Result:", result)
