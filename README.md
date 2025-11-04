# 🍅 DevMeter - GitHub Developer Rating System

<!-- Trigger integration tests -->

[![Deploy to Google Cloud](https://github.com/jorgedlt/gh-meter/actions/workflows/deploy.yml/badge.svg)](https://github.com/jorgedlt/gh-meter/actions/workflows/deploy.yml)
[![codecov](https://codecov.io/gh/jorgedlt/gh-meter/branch/main/graph/badge.svg)](https://codecov.io/gh/jorgedlt/gh-meter)

Rate developers like Rotten Tomatoes rates movies! DevMeter analyzes GitHub profiles and provides a comprehensive hireability score based on activity, code quality, collaboration, consistency, expertise, and impact.

## 🌟 Features

- **Comprehensive Analysis**: Evaluates GitHub profiles across 6 key dimensions
- **Rotten Tomatoes Style Rating**: Fun, intuitive scoring system (0-100%)
- **Real-time API**: RESTful API for programmatic access
- **Web Interface**: Beautiful, responsive web UI
- **Docker Ready**: Containerized for easy deployment
- **Google Cloud Run**: Production-ready deployment pipeline

## 🎯 Rating Categories

- **🍅 Certified Fresh** (90-100%): Exceptional developer - highly recommended
- **🍅 Fresh** (80-89%): Strong candidate with proven track record
- **🍅 Mostly Fresh** (70-79%): Good developer with minor concerns
- **🍅 Mixed** (60-69%): Average with some red flags
- **🍅 Rotten** (50-59%): Not recommended - significant concerns
- **🍅 Mostly Rotten** (0-49%): Strong pass - major issues present

## 📊 Scoring Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Activity Level | 25% | Repository count, recent commits, overall engagement |
| Code Quality | 20% | Language diversity, use of popular technologies |
| Collaboration | 15% | Original work vs forks, social network |
| Consistency | 15% | Regular maintenance, sustained activity |
| Expertise | 15% | Technical breadth, focus area diversity |
| Impact | 10% | Community influence, stars, forks |

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/jorgedlt/gh-meter.git
   cd gh-meter
   ```

2. **Set up environment**
   ```bash
   # Optional: Set GitHub token for higher rate limits
   echo "GITHUB_TOKEN=your_github_token" > .env
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Open your browser**
   ```
   http://localhost:8080
   ```

### Manual Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Run the application**
   ```bash
   cd src
   python app.py
   ```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_app.py::TestDevMeter::test_calculate_rating_perfect_profile -v
```

## 📡 API Usage

### Analyze Profile

**Endpoint:** `POST /analyze`

**Request:**
```json
{
  "url": "https://github.com/octocat"
}
```

**Response:**
```json
{
  "profile": {
    "username": "octocat",
    "name": "The Octocat",
    "bio": "GitHub mascot",
    "location": "San Francisco",
    "company": "GitHub",
    "followers": 5000,
    "following": 100
  },
  "repositories": [...],
  "languages": [["JavaScript", 15], ["Python", 8]],
  "focus_areas": ["web", "devops"],
  "devmeter": {
    "score": 92,
    "rating": "🍅 Certified Fresh",
    "recommendation": "Highly recommended - this developer shows strong potential",
    "category_scores": {
      "activity_level": 0.95,
      "code_quality": 0.88,
      "collaboration": 0.90,
      "consistency": 0.85,
      "expertise": 0.92,
      "impact": 0.80
    }
  }
}
```

### Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

## 🐳 Docker Deployment

### Build and run locally

```bash
# Build image
docker build -t devmeter .

# Run container
docker run -p 8080:8080 -e GITHUB_TOKEN=your_token devmeter
```

### Google Cloud Run Deployment

The project includes automated CI/CD that deploys to Google Cloud Run on every push to main.

**Required Secrets:**
- `GCP_PROJECT_ID`: Your Google Cloud Project ID
- `GCP_SA_KEY`: Service Account JSON key with Cloud Run Admin permissions

**Deployment Steps:**
1. Fork this repository
2. Set up Google Cloud Project
3. Create a Service Account with necessary permissions
4. Add secrets to GitHub repository
5. Push to main branch

The service will be automatically deployed and tested.

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GITHUB_TOKEN` | GitHub API token for higher rate limits | None |
| `PORT` | Server port | 8080 |
| `FLASK_DEBUG` | Enable Flask debug mode | False |

### GitHub Token Setup

For higher API rate limits (5,000 vs 60 requests/hour), set up a GitHub token:

1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Generate a new token with `public_repo` scope
3. Set as `GITHUB_TOKEN` environment variable

## 🏗️ Architecture

```
├── src/
│   └── app.py              # Main Flask application
├── tests/
│   └── test_app.py         # Comprehensive test suite
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Local development setup
├── requirements.txt        # Python dependencies
└── .github/workflows/      # CI/CD pipeline
    └── deploy.yml
```

## 🤝 Contributing

We welcome contributions that improve the tool's accuracy, add features, or enhance its educational value. However, all contributions must align with our ethical guidelines.

### Contribution Guidelines:
1. **Ethical focus**: Ensure changes don't enable harmful use cases
2. **Transparency**: Rating algorithms should be clear and well-documented
3. **Bias awareness**: Consider how changes might affect different types of developers
4. **Testing**: Maintain comprehensive test coverage

### Development Process:
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Write tests for your changes
4. Ensure all tests pass: `pytest tests/`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Reporting Issues:
- **Algorithm concerns**: If you believe the rating system is unfair, please open an issue with specific examples
- **Ethical issues**: Report any misuse or concerning applications of this tool

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by Rotten Tomatoes rating system
- Built with Flask, PyGitHub, and Docker
- Deployed on Google Cloud Run

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/jorgedlt/gh-meter/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jorgedlt/gh-meter/discussions)

---

**Made with ❤️ for the developer community**