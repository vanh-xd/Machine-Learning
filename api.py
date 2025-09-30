from openai import OpenAI
client = OpenAI(api_key="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")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant!"},
        {"role": "user", "content": "chợ nổi tiếng nhất sài gòn?"}
    ],
)

print(response.choices[0].message.content)