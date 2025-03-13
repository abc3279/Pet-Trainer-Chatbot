with open ('script_rmqa_formal.txt', 'r', encoding='utf-8') as f:
    sentences = f.readlines()

print(len(sentences))

sentences = list(set(sentences))

with open('script_rmqa_formal_rmdup.txt', 'w', encoding='utf-8') as f:
    f.writelines(sentences)