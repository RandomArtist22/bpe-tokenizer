with open("data/corpus.txt", "rb") as f:
    data = f.read()
tokens = list(data)
unique_tokens = list(set(tokens))

print(f"Corpus: {len(tokens)} bytes")
print(f"Initial tokens: {len(tokens)}")
print(f"Unique byte values seen: {len(unique_tokens)}\n")

token_pairs = {}

for i in range(1, len(tokens)):
    if token_pairs.get((tokens[i - 1], tokens[i])):
        token_pairs[(tokens[i - 1], tokens[i])] += 1
    else:
        token_pairs[(tokens[i - 1], tokens[i])] = 1

token_pairs_sorted = dict(
    sorted(token_pairs.items(), key=lambda item: item[1], reverse=True)
)
keys_sorted = list(token_pairs_sorted.keys())
print("Top 20 pairs:")
for i in range(20):
    print(
        f"({keys_sorted[i][0]:<3},{keys_sorted[i][1]:<3})  '{bytes(keys_sorted[i]).decode('latin-1'):<2}'  ->  {token_pairs_sorted[keys_sorted[i]]:<10}"
    )
