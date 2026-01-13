# 🎬 MovieMate - AI Movie Recommender

A simple and elegant Streamlit web application that recommends movies using machine learning and natural language processing.

## What Does This App Do?

MovieMate helps you discover new movies by analyzing your favorite films and finding similar ones from the IMDB Top 1000 Movies database. Simply enter a movie you love and the AI will recommend movies with similar themes, genres, directors and cast members.

## Complete Setup Guide 
### Step 1: Prerequisites

Make sure you have Python installed on your system:
- **Python 3.7 or higher** 
- **pip** 

To check if you have Python:
```bash
python --version
```

### Step 2: Download the Project

1. **Download all project files** to a folder on your computer:
   - `app.py` - Main application
   - `requirements.txt` - Dependencies list
   - `run_app.py` - Easy launcher script
   - `IMDB Top 1000 Movies.csv` - Movie dataset
   - `README.md` - This file

2. **Navigate to the project folder** in your terminal/command prompt:
   ```bash
   cd /path/to/your/movie-recommender-folder
   ```

### Step 3: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

**What gets installed:**
- `streamlit` - Web app framework
- `pandas` - Data manipulation
- `scikit-learn` - Machine learning algorithms
- `numpy` - Numerical computing
- And other supporting libraries

### Step 4: Run the Application

**Method 1: Easy Launcher**
```bash
python run_app.py
```

**Method 2: Direct Streamlit Command**
```bash
streamlit run_app.py
```

### Step 5: Use the App

1. **Open your web browser** - The app automatically opens at `http://localhost:8501`
2. **Enter a movie name** in the search box
3. **Use autocomplete suggestions** for accurate movie selection
4. **Click "Get Recommendations"**
5. **Browse similar movies** with similarity scores and details

## Project Structure

```
📁 The Project Folder/
├── 🎬 app.py                    # Main Streamlit application
├── 📊 IMDB Top 1000 Movies.csv  # Movie dataset (1000 movies)
├── 📋 requirements.txt          # Python dependencies
├── 🚀 run_app.py               # Easy launcher script
└── 📖 README.md                # This documentation
```

## 🧠 How the AI Recommendation Works

### The Process:
1. **Data Loading**: Loads IMDB Top 1000 Movies dataset
2. **Text Processing**: Combines movie features (title, genre, overview, director, cast)
3. **Vectorization**: Converts text to numerical vectors using TF-IDF
4. **Similarity Calculation**: Uses cosine similarity to find similar movies
5. **Smart Matching**: Handles typos and partial matches in movie names
6. **Ranking**: Shows top 10 most similar movies with match percentages

### Technical Stack:
- **Frontend**: Streamlit (Python web framework)
- **ML Algorithm**: TF-IDF + Cosine Similarity
- **Data Processing**: Pandas, NumPy
- **Text Matching**: Difflib for fuzzy string matching

## App Features

**Simple Interface** - Clean, movie-themed design  
**Smart Search** - Autocomplete suggestions as you type  
**AI Recommendations** - Machine learning-powered suggestions  
**Movie Details** - Genre, director, rating, and overview  
**Similarity Scores** - See how closely movies match (percentage)  
**Fuzzy Matching** - Works even with slight spelling errors  

## Dataset Information

**IMDB Top 1000 Movies** includes:
- 🎬 1,000 highest-rated movies on IMDB
- 📅 Movies from 1920-2020
- 🎭 Multiple genres: Action, Drama, Comedy, Thriller, etc.
- ⭐ IMDB ratings, box office data, cast & crew info
- 📝 Movie overviews and detailed metadata

## Example Usage

**Input:** "The Dark Knight"  
**Output:** Movies like:
- Batman Begins (29.8% match)
- The Dark Knight Rises (29.3% match)
- The Prestige (15.3% match)
- Joker (12.4% match)
- And more...
