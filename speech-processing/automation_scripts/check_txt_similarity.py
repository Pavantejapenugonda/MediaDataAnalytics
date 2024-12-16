#!pip install scikit-learn

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib

# When you run this code, you will get a similarity score followed by a list of differences, where:

# Words present in sentence1 are prefixed with a space.
# Words present in sentence2 but not in sentence1 are prefixed with a -.
# Words in sentence1 that do not appear in sentence2 are prefixed with a +.


# Function to read a text file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Read the two text files
text1 = read_file('org_file.txt')
text2 = read_file('file1.txt')

# Create a TF-IDF Vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the sentences
tfidf_matrix = vectorizer.fit_transform([text1, text2])

# Compute cosine similarity
similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
similarity_score = similarity_matrix[0][0]
print(f"Similarity Score : {similarity_score}")

# Highlight differences using difflib
differ = difflib.Differ()
diff = differ.compare(text1.split(), text2.split())

# Prepare output
output = []
output.append(f"Similarity between the two sentences: {similarity_score:.4f}\n")
output.append("Differences:\n")
output.append('\n'.join(diff))

# Write to a text file
with open('sentence_comparison.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(output))

print("Comparison results written to 'sentence_comparison.txt'.")
