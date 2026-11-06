from collections import Counter
import json, base64


def merge(tokens, pair, new_id):
    result = []
    i = 0
    while i < len(tokens):
        if i < len(tokens) - 1 and (tokens[i], tokens[i + 1]) == pair:
            result.append(new_id)
            i += 2
        else:
            result.append(tokens[i])
            i += 1
    return tuple(result)


def merge_in_table(word_tokens, pair, new_id):
    return {merge(tokens, pair, new_id): freq for tokens, freq in word_tokens.items()}


def count_pairs(word_tokens):
    counts = {}
    for tokens, freq in word_tokens.items():
        for a, b in zip(tokens, tokens[1:]):
            counts[(a, b)] = counts.get((a, b), 0) + freq
    return counts


def write_vocab(path, vocab):
    vocab_serializable = {
        str(k): base64.b64encode(v).decode("utf-8", errors="replace")
        for k, v in vocab.items()
    }
    with open(path, "w") as f:
        json.dump(vocab_serializable, f)
    print(f"Sucessfully saved vocab at {path}")


def write_merges(path, merges):
    with open(path, "w") as f:
        f.write(f"{len(merges)}\n")
        for i in range(len(merges)):
            f.write(f"{merges[i][0]} {merges[i][1]} {merges[i][2]}\n")
    print(f"Sucessfully saved merges at {path}")


def load_tokenizer(vocab_path, merge_path):
    with open(vocab_path, "r") as f:
        raw = json.load(f)
    vocab = {int(k): base64.b64decode(v) for k, v in raw.items()}
    with open(merge_path, "r") as f:
        lines = f.readlines()
    N = int(lines[0])
    for i in range(N):
        a, b, c = map(int, lines[i + 1].split())
        assert vocab[c] == vocab[a] + vocab[b], (
            f"Mismatch at {c}: Expected {vocab[a] + vocab[b]} got {vocab[c]}"
        )
    print("vocab: OK")
    return vocab


with open("data/corpus.txt", "rb") as f:
    data = f.read()
text = data.decode("utf-8")
words = text.split(" ")
word_freq = Counter(words)

word_tokens = {tuple(w.encode("utf-8")): freq for w, freq in word_freq.items() if w}
initial_len = sum([(len(tokens) * freq) for tokens, freq in word_tokens.items()])
tot_tokens = initial_len
vocab = {i: bytes([i]) for i in range(256)}
N = 500
merges = []
for n in range(N):
    token_pairs = count_pairs(word_tokens)
    best = max(token_pairs, key=token_pairs.get)
    new_id = 256 + n
    vocab[new_id] = vocab[best[0]] + vocab[best[1]]
    merges.append(best + (new_id,))
    word_tokens = merge_in_table(word_tokens, best, new_id)
    print(f"Merge {n + 1}, {best} -> {new_id} '{vocab[new_id].decode('latin-1')!r}'")
tot_tokens = sum([(len(tokens) * freq) for tokens, freq in word_tokens.items()])
print(f"Initial tokens: {initial_len}\nFinal tokens: {tot_tokens}")
print(f"Compression: {initial_len / tot_tokens}x")
print(f"Vocabulary size: {len(vocab)} (256 bytes + {len(vocab) - 256} merges)")

write_vocab("data/vocab.json", vocab)
write_merges("data/merges.txt", merges)
load_tokenizer("data/vocab.json", "data/merges.txt")
