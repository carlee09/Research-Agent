#!/usr/bin/env python3
"""Test Research Agent with mock data."""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from analyzers import GeminiAnalyzer
from generators import MarkdownGenerator
from config import Config

# Mock data for testing
MOCK_X_DATA = [
    {
        "source": "x",
        "content": "Uniswap v4 is now live on mainnet! 🦄 The new hooks system allows for unprecedented customization of liquidity pools. This is a game-changer for DeFi.",
        "author": "Uniswap",
        "author_name": "Uniswap Protocol",
        "date": "2024-02-10",
        "url": "https://twitter.com/Uniswap/status/1234567890",
        "engagement": {
            "likes": 5420,
            "retweets": 1230,
            "replies": 456
        },
        "metadata": {
            "id": "1234567890",
            "language": "en",
            "verified": True
        }
    },
    {
        "source": "x",
        "content": "Just deployed my first liquidity pool on @Uniswap v4 with a custom hook. The developer experience is incredible. Building the future of AMMs! 🚀",
        "author": "DeFiBuilder",
        "author_name": "DeFi Builder",
        "date": "2024-02-09",
        "url": "https://twitter.com/DeFiBuilder/status/1234567891",
        "engagement": {
            "likes": 892,
            "retweets": 156,
            "replies": 67
        },
        "metadata": {
            "id": "1234567891",
            "language": "en",
            "verified": False
        }
    },
    {
        "source": "x",
        "content": "Uniswap continues to dominate DEX volume with over $1.5B in daily trades. The v4 launch could push this even higher. #DeFi #Ethereum",
        "author": "CryptoAnalyst",
        "author_name": "Crypto Market Analyst",
        "date": "2024-02-08",
        "url": "https://twitter.com/CryptoAnalyst/status/1234567892",
        "engagement": {
            "likes": 1340,
            "retweets": 287,
            "replies": 94
        },
        "metadata": {
            "id": "1234567892",
            "language": "en",
            "verified": True
        }
    }
]

MOCK_WEB_DATA = [
    {
        "source": "web",
        "title": "Uniswap v4 Launch: What You Need to Know",
        "content": "Uniswap Labs has officially launched version 4 of its decentralized exchange protocol, introducing a revolutionary hooks system that allows developers to customize liquidity pool behavior. The new architecture reduces gas costs by up to 99% for certain operations.",
        "url": "https://techcrunch.com/uniswap-v4-launch",
        "author": "TechCrunch",
        "date": "2024-02-10",
        "metadata": {
            "domain": "techcrunch.com",
            "position": 1,
            "thumbnail": ""
        }
    },
    {
        "source": "web",
        "title": "Uniswap Dominates DEX Market with 65% Volume Share",
        "content": "According to DeFi Llama data, Uniswap maintains its position as the largest decentralized exchange by trading volume, processing over $1.5 billion in daily transactions. The platform's market dominance has grown since the v3 launch.",
        "url": "https://coindesk.com/uniswap-market-dominance",
        "author": "CoinDesk",
        "date": "2024-02-09",
        "metadata": {
            "domain": "coindesk.com",
            "position": 2,
            "thumbnail": ""
        }
    },
    {
        "source": "web",
        "title": "Understanding Uniswap v4 Hooks: A Developer Guide",
        "content": "Hooks in Uniswap v4 are smart contracts that can execute custom logic at specific points in a pool's lifecycle. This enables use cases like dynamic fees, custom oracles, and advanced trading strategies that were previously impossible.",
        "url": "https://ethereum.org/uniswap-v4-hooks",
        "author": "Ethereum.org",
        "date": "2024-02-08",
        "metadata": {
            "domain": "ethereum.org",
            "position": 3,
            "thumbnail": ""
        }
    }
]


def test_with_mock_data():
    """Test the full pipeline with mock data."""
    print("🧪 Testing Research Agent with Mock Data\n")
    print("=" * 60)

    topic = "uniswap"

    # Combine mock data
    all_data = MOCK_X_DATA + MOCK_WEB_DATA

    print(f"\n📊 Mock Data Summary:")
    print(f"  - X posts: {len(MOCK_X_DATA)}")
    print(f"  - Web results: {len(MOCK_WEB_DATA)}")
    print(f"  - Total items: {len(all_data)}")

    # Test Gemini Analyzer
    print(f"\n🤖 Testing Gemini AI Analyzer...")
    try:
        analyzer = GeminiAnalyzer()
        analysis_result = analyzer.analyze(topic, all_data, depth="quick")

        if analysis_result.get("success"):
            print("✅ Analysis successful!")
            metadata = analysis_result.get("metadata", {})
            print(f"  - Model: {metadata.get('model')}")
            print(f"  - Tokens used: {metadata.get('tokens_used')}")
            print(f"  - Items analyzed: {metadata.get('items_analyzed')}")

            # Show first 500 chars of analysis
            analysis_text = analysis_result.get("analysis", "")
            print(f"\n📝 Analysis Preview:")
            print("-" * 60)
            print(analysis_text[:500] + "..." if len(analysis_text) > 500 else analysis_text)
            print("-" * 60)
        else:
            print(f"❌ Analysis failed: {analysis_result.get('error')}")
            return False

    except Exception as e:
        print(f"❌ Analyzer error: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Test Markdown Generator
    print(f"\n📝 Testing Markdown Report Generator...")
    try:
        generator = MarkdownGenerator()

        # Organize sources
        sources = analyzer.summarize_sources(all_data)

        # Generate report
        output_filename = f"test_report_uniswap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        output_path = Config.OUTPUT_DIR / output_filename

        success = generator.generate_report(
            topic=topic,
            analysis_result=analysis_result,
            sources=sources,
            output_path=output_path
        )

        if success:
            print(f"✅ Report generated successfully!")
            print(f"  - Output: {output_path}")
            print(f"  - Size: {output_path.stat().st_size} bytes")

            # Show file info
            print(f"\n📄 Report Contents:")
            content = output_path.read_text(encoding="utf-8")
            lines = content.split("\n")
            print(f"  - Total lines: {len(lines)}")
            print(f"  - Total characters: {len(content)}")

            return True
        else:
            print("❌ Report generation failed")
            return False

    except Exception as e:
        print(f"❌ Generator error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🔬 Research Agent - Mock Data Test\n")

    # Ensure output directory exists
    Config.ensure_output_dir()

    # Run test
    success = test_with_mock_data()

    print("\n" + "=" * 60)
    if success:
        print("\n✅ All tests passed! System is working correctly.")
        print("\n📂 Check the reports/ directory for the generated report.")
        sys.exit(0)
    else:
        print("\n❌ Tests failed. Please check the errors above.")
        sys.exit(1)
