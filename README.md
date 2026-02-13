# Research Agent 🔬

AI-powered research automation and analysis tool that helps researchers focus on insights instead of data collection.

## Overview

**Research Agent** automatically collects data from X (Twitter) and web search, analyzes it with AI (Claude or Gemini), and generates comprehensive Markdown research reports.

### Key Features

- 🤖 **Multiple AI Models**: Choose between Claude Sonnet 4 or Google Gemini
- 🔍 **Multi-Source Collection**: Automated data gathering from X and web
- 📝 **Beautiful Reports**: Structured Markdown reports ready to use
- ⚡ **Fast & Efficient**: Research in minutes, not hours
- 🎯 **Flexible Options**: Customizable sources, depth, model, and output

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/research-agent.git
cd research-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```bash
# At least one AI model API key is required
GEMINI_API_KEY=your-gemini-key-here          # Recommended
ANTHROPIC_API_KEY=sk-ant-your-key-here       # Optional

# Sela Network API (for X and web search)
SELA_API_KEY=your-sela-key-here
SELA_API_ENDPOINT=https://api.selanetwork.io/api/rpc/scrapeUrl

# Default AI model (claude or gemini)
DEFAULT_MODEL=gemini
```

### Usage

Basic usage:
```bash
research-agent --topic "AI agents 2024"
```

With model selection:
```bash
# Use Gemini (default)
research-agent --topic "AI agents 2024" --model gemini

# Use Claude
research-agent --topic "AI agents 2024" --model claude
```

Advanced usage:
```bash
research-agent \
  --topic "Anthropic Claude updates" \
  --sources x,web \
  --max-items 30 \
  --model gemini \
  --output claude-research.md \
  --depth detailed
```

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--topic` | Research topic (required) | - |
| `--sources` | Data sources: `x`, `web`, or `all` | `all` |
| `--max-items` | Maximum items per source | `20` |
| `--model` | AI model: `claude` or `gemini` | `gemini` |
| `--output` | Output filename | Auto-generated |
| `--depth` | Analysis depth: `quick` or `detailed` | `detailed` |

## Examples

### Example 1: Market Research with Gemini
```bash
research-agent --topic "AI coding assistants market 2024" \
  --sources all \
  --max-items 30 \
  --model gemini
```

**Result**: Comprehensive market analysis with trends, competitors, and user sentiment.

### Example 2: Academic Research with Claude
```bash
research-agent --topic "Large Language Models safety" \
  --sources web \
  --max-items 50 \
  --model claude \
  --depth detailed
```

**Result**: Detailed academic analysis with latest papers and research findings.

### Example 3: Social Media Trend Analysis
```bash
research-agent --topic "sustainable fashion trends" \
  --sources x \
  --max-items 40 \
  --model gemini
```

**Result**: Social media trends and influencer opinions on sustainable fashion.

## AI Models

### Google Gemini (Recommended)
- **Model**: `gemini-2.5-flash`
- **Pros**: Fast, cost-effective, high quality
- **Best for**: General research, quick analysis, high-volume usage
- **Get API Key**: [Google AI Studio](https://makersuite.google.com/app/apikey)

### Anthropic Claude
- **Model**: `claude-sonnet-4-20250514`
- **Pros**: Exceptional reasoning, detailed analysis
- **Best for**: Complex research, academic work, in-depth analysis
- **Get API Key**: [Anthropic Console](https://console.anthropic.com/)

You can switch between models anytime using the `--model` option!

## Report Structure

Generated reports include:

- **Executive Summary**: Key findings in 3-5 sentences
- **Key Insights**: Major discoveries with evidence
- **Detailed Analysis**: Thematic breakdown of findings
- **Opinion Analysis**: Mainstream vs. contrasting views
- **Data Sources**: All X posts and web articles referenced
- **Conclusion**: Recommendations and next steps

See [examples/sample_report.md](examples/sample_report.md) for a complete example.

## Project Structure

```
research-agent/
├── src/
│   ├── main.py              # CLI entry point
│   ├── config.py            # Configuration management
│   ├── collectors/          # Data collection
│   │   ├── x_collector.py   # X API integration
│   │   └── web_collector.py # Web search integration
│   ├── analyzers/           # AI analysis
│   │   ├── claude_analyzer.py   # Claude integration
│   │   ├── gemini_analyzer.py   # Gemini integration
│   │   └── prompt_templates.py
│   ├── generators/          # Report generation
│   │   └── markdown_generator.py
│   └── utils/              # Utilities
│       ├── logger.py
│       └── validators.py
├── examples/               # Sample files
├── tests/                 # Test suite
└── reports/              # Generated reports
```

## Requirements

- Python 3.9+ (Python 3.10+ recommended)
- At least one AI API key:
  - Google Gemini API key (recommended), OR
  - Anthropic Claude API key
- Sela Network API key (for X and web search)

## API Setup

### Google Gemini API (Recommended)

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add to `.env` as `GEMINI_API_KEY`
4. **Free tier available** with generous limits

### Anthropic Claude API (Optional)

1. Sign up at [console.anthropic.com](https://console.anthropic.com/)
2. Create an API key
3. Add to `.env` as `ANTHROPIC_API_KEY`
4. Pay-as-you-go pricing

### Sela Network API

1. Contact Sela Network for API access
2. Obtain API key and endpoint URL
3. Add to `.env`:
   - `SELA_API_KEY`
   - `SELA_API_ENDPOINT`

**Supported Scrape Types:**
- `GOOGLE_SEARCH`: Google search results
- `TWITTER_PROFILE`: Twitter user profile posts
- `TWITTER_POST`: Individual tweet scraping

See [SELA_API.md](SELA_API.md) for detailed API documentation and request/response formats.

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint
flake8 src/ tests/

# Type check
mypy src/
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Roadmap

### ✅ Completed (v0.1.0)
- [x] CLI interface with Click
- [x] X and Web data collection
- [x] Claude AI integration
- [x] Gemini AI integration
- [x] Markdown report generation
- [x] Multi-model support

### Phase 2 (3 months)
- [ ] Scheduled research automation
- [ ] Change tracking and comparison
- [ ] PDF and HTML export
- [ ] Additional AI models (GPT-4, etc.)

### Phase 3 (6 months)
- [ ] Interactive mode with follow-up questions
- [ ] Chart and graph generation
- [ ] Team collaboration features
- [ ] Web dashboard

## Troubleshooting

### "No AI API key found"
Make sure you have at least one of these in your `.env`:
- `GEMINI_API_KEY` (recommended)
- `ANTHROPIC_API_KEY`

### "SELA_API_KEY is required"
Add your Sela Network API credentials to `.env`:
```bash
SELA_API_KEY=your-key-here
SELA_API_ENDPOINT=https://api.selanetwork.io/api/rpc/scrapeUrl
```

### Python version warnings
Google recommends Python 3.10+. To upgrade:
```bash
# Install Python 3.11 or 3.12
# Recreate virtual environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Support

- 📖 [Documentation](https://github.com/yourusername/research-agent/wiki)
- 🐛 [Report Issues](https://github.com/yourusername/research-agent/issues)
- 💬 [Discussions](https://github.com/yourusername/research-agent/discussions)

## Acknowledgments

- Powered by [Anthropic Claude](https://anthropic.com/) & [Google Gemini](https://ai.google.dev/)
- Data collection via [Sela Network](https://selanetwork.io)
- Built with [Click](https://click.palletsprojects.com/) and [Rich](https://rich.readthedocs.io/)

---

**Research Agent** - Automate your research, amplify your insights. 🚀
