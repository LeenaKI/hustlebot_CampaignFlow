# HustleBot

An AI-powered drip campaign generator that creates multi-step marketing campaigns using Google's Gemini AI.

## Overview

HustleBot automates the creation of personalized drip campaigns by taking your business context and campaign parameters, then generating a complete sequence of marketing messages tailored to your target audience.

## Features

- **AI-Powered Generation**: Uses Google Gemini 2.5 Flash for intelligent campaign creation
- **Flexible Configuration**: Define campaign length, tone, target audience, and goals
- **Context-Aware**: Incorporates business context and notes into campaign copy
- **Failover Support**: Multiple API key support with automatic failover
- **Privacy-Focused**: Automatically anonymizes employee names using functional titles
- **JSON Output**: Clean, structured output ready for integration

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hustlebot
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv hustlebot
source hustlebot/bin/activate  # On Windows: hustlebot\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root:
```env
GEMINI_API_KEYS=your_api_key_1,your_api_key_2,your_api_key_3
```

You can provide multiple API keys separated by commas. The system will automatically failover to the next key if one fails.

2. Configure your campaign in `input.json`:
```json
{
  "flow_category": "Lead Generation",
  "flow_length_(steps)": "50",
  "target_audience": "sales persons",
  "campaign_goal": "Option",
  "tone_of_voice": "professional",
  "primary_cta": "Option",
  "Additional_context_&_notes__(optional)": "Your business context here..."
}
```

### Input Parameters

- **flow_category**: Type of campaign (e.g., "Lead Generation", "Onboarding", "Re-engagement")
- **flow_length_(steps)**: Number of steps in the drip campaign
- **target_audience**: Who the campaign is targeting
- **campaign_goal**: Primary objective of the campaign
- **tone_of_voice**: Communication style (e.g., "professional", "casual", "friendly")
- **primary_cta**: Main call-to-action
- **Additional_context_&_notes__(optional)**: Business facts, company info, or other context to weave into the copy

## Usage

Run the campaign generator:

```bash
python main.py
```

The script will:
1. Load your configuration from `input.json`
2. Generate the campaign using Gemini AI
3. Save the output to `campaign_output.json`

### Test Configuration

To verify your setup before running a full campaign:

```bash
python example.py
```

This will check that your `.env` file is configured correctly and that `input.json` can be read.

## Output

The generated campaign is saved as `campaign_output.json` in the following format:

```json
[
  {
    "step": 1,
    "message": "Your campaign message here...",
    "cta": "Call to action text"
  },
  ...
]
```

## System Prompt Behavior

The AI is instructed to:
- Generate exactly the number of steps requested
- Never use employee names (uses functional titles instead)
- Always append "Our team will attend to you ASAP" after time slot selection
- Return raw JSON only (no markdown formatting)
- Extract and weave business facts from the additional context

## Requirements

- Python 3.7+
- google-genai
- python-dotenv

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
