from vertexai.preview import tokenization

model_name = "gemini-1.5-flash-002"
tokenizer = tokenization.get_tokenizer_for_model(model_name)

text = "The quick brown fox jumps over the lazy dog."
result = tokenizer.count_tokens(text)

print(f"{result.total_tokens=}")
