from textblob import TextBlob

# This function takes a string input and returns the sentiment of the text.
def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"
    
# Example usage
if __name__ == "__main__":
    text = "I love programming!"
    sentiment = analyze_sentiment(text)
    print(f"The sentiment of the text is: {sentiment}")
