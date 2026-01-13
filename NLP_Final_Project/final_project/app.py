import streamlit as st
import pandas as pd
import numpy as np
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page configuration
st.set_page_config(
    page_title="🎬 MovieMate - AI Movie Recommender",
    page_icon="🎬",
    layout="centered"
)

# Custom CSS for movie theme
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #E50914;
        text-align: center;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .similarity-score {
        background: #E50914;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the movie data"""
    try:
        data = pd.read_csv('IMDB Top 1000 Movies.csv')
        
        # Data preprocessing
        data['Gross'] = data['Gross'].replace(',', '', regex=True)
        data['Gross'] = pd.to_numeric(data['Gross'], errors='coerce')
        
        data['Certificate'] = data['Certificate'].fillna(data['Certificate'].mode()[0])
        data['Meta_score'] = data['Meta_score'].fillna(data['Meta_score'].median())
        data['Gross'] = data['Gross'].fillna(data['Gross'].median())
        
        data['Runtime'] = data['Runtime'].str.replace(" min","").astype(float)
        data['Released_Year'] = pd.to_numeric(data['Released_Year'], errors='coerce')
        
        return data
    except FileNotFoundError:
        st.error("❌ Movie dataset not found! Please ensure 'IMDB Top 1000 Movies.csv' is in the same directory.")
        return None

@st.cache_data
def prepare_similarity_matrix(data):
    """Prepare the similarity matrix for recommendations"""
    if data is None:
        return None, None
    
    # Combine features for similarity calculation
    selected_features = ['Series_Title','Genre','Overview','Director','Star1','Star2','Star3','Star4']
    combined_features = (data['Series_Title']+' '+data['Genre']+' '+data['Overview']+' '+
                        data['Director']+' '+data['Star1']+' '+data['Star2']+' '+
                        data['Star3']+' '+data['Star4'])
    
    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)
    
    # Calculate cosine similarity
    similarity = cosine_similarity(feature_vectors)
    
    return similarity, vectorizer

def recommend_movies(movie_name, data, similarity, top_n=10):
    """
    Recommend similar movies based on a given movie name.
    """
    if data is None or similarity is None:
        return pd.DataFrame({"Message": ["Data not loaded properly"]})
    
    # List of all movie titles
    list_of_all_titles = data['Series_Title'].tolist()
    
    # Find close match
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
    if not find_close_match:
        return pd.DataFrame({"Message": [f"No close match found for '{movie_name}'"]})
    
    close_match = find_close_match[0]
    
    # Index of matched movie
    index_of_the_movie = data[data.Series_Title == close_match].index[0]
    
    # Similarity scores
    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    
    # Sort by similarity
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    
    # Collect recommendations
    recommendations = []
    for i, (index, score) in enumerate(sorted_similar_movies):
        if i == 0:  # skip the same movie
            continue
        if i > top_n:
            break
        
        movie_data = data.iloc[index]
        recommendations.append({
            "Title": movie_data['Series_Title'],
            "Similarity_Score": score,
            "Year": movie_data['Released_Year'],
            "Genre": movie_data['Genre'],
            "IMDB_Rating": movie_data['IMDB_Rating'],
            "Director": movie_data['Director'],
            "Overview": movie_data['Overview'][:200] + "..." if len(movie_data['Overview']) > 200 else movie_data['Overview']
        })
    
    return pd.DataFrame(recommendations), close_match


def main():
    # Header
    st.markdown('<h1 class="main-header">🎬 MovieMate - AI Movie Recommender</h1>', unsafe_allow_html=True)
    st.markdown("### Find your next favorite movie! 🍿")
    
    # Load data
    with st.spinner("🔄 Loading movie database..."):
        data = load_data()
        similarity, vectorizer = prepare_similarity_matrix(data)
    
    if data is None:
        st.stop()
    
    # Movie search input
    st.markdown("## 🔍 Search for a Movie")
    movie_input = st.text_input(
        "Enter a movie name:",
        placeholder="e.g., The Dark Knight, Inception, Titanic...",
        help="Start typing and we'll help you find the movie!"
    )
    
    # Show suggestions as you type
    if movie_input and len(movie_input) > 2:
        suggestions = [title for title in data['Series_Title'].tolist() 
                     if movie_input.lower() in title.lower()][:5]
        
        if suggestions:
            st.markdown("**Suggestions:**")
            suggestion_cols = st.columns(len(suggestions))
            for i, suggestion in enumerate(suggestions):
                with suggestion_cols[i]:
                    if st.button(f"🎬 {suggestion}", key=f"suggest_{suggestion}"):
                        movie_input = suggestion
                        st.experimental_rerun()
    
    # Get recommendations button
    if movie_input and st.button("🔍 Get Recommendations", type="primary"):
        with st.spinner(f"🎭 Finding movies similar to '{movie_input}'..."):
            try:
                recommendations, matched_movie = recommend_movies(
                    movie_input, data, similarity, top_n=10
                )
                
                if "Message" in recommendations.columns:
                    st.error(recommendations.iloc[0]["Message"])
                else:
                    st.session_state['recommendations'] = recommendations
                    st.session_state['matched_movie'] = matched_movie
                    st.success(f"✅ Found recommendations for: **{matched_movie}**")
                    
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
    
    # Display recommendations
    if 'recommendations' in st.session_state and not st.session_state['recommendations'].empty:
        st.markdown("---")
        st.markdown("## 🍿 Similar Movies You Might Like")
        
        recommendations = st.session_state['recommendations']
        
        # Display recommendations
        for idx, movie in recommendations.iterrows():
            with st.expander(f"🎬 {movie['Title']} ({int(movie['Year'])}) - ⭐ {movie['IMDB_Rating']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    **🎭 Genre:** {movie['Genre']}  
                    **🎬 Director:** {movie['Director']}  
                    **📝 Overview:** {movie['Overview']}
                    """)
                
                with col2:
                    similarity_percentage = movie['Similarity_Score'] * 100
                    st.markdown(f"""
                    <div class="similarity-score">
                        🎯 {similarity_percentage:.1f}% Match
                    </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
