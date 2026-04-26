from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

model = SentenceTransformer('all-MiniLM-L6-v2')

text = "This is a test sentence"
embedding = model.encode(text)

print("Embedding generated successfully!")
print("First 5 values:", embedding[:5])