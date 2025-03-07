# RAG (Retrieval Augmented Generation) Project

## What is RAG?
RAG (Retrieval Augmented Generation) is a hybrid AI architecture that combines two key capabilities:
1. **Information Retrieval**: Fetching relevant information from a knowledge base
2. **Text Generation**: Using language models to generate coherent responses

The main advantage of RAG is that it grounds language model outputs in factual, retrievable information, reducing hallucinations and improving accuracy.

## Types of RAG Evaluation
There are several approaches to evaluating RAG systems, each suited for different contexts:

### 1. Retrieval Evaluation
**Best for**: Search engines, document retrieval systems
- **Metrics**: Precision, Recall, F1-Score
- **Advantages**: 
  - Objective measurements
  - Easy to automate
- **Disadvantages**: 
  - Doesn't evaluate response quality
  - Requires labeled relevant documents

### 2. Response Evaluation
**Best for**: Chatbots, Q&A systems
- **Metrics**: Relevance, Context Usage, Coherence
- **Advantages**:
  - Evaluates actual output quality
  - Immediate feedback
- **Disadvantages**:
  - More subjective
  - Harder to automate perfectly

### 3. LLM-based Evaluation
**Best for**: Complex reasoning tasks, fact-checking
- **Characteristics**:
  - Uses AI to evaluate AI
  - Can check factual accuracy
  - Evaluates semantic understanding
- **Trade-offs**:
  - More sophisticated evaluation
  - Computationally expensive
  - May inherit LLM biases

### 4. Human Evaluation
**Best for**: High-stakes applications, baseline creation
- **Aspects**:
  - Information accuracy
  - Response usefulness
  - Overall quality
- **Trade-offs**:
  - Most accurate
  - Not scalable
  - Expensive and time-consuming

## Overview
This project implements a RAG system that combines information retrieval with text generation to provide accurate, context-based responses. The system uses Hugging Face models for text generation and implements a response evaluation mechanism.

## Why Response Evaluation?
We chose to focus on response evaluation because:
- It's simpler and more efficient for our context
- Effectively measures response quality against provided context
- Particularly useful for chatbot applications with specific knowledge bases
- Provides immediate feedback on response quality
- Helps identify and prevent hallucinations

## Project Structure
The project follows a modular architecture, with components organized as follows:

1. **Utils Components**:
   - Provider configurations
   - Decorators for timeout handling
   - Logging setup

2. **Core Components**:
   - `evaluation.py`: Implements response quality assessment
   - `prompt_templates.py`: Manages context formatting
   - `text_generation.py`: Handles text generation with models

3. **Integration Components**:
   - `rag_handler.py`: Combines retrieval and generation
   - `rag_service.py`: Orchestrates the RAG process
   - `views.py`: Exposes the API endpoints

4. **Knowledge Base**:
   - `knowledge_base.json`: A simulation of science and technology data
   - Serves as the contextual information source for RAG
   - Can be populated from various sources:
     * Structured datasets
     * CSV file conversions
     * Database extractions
   - Current implementation focuses on tech and science topics
   - Easily extensible for different domains or data sources

## Flow
```
Utils -> Evaluation -> Prompt Templates -> Text Generation -> RAG Handler -> RAG Service -> Views
```

## API Usage

### Endpoint
```
GET http://localhost:8002/rag/{model}/?query={your_query}
```
Where `{model}` can be:
- `gpt2`
- `deepseek`

### Example Request
```
http://localhost:8002/rag/gpt2/?query=What is tecnology?
```

### Example Response
```json
{
    "query": "What is tecnology?",
    "context": [
        "The World Wide Web (WWW) is an information system...",
        "Artificial Intelligence (AI) is the simulation of human intelligence...",
        // Additional context entries...
    ],
    "response": "Technology is...",
    "model": "gpt2",
    "evaluation": {
        "overall_score": 36.55,
        "relevance_score": 4.57,
        "context_usage": 5.09,
        "length_score": 100.0,
        "response_length": 82,
        "feedback": [
            "The answer could be more focused on addressing the specific question.",
            "The answer could make better use of the provided context information.",
            "Comprehensive answer with appropriate length and detail.",
            "The response needs significant improvement to better address the question."
        ]
    }
}
```

## Evaluation Metrics
The system evaluates responses based on:
- **Overall Score**: Combined evaluation of all metrics
- **Relevance Score**: How well the response addresses the query
- **Context Usage**: How effectively the context is utilized
- **Length Score**: Appropriateness of response length
- **Feedback**: Specific improvement suggestions

## Technical Details
- Built with Python and Django
- Uses Hugging Face Transformers
- Implements timeout handling for reliability
- Includes comprehensive logging
- Modular and extensible architecture

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)
- Git

### Installation Steps

1. **Clone the Repository**

2. **Create and Activate Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Set Up Django**
```bash
python manage.py migrate
python manage.py collectstatic
```

5. **Configure Environment Variables**
Create a `.env` file in the root directory:
```env
DEEPSEEK_API_KEY=123xxxxxxxx
HUGGINGFACE_TOKEN=123xxxxxxxxxxx
```

6. **Verify Knowledge Base**
Ensure `knowledge_base.json` is present in the root directory. If not, create it with sample data:
```json
[
    {
        "content": "Your first knowledge entry here..."
    },
    {
        "content": "Your second knowledge entry here..."
    }
]
```

7. **Run the Development Server**
```bash
python manage.py runserver 8002
```

8. **Test the Installation**
Open your browser or use curl to test the endpoint:
```bash
curl "http://localhost:8002/rag/gpt2/?query=What is technology?"
```

The application should now be running at `http://localhost:8002/`