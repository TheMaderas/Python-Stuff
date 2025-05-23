"""
Utility for text analysis and natural language processing.
This script provides functions to analyze texts, extract information, and perform basic analyses.
"""
import re
import argparse
import collections
import string
import os
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import ssl
import socket
import zipfile

ssl._create_default_https_context = ssl._create_unverified_context
socket.setdefaulttimeout(10)

def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    
    try:
        nltk.data.find('corpora/wordnet')
    except (LookupError, zipfile.BadZipFile):
        try:
            nltk.download('wordnet', quiet=True)
        except Exception as e:
            print(f"Warning: Unable to download WordNet data. {str(e)}")

def read_text_file(file_path):
    """
    Reads the contents of a text file.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: File contents
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return ""

def basic_text_stats(text):
    """
    Gets basic statistics of a text.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        dict: Text statistics
    """
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    character_count = len(text)
    word_count = len(words)
    sentence_count = len(sentences)
    avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    unique_words = set(word.lower() for word in words if word.isalpha())
    unique_word_count = len(unique_words)
    lexical_diversity = unique_word_count / word_count if word_count > 0 else 0
    
    return {
        'character_count': character_count,
        'word_count': word_count,
        'sentence_count': sentence_count,
        'avg_word_length': avg_word_length,
        'avg_sentence_length': avg_sentence_length,
        'unique_word_count': unique_word_count,
        'lexical_diversity': lexical_diversity
    }

def extract_frequent_words(text, top_n=10, include_stopwords=False, language='english'):
    """
    Extracts the most frequent words from a text.
    
    Args:
        text (str): Text to analyze
        top_n (int): Number of words to return
        include_stopwords (bool): If True, includes common words (stopwords)
        language (str): Language for stopwords
        
    Returns:
        list: List of tuples (word, frequency)
    """
    words = word_tokenize(text.lower())
    if not include_stopwords:
        stop_words = set(stopwords.words(language))
        words = [word for word in words if word.isalpha() and word not in stop_words]
    else:
        words = [word for word in words if word.isalpha()]
    word_freq = collections.Counter(words)
    return word_freq.most_common(top_n)

def generate_word_cloud(text, output_file=None, width=800, height=400, include_stopwords=False, language='english'):
    """
    Generates a word cloud from a text.
    
    Args:
        text (str): Text to analyze
        output_file (str): Path to save the image
        width (int): Image width
        height (int): Image height
        include_stopwords (bool): If True, includes common words (stopwords)
        language (str): Language for stopwords
        
    Returns:
        WordCloud: Generated WordCloud object
    """
    if not include_stopwords:
        stop_words = set(stopwords.words(language))
    else:
        stop_words = set()
    wordcloud = WordCloud(
        width=width, 
        height=height,
        background_color='white',
        stopwords=stop_words,
        min_font_size=10,
        max_font_size=100,
        contour_width=3,
        contour_color='steelblue'
    ).generate(text)
    plt.figure(figsize=(width/100, height/100), dpi=100)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    if output_file:
        plt.savefig(output_file, bbox_inches='tight')
        print(f"Word cloud saved at: {output_file}")
    else:
        plt.show()
    return wordcloud

def analyze_sentiment_basic(text):
    """
    Performs a basic sentiment analysis using keywords.
    This is a simplified version, without ML.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        dict: Analysis result
    """
    positive_words = {
        'english': ['good', 'great', 'excellent', 'happy', 'love', 'best', 'wonderful', 
                   'fantastic', 'amazing', 'beautiful', 'nice', 'awesome', 'super', 
                   'positive', 'perfect', 'enjoy', 'like', 'fun', 'impressed'],
        'portuguese': ['bom', 'ótimo', 'excelente', 'feliz', 'amor', 'melhor', 'maravilhoso',
                      'fantástico', 'incrível', 'bonito', 'legal', 'impressionante', 
                      'positivo', 'perfeito', 'gosto', 'divertido', 'impressionado']
    }
    
    negative_words = {
        'english': ['bad', 'terrible', 'awful', 'worst', 'hate', 'horrible', 'poor',
                   'disappointing', 'sad', 'angry', 'negative', 'annoying', 'wrong',
                   'problem', 'difficult', 'dislike', 'boring', 'ugly'],
        'portuguese': ['ruim', 'terrível', 'horrível', 'pior', 'odeio', 'péssimo',
                      'decepcionante', 'triste', 'raiva', 'negativo', 'irritante',
                      'errado', 'problema', 'difícil', 'chato', 'feio']
    }
    
    words = word_tokenize(text.lower())
    pt_count = sum(1 for word in words if word in positive_words['portuguese'] or word in negative_words['portuguese'])
    en_count = sum(1 for word in words if word in positive_words['english'] or word in negative_words['english'])
    language = 'portuguese' if pt_count > en_count else 'english'
    positive_count = sum(1 for word in words if word in positive_words[language])
    negative_count = sum(1 for word in words if word in negative_words[language])
    total_count = positive_count + negative_count
    if total_count > 0:
        positive_score = positive_count / total_count
        negative_score = negative_count / total_count
    else:
        positive_score = 0.5
        negative_score = 0.5
    if positive_score > negative_score:
        sentiment = "positive"
        score = positive_score
    elif negative_score > positive_score:
        sentiment = "negative"
        score = negative_score
    else:
        sentiment = "neutral"
        score = 0.5
    
    return {
        'sentiment': sentiment,
        'score': score,
        'positive_words': positive_count,
        'negative_words': negative_count,
        'language': language
    }

def extract_entities_basic(text):
    """
    Extracts basic entities like emails, URLs, dates, etc.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        dict: Extracted entities
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    url_pattern = r'https?://[^\s]+'
    phone_pattern = r'(?:\+\d{1,3}\s?)?\(?\d{2,3}\)?[\s.-]?\d{3,5}[\s.-]?\d{4}'
    date_pattern = r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}'
    money_pattern = r'[$€£¥]\s?\d+(?:[.,]\d+)?|\d+(?:[.,]\d+)?\s?[$€£¥]'
    hashtag_pattern = r'#[a-zA-Z0-9_]+'
    emails = re.findall(email_pattern, text)
    urls = re.findall(url_pattern, text)
    phones = re.findall(phone_pattern, text)
    dates = re.findall(date_pattern, text)
    money = re.findall(money_pattern, text)
    hashtags = re.findall(hashtag_pattern, text)
    
    return {
        'emails': emails,
        'urls': urls,
        'phones': phones,
        'dates': dates,
        'money': money,
        'hashtags': hashtags
    }

