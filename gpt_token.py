import tiktoken

def count_tokens(text, model="gpt-4o"):
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)

    return len(tokens)

# 테스트
text = "Hello World!"
print("Token Count:", count_tokens(text))

with open("script_formal.txt", 'r', encoding='utf-8') as f:
    sentences =  f.readlines()

sentences_list = []

for i in range(0, len(sentences), 100):
    sentences_list.append(sentences[i:i+100])

print(sentences_list[0])

sentences_sum = ''

for i in range(len(sentences_list[0])):
    sentences_sum += '%d. '%(i+1) + sentences_list[0][i]

print(sentences_sum)