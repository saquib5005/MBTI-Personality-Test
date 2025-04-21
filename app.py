import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Placeholder function for MBTI prediction (replace with your actual model logic)
def tellmemyMBTI(posts, name):
    # Example: A dummy classifier that predicts based on keyword matching
    traits = {
        "INTJ": ["logical", "strategic", "independent"],
        "ESFP": ["energetic", "spontaneous", "enthusiastic"],
        "INFJ": ["empathetic", "insightful", "idealistic"],
        "ENTP": ["curious", "debater", "innovative"],
    }
    scores = {trait: sum(word in " ".join(posts).lower() for word in keywords) for trait, keywords in traits.items()}
    predicted_trait = max(scores, key=scores.get)
    return predicted_trait

# Function to preprocess text
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    # Remove numbers and punctuation
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    text = re.sub(r"\d+", "", text)
    # Tokenize
    tokens = nltk.word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    # Join back into a string
    return " ".join(filtered_tokens)

# Streamlit app layout
st.title("Personality Prediction App")
st.write("Upload a file or enter text to predict your MBTI personality type!")

# Option 1: File upload
uploaded_file = st.file_uploader("Upload a text file containing your writings:", type=["txt"])
if uploaded_file is not None:
    try:
        # Read the file content
        my_writing = uploaded_file.readlines()
        my_posts = my_writing[0].decode('utf-8').split('|||')  # Split posts by separator
        st.write(f"Number of posts extracted: {len(my_posts)}")
        
        # Predict personality type
        name = st.text_input("Enter your name:", value="User")
        trait = tellmemyMBTI(my_posts, name)
        st.success(f"Predicted MBTI Type for {name}: **{trait}**")

        # Generate word cloud
        all_text = " ".join(my_posts)
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_text)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

        # Display trait explanation
        trait_explanations = {
            "INTJ": "You are strategic, logical, and independent. You enjoy planning for the future and solving complex problems.",
            "ESFP": "You are energetic, spontaneous, and enthusiastic. You thrive in social settings and love experiencing new things.",
            "INFJ": "You are empathetic, insightful, and idealistic. You care deeply about others and strive to make a positive impact.",
            "ENTP": "You are curious, innovative, and enjoy debating ideas. You love exploring possibilities and thinking outside the box.",
        }
        st.info(f"Trait Explanation: {trait_explanations.get(trait, 'No explanation available.')}")
    
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Option 2: Manual text input
else:
    input_text = st.text_area("Or describe your day/experiences manually:", height=200)
    if st.button("Predict Personality"):
        try:
            # Preprocess and split text into posts
            my_posts = [preprocess_text(input_text)]
            name = st.text_input("Enter your name:", value="User")
            trait = tellmemyMBTI(my_posts, name)
            st.success(f"Predicted MBTI Type for {name}: **{trait}**")

            # Generate word cloud
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(input_text)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)

            # Display trait explanation
            trait_explanations = {
                "INTJ": "You are strategic, logical, and independent. You enjoy planning for the future and solving complex problems.",
                "ESFP": "You are energetic, spontaneous, and enthusiastic. You thrive in social settings and love experiencing new things.",
                "INFJ": "You are empathetic, insightful, and idealistic. You care deeply about others and strive to make a positive impact.",
                "ENTP": "You are curious, innovative, and enjoy debating ideas. You love exploring possibilities and thinking outside the box.",
            }
            st.info(f"Trait Explanation: {trait_explanations.get(trait, 'No explanation available.')}")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Footer
st.markdown("""
---
**Note:** This app uses a simple keyword-based prediction model for demonstration purposes. For more accurate results, consider training a machine learning model on labeled data.
""")