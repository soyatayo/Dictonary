def load_data(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        headers = file.readline().strip().split(',')
        for line in file:
            row = line.strip().split(',')
            if len(row) != len(headers):
                # Handle misaligned columns by joining extra columns
                row = handle_misaligned_columns(row, headers)
            data.append(dict(zip(headers, row)))
    return data

def handle_misaligned_columns(row, headers):
    # Join extra columns to the last column
    if len(row) > len(headers):
        row[len(headers) - 1] = ','.join(row[len(headers) - 1:])
        row = row[:len(headers)]
    return row

def preprocess_text(text):
    text = ''.join(char.lower() if char.isalnum() or char.isspace() else ' ' for char in text)
    words = text.split()
    return words

def count_words(words):
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

def most_common_words_by_rating(data):
    rating_reviews = {}
    
    for row in data:
        if 'Certificate' not in row or 'Review' not in row:
            continue
        
        rating = row['Certificate']
        review = row['Review']
        if rating not in rating_reviews:
            rating_reviews[rating] = []
        rating_reviews[rating].append(review)
    
    common_words = {}
    
    for rating, reviews in rating_reviews.items():
        all_words = []
        for review in reviews:
            words = preprocess_text(review)
            all_words.extend(words)
        
        word_counts = count_words(all_words)
        sorted_word_counts = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
        common_words[rating] = sorted_word_counts[:10]  # Get 10 most common words
    
    return common_words

# Load the dataset
file_path = r'C:\Users\sharo\OneDrive\Documents\Intro to informatics\imdb-movies-dataset.csv'
data = load_data(file_path)

# Get the most common words for each certificate rating
common_words = most_common_words_by_rating(data)

# Print the results
for rating, words in common_words.items():
    print(f"Certificate Rating: {rating}")
    for word, count in words:
        print(f"{word}: {count}")
    print()