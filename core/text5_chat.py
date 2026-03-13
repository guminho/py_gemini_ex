from google import genai

client = genai.Client()
model = "gemini-3-flash-preview"
chat = client.chats.create(model=model)

response = chat.send_message("I have 2 dogs in my house.")
print(f"{response.text=}")

response = chat.send_message("How many paws are in my house?")
print(f"{response.text=}")

for msg in chat.get_history():
    print(f"\n[{msg.role}]:\n{msg.parts[0].text}")
