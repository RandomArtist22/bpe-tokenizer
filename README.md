# bpe-tokenizer

Byte-level BPE tokenizer written from scratch. Training is in Python. Inference will be in C.

## Status

- [x] Training
- [x] Merges and vocab serialization
- [ ] Encode
- [ ] Decode + C port
- [ ] Benchmark against tiktoken

## Training

The corpus is the Complete Works of Shakespeare from Project Gutenberg (5.6 MB).

```
curl -L https://www.gutenberg.org/cache/epub/100/pg100.txt -o data/corpus.txt
python tools/train_bpe.py
```

Run the scripts from the repo root, since the paths are relative.

The trainer splits the text on spaces and works on a `{word: count}` table, not on one flat list of tokens. A pair inside a word that appears 10k times is counted once and weighted by 10k. The flat-list version was too slow in Python.

A merge never crosses a space. Newlines don't split words, so `\r\n` is the first merge.

500 merges give 2.24x compression, with a vocab size of 756.

## Files

`data/merges.txt`: the merge count on the first line, then one `a b new_id` per line in rank order.

`data/vocab.json`: maps each token id to its bytes, base64-encoded. On load, every merge is checked with `vocab[new_id] == vocab[a] + vocab[b]`.

`tools/inspect_corpus.py`: prints the byte count and the 20 most common byte pairs.
