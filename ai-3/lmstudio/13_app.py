import lmstudio as lms

model = lms.embedding_model('text-embedding-nomic-embed-text-v1.5-embedding')

embedding = model.embed('Hello World!')
print(embedding)