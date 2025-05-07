# Presentation Assistant

An AI-powered presentation assistant that provides real-time narration and Q&A capabilities for Google Slides presentations.

## Features

- Real-time slide detection and narration
- Text-to-speech narration of speaker notes
- Interactive Q&A using speech recognition
- Integration with Google Slides API
- OpenAI GPT-4 powered responses

## Prerequisites

- Python 3.8+
- Google Cloud Platform account with Slides API enabled
- OpenAI API key
- Google service account credentials

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd presentation_assistant3
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key
SLIDES_URL=your_google_slides_url
```

5. Place your Google service account credentials in `google_credentials.json`

## Usage

1. Start the presentation assistant:
```bash
python main.py
```

2. Open your Google Slides presentation in a browser
3. The assistant will automatically detect slide changes and provide narration
4. For slides 5 and above, the assistant will prompt for questions
5. Speak your question or say "no" to skip

## Project Structure

- `main.py`: Main application entry point
- `slides_service.py`: Google Slides integration
- `tts_service.py`: Text-to-speech functionality
- `stt_service.py`: Speech-to-text functionality
- `qa_service.py`: Question answering service
- `slide_detector.py`: Slide change detection
- `config_loader.py`: Configuration management

## Recovery Guide

See [RECOVERY.md](RECOVERY.md) for detailed recovery procedures and troubleshooting steps.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 