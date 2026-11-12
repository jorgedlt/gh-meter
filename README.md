# 🍅 DevMeter - GitHub Developer Rating System

<!-- Trigger integration tests -->

[![Deploy to Google Cloud](https://github.com/jorgedlt/gh-meter/actions/workflows/deploy.yml/badge.svg)](https://github.com/jorgedlt/gh-meter/actions/workflows/deploy.yml)
[![codecov](https://codecov.io/gh/jorgedlt/gh-meter/branch/main/graph/badge.svg)](https://codecov.io/gh/jorgedlt/gh-meter)

Rate developers like Rotten Tomatoes rates movies! DevMeter analyzes GitHub profiles and provides a comprehensive hireability score based on activity, code quality, collaboration, consistency, expertise, and impact.

## 🍅 DevMeter Rating System

### Rating Categories
- **🍅 Certified Fresh** (90-100%): Exceptional developer - highly recommended
- **🍅 Fresh** (80-89%): Strong candidate with proven track record
- **🍅 Mostly Fresh** (70-79%): Good developer with minor concerns
- **🍅 Mixed** (60-69%): Average with some red flags
- **🍅 Rotten** (50-59%): Not recommended - significant concerns
- **🍅 Mostly Rotten** (0-49%): Strong pass - major issues present

### Scoring Dimensions (25% each except Impact)
| Dimension | Weight | Description |
|-----------|--------|-------------|
| Activity Level | 25% | Repository count, recent commits, overall engagement |
| Code Quality | 20% | Language diversity, use of popular technologies |
| Collaboration | 15% | Original work vs forks, social network |
| Consistency | 15% | Regular maintenance, sustained activity |
| Expertise | 15% | Technical breadth, focus area diversity |
| Impact | 10% | Community influence, stars, forks |

## 🌟 Features

- **Comprehensive Analysis**: Evaluates GitHub profiles across 6 key dimensions
- **Rotten Tomatoes Style Rating**: Fun, intuitive scoring system (0-100%)
- **Real-time API**: RESTful API for programmatic access
- **Web Interface**: Beautiful, responsive web UI
- **Docker Ready**: Containerized for easy deployment
- **Google Cloud Run**: Production-ready deployment pipeline
- **Real Integration Testing**: Tests with actual HTTP calls and live GitHub data
- **Automated CI/CD**: Full pipeline with unit tests, integration tests, and deployment
- **Live Demonstrations**: Proven functionality with real DevMeter output

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

### Unit Tests
Run the unit test suite:

```bash
# Run all unit tests
pytest tests/test_app.py -v

# Run with coverage
pytest tests/test_app.py --cov=src --cov-report=html

# Run specific test
pytest tests/test_app.py::TestDevMeter::test_calculate_rating_perfect_profile -v
```

### Integration Tests
Run end-to-end integration tests with real HTTP calls:

```bash
# Run integration tests (spins up real Docker containers)
pytest tests/test_integration.py -v -s

# Run with the automated script
./run_integration_tests.sh

# Run specific integration test
pytest tests/test_integration.py::TestDevMeterIntegration::test_github_profile_analysis_octocat -v -s
```

### What Integration Tests Prove
The integration tests provide **real DevMeter output** from actual HTTP calls:

```
🎯 REAL DEVMETER ANALYSIS RESULTS:
   Profile: The Octocat (@octocat)
   Score: 69%
   Rating: 🍅 Mixed
   Recommendation: Consider with caution - may need mentoring
   Top Languages: Ruby, CSS, HTML
```

Unlike simulations, these tests:
- ✅ Spin up actual Docker containers
- ✅ Make real HTTP POST requests to `/analyze`
- ✅ Fetch live data from GitHub API
- ✅ Show genuine scoring calculations
- ✅ Validate complete end-to-end functionality

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
  "languages": [["Ruby", 12], ["CSS", 8], ["HTML", 6]],
  "focus_areas": [],
  "devmeter": {
    "score": 69,
    "rating": "🍅 Mixed",
    "recommendation": "Consider with caution - may need mentoring",
    "category_scores": {
      "activity_level": 0.70,
      "code_quality": 0.65,
      "collaboration": 0.75,
      "consistency": 0.60,
      "expertise": 0.80,
      "impact": 0.50
    }
  }
}
```

**Real Example Output** (from integration tests):
```
🎯 REAL DEVMETER ANALYSIS RESULTS:
   Profile: The Octocat (@octocat)
   Score: 69%
   Rating: 🍅 Mixed
   Recommendation: Consider with caution - may need mentoring
   Top Languages: Ruby, CSS, HTML
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

## 🚀 Deployment & Usage

### Live Demo
The DevMeter application is deployed and running. Try it with real GitHub profiles:

**Web Interface:** Access the live application at the deployed URL (available after Google Cloud Run deployment)

**API Testing:**
```bash
# Test with curl
curl -X POST https://your-deployed-url/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/octocat"}'

# Expected real output:
# {
#   "devmeter": {
#     "score": 69,
#     "rating": "🍅 Mixed",
#     "recommendation": "Consider with caution - may need mentoring"
#   }
# }
```

### Google Cloud Run Deployment
The project includes automated CI/CD:

1. **Push to main branch** → Triggers GitHub Actions
2. **Unit tests run** → Validate code quality
3. **Integration tests run** → Test with real HTTP calls and Docker
4. **Deploy to Cloud Run** → Live application available
5. **Health checks** → Verify deployment success

### Local Development
```bash
# Start with Docker Compose
docker-compose up --build

# Or run locally
pip install -r requirements-dev.txt
cd src && python app.py
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
│   └── app.py              # Main Flask application with DevMeter logic
├── tests/
│   ├── test_app.py         # Unit tests for DevMeter rating system
│   └── test_integration.py # Integration tests with real HTTP calls
├── Dockerfile              # Production container
├── docker-compose.yml      # Local development setup
├── requirements.txt        # Python dependencies
├── requirements-dev.txt    # Development dependencies
├── run_integration_tests.sh # Automated integration test runner
├── Makefile               # Development helpers
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

## Completeness grade: A

Code, tests, CI/CD workflows and the Cloud Run deployment pipeline are
all in this repo; a fresh clone rebuilds and redeploys the service.
The remaining fraction is live credentials and cloud state, named below.

## Not in code

- GitHub API tokens and GCP service credentials: GitHub Actions secrets
  and the Google Cloud console for the gh-meter project, never in this
  repo.
- Live Cloud Run service state and any console-side configuration:
  Google Cloud console is the record of truth.
