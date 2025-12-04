# Text Analyzer Agent

Analyze text for statistics, word frequency, and sentiment.

## Features
- Word, character, sentence counts
- Top word frequency
- Simple sentiment analysis
- Reading time estimation
- Clean web interface

## Run Standalone

```bash
chmod +x run.sh
./run.sh
```

Then open: http://localhost:8003

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface |
| POST | `/api/analyze` | Full text analysis |
| POST | `/api/word-count` | Word count only |
| POST | `/api/character-count` | Character count |

## Example

```bash
curl -X POST http://localhost:8003/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a great example. I love it!"}'
```

## Response

```json
{
  "character_count": 37,
  "word_count": 8,
  "sentence_count": 2,
  "sentiment_label": "Positive",
  "top_words": [{"word": "great", "count": 1}, ...]
}
```
