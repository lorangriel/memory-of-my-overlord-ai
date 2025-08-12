from openai import OpenAI

client = OpenAI()


def main():
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # replace with your model
        messages=[
            {"role": "system", "content": "Du är en hjälpsam assistent."},
            {"role": "user", "content": "Hej! Vad kan du göra?"}
        ],
        max_tokens=200,
    )
    print(response.choices[0].message["content"])


if __name__ == "__main__":
    main()
