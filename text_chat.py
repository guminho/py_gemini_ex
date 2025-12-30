from google import genai

client = genai.Client()
chat = client.chats.create(model="gemini-3-flash-preview")

response = chat.send_message_stream("I have 2 dogs in my house.")
for chunk in response:
    print(chunk.text, end="")

print("\n\n")
response = chat.send_message_stream("How many paws are in my house?")
for chunk in response:
    print(chunk.text, end="")

print("\n\n")
for message in chat.get_history():
    print(f"role - {message.role}", end=": ")
    print(message.parts[0].text)