def text_summary_basic(text, sentences=3):
    """
    Creates a basic summary of text by selecting the most relevant sentences.
    
    Args:
        text (str): Text to summarize
        sentences (int): Number of sentences in the summary
        
    Returns:
        str: Text summary
    """
    sents = sent_tokenize(text)
    if len(sents) <= sentences:
        return text
    stop_words = set(stopwords.words('english')).union(set(stopwords.words('portuguese')))
    word_tokens = word_tokenize(text.lower())
    filtered_words = [word for word in word_tokens if word.isalpha() and word not in stop_words]
    word_freq = collections.Counter(filtered_words)
    sent_scores = {}
    for i, sent in enumerate(sents):
        words = word_tokenize(sent.lower())
        score = sum(word_freq[word] for word in words if word in word_freq)
        sent_scores[i] = score / (len(words) + 1)
    top_indices = sorted(sent_scores, key=sent_scores.get, reverse=True)[:sentences]
    top_indices.sort()
    summary = " ".join(sents[i] for i in top_indices)
    
    return summary

def main():
    download_nltk_data()
    file_path = input("Enter path to text file: ").strip()
    if not file_path or not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return
    text = read_text_file(file_path)
    if not text:
        print("Error: Could not read file or file is empty.")
        return

    options = {
        '1': 'Basic Statistics',
        '2': 'Frequent Words',
        '3': 'Entities Extraction',
        '4': 'Sentiment Analysis',
        '5': 'Summary',
        '6': 'Generate Word Cloud',
        '0': 'All Analyses'
    }
    print("\nSelect analysis to perform:")
    for key, desc in options.items():
        print(f"{key}) {desc}")
    choice = input("Enter option number: ").strip()
    print("\nResults:\n" + '-'*40)

    if choice == '1' or choice == '0':
        stats = basic_text_stats(text)
        print("--- BASIC STATISTICS ---")
        for k, v in stats.items():
            print(f"{k.replace('_', ' ').title()}: {v}")
        print('-'*40)
    if choice == '2' or choice == '0':
        n = int(input("Number of top words [default 10]: ") or 10)
        freq = extract_frequent_words(text, top_n=n)
        print(f"--- TOP {n} FREQUENT WORDS ---")
        for w, c in freq:
            print(f"{w}: {c}")
        print('-'*40)
    if choice == '3' or choice == '0':
        ents = extract_entities_basic(text)
        print("--- ENTITIES ---")
        for t, items in ents.items():
            print(f"{t.title()}: {', '.join(items[:5])}...")
        print('-'*40)
    if choice == '4' or choice == '0':
        sent = analyze_sentiment_basic(text)
        print("--- SENTIMENT ---")
        print(f"Sentiment: {sent['sentiment'].title()}, Score: {sent['score']:.2f}")
        print('-'*40)
    if choice == '5' or choice == '0':
        sents = int(input("Number of sentences for summary [default 3]: ") or 3)
        summary = text_summary_basic(text, sentences=sents)
        print(f"--- SUMMARY ({sents} sentences) ---")
        print(summary)
        print('-'*40)
    if choice == '6' or choice == '0':
        out = input("Word cloud output file [default none]: ").strip() or None
        print("Generating word cloud...")
        generate_word_cloud(text, out)

if __name__ == '__main__':
    main()
