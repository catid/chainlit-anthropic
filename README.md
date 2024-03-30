# Chainlit Anthropic

This is a Chainlit app that uses the Anthropic API to generate text.

## Setup

```bash
git clone https://github.com/catid/chainlit-anthropic.git
cd chainlit-anthropic

conda create -n chat python=3.10 -y && conda activate chat
pip install -r requirements.txt
```

Create a `.env` file with your Anthropic API key:

```bash
echo "ANTHROPIC_API_KEY=your_api_key" > .env
```

Run the app:

```bash
chainlit run
```
