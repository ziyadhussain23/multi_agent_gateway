"""
Agent C: Text Analyzer Service
A text analysis API with word count, sentiment, and statistics
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Any, Dict, List
import os
import re
from collections import Counter

app = FastAPI(
    title="Text Analyzer Agent",
    description="A text analysis service with statistics and insights",
    version="1.0.0"
)

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mount static files
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontend")), name="static")


class TextInput(BaseModel):
    text: str


class WordCount(BaseModel):
    word: str
    count: int


class TextAnalysis(BaseModel):
    character_count: int
    character_count_no_spaces: int
    word_count: int
    sentence_count: int
    paragraph_count: int
    average_word_length: float
    average_sentence_length: float
    top_words: List[WordCount]
    reading_time_minutes: float
    sentiment_score: float  # Simple sentiment: -1 to 1
    sentiment_label: str


@app.get("/")
async def serve_frontend():
    """Serve the text analyzer frontend"""
    return FileResponse(os.path.join(BASE_DIR, "frontend", "index.html"))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agent": "text-analyzer"}


def simple_sentiment(text: str) -> tuple:
    """Simple sentiment analysis based on keyword matching"""
    positive_words = {
        'good', 'great', 'awesome', 'excellent', 'amazing', 'wonderful', 
        'fantastic', 'love', 'happy', 'joy', 'beautiful', 'perfect',
        'best', 'brilliant', 'outstanding', 'superb', 'nice', 'pleasant'
    }
    negative_words = {
        'bad', 'terrible', 'awful', 'horrible', 'hate', 'sad', 'angry',
        'worst', 'poor', 'ugly', 'disappointing', 'annoying', 'frustrating',
        'boring', 'dull', 'stupid', 'wrong', 'fail', 'failure'
    }
    
    words = re.findall(r'\b\w+\b', text.lower())
    pos_count = sum(1 for w in words if w in positive_words)
    neg_count = sum(1 for w in words if w in negative_words)
    
    total = pos_count + neg_count
    if total == 0:
        return 0.0, "Neutral"
    
    score = (pos_count - neg_count) / total
    
    if score > 0.3:
        label = "Positive"
    elif score < -0.3:
        label = "Negative"
    else:
        label = "Neutral"
    
    return round(score, 2), label


@app.post("/api/analyze", response_model=TextAnalysis)
async def analyze_text(input: TextInput):
    """Analyze the provided text"""
    text = input.text
    
    # Character counts
    char_count = len(text)
    char_count_no_spaces = len(text.replace(" ", "").replace("\n", "").replace("\t", ""))
    
    # Word analysis
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words)
    
    # Sentence count (simple heuristic)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_count = len(sentences) if sentences else 1
    
    # Paragraph count
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    paragraph_count = len(paragraphs) if paragraphs else 1
    
    # Averages
    avg_word_length = sum(len(w) for w in words) / word_count if word_count > 0 else 0
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    
    # Top words (excluding common stop words)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                  'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                  'should', 'may', 'might', 'must', 'shall', 'can', 'it', 'its', 'this',
                  'that', 'these', 'those', 'i', 'you', 'he', 'she', 'we', 'they'}
    
    filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
    word_freq = Counter(filtered_words)
    top_words = [WordCount(word=word, count=count) for word, count in word_freq.most_common(10)]
    
    # Reading time (average 200 words per minute)
    reading_time = word_count / 200
    
    # Sentiment
    sentiment_score, sentiment_label = simple_sentiment(text)
    
    return TextAnalysis(
        character_count=char_count,
        character_count_no_spaces=char_count_no_spaces,
        word_count=word_count,
        sentence_count=sentence_count,
        paragraph_count=paragraph_count,
        average_word_length=round(avg_word_length, 2),
        average_sentence_length=round(avg_sentence_length, 2),
        top_words=top_words,
        reading_time_minutes=round(reading_time, 2),
        sentiment_score=sentiment_score,
        sentiment_label=sentiment_label
    )


@app.post("/api/word-count")
async def word_count(input: TextInput):
    """Get simple word count"""
    words = re.findall(r'\b\w+\b', input.text)
    return {"word_count": len(words)}


@app.post("/api/character-count")
async def character_count(input: TextInput):
    """Get character count"""
    return {
        "with_spaces": len(input.text),
        "without_spaces": len(input.text.replace(" ", ""))
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
