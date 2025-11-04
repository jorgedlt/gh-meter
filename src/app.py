"""
GitHub Profile Analyzer - DevMeter
A Rotten Tomato-style rating system for developer hireability
"""

from flask import Flask, request, jsonify, render_template_string
from github import Github
import os
import re
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class DevMeter:
    """DevMeter rating system - like Rotten Tomatoes for developers"""

    def __init__(self):
        self.weights = {
            'activity_level': 0.25,
            'code_quality': 0.20,
            'collaboration': 0.15,
            'consistency': 0.15,
            'expertise': 0.15,
            'impact': 0.10
        }

    def calculate_rating(self, profile_data: Dict) -> Dict:
        """Calculate DevMeter score and rating"""
        scores = {}

        # Activity Level (25%): Based on repos, commits, contributions
        activity_score = self._calculate_activity_score(profile_data)
        scores['activity_level'] = activity_score

        # Code Quality (20%): Languages used, project complexity
        quality_score = self._calculate_quality_score(profile_data)
        scores['code_quality'] = quality_score

        # Collaboration (15%): Forks, PRs, issues
        collab_score = self._calculate_collaboration_score(profile_data)
        scores['collaboration'] = collab_score

        # Consistency (15%): Regular activity, maintenance
        consistency_score = self._calculate_consistency_score(profile_data)
        scores['consistency'] = consistency_score

        # Expertise (15%): Language diversity, project types
        expertise_score = self._calculate_expertise_score(profile_data)
        scores['expertise'] = expertise_score

        # Impact (10%): Stars, forks, community influence
        impact_score = self._calculate_impact_score(profile_data)
        scores['impact'] = impact_score

        # Calculate weighted total
        total_score = sum(scores[category] * self.weights[category] for category in scores)

        # Convert to percentage and determine rating
        percentage = min(100, max(0, int(total_score * 100)))

        rating = self._get_rating_category(percentage)

        return {
            'score': percentage,
            'rating': rating,
            'category_scores': scores,
            'recommendation': self._get_recommendation(percentage)
        }

    def _calculate_activity_score(self, data: Dict) -> float:
        """Calculate activity level score"""
        repos = data.get('repositories', [])
        recent_activity = data.get('recent_activity', 0)

        # Base score from repository count
        repo_score = min(1.0, len(repos) / 20.0)  # Max at 20 repos

        # Recent activity bonus
        activity_bonus = min(0.5, recent_activity / 10.0)  # Max bonus at 10 recent activities

        return min(1.0, repo_score + activity_bonus)

    def _calculate_quality_score(self, data: Dict) -> float:
        """Calculate code quality score"""
        languages = data.get('languages', [])
        repos = data.get('repositories', [])

        # Language diversity bonus
        lang_diversity = min(1.0, len(languages) / 5.0)  # Max at 5 languages

        # Popular languages bonus
        popular_langs = {'Python', 'JavaScript', 'TypeScript', 'Go', 'Rust', 'Java', 'C++', 'C#'}
        popular_count = sum(1 for lang, _ in languages if lang in popular_langs)
        popular_bonus = min(0.5, popular_count / 3.0)  # Max bonus at 3 popular languages

        return min(1.0, (lang_diversity * 0.7) + (popular_bonus * 0.3))

    def _calculate_collaboration_score(self, data: Dict) -> float:
        """Calculate collaboration score"""
        repos = data.get('repositories', [])
        profile = data.get('profile', {})

        # Fork ratio (lower is better - indicates original work)
        total_repos = len(repos)
        if total_repos == 0:
            return 0.0

        fork_count = sum(1 for repo in repos if repo.get('is_fork', False))
        fork_ratio = fork_count / total_repos

        # Prefer original work (inverse of fork ratio)
        originality_score = 1.0 - fork_ratio

        # Followers/following ratio
        followers = profile.get('followers', 0)
        following = profile.get('following', 1)  # Avoid division by zero
        social_score = min(1.0, followers / following) if following > 0 else 0.0

        return min(1.0, (originality_score * 0.7) + (social_score * 0.3))

    def _calculate_consistency_score(self, data: Dict) -> float:
        """Calculate consistency score"""
        repos = data.get('repositories', [])

        if not repos:
            return 0.0

        # Check for regular updates
        recent_repos = []
        for repo in repos:
            if repo.get('updated_at'):
                try:
                    updated = datetime.fromisoformat(repo['updated_at'].replace('Z', '+00:00'))
                    if updated > datetime.now() - timedelta(days=365):
                        recent_repos.append(repo)
                except:
                    continue

        consistency_ratio = len(recent_repos) / len(repos)
        return min(1.0, consistency_ratio * 1.5)  # Boost for consistency

    def _calculate_expertise_score(self, data: Dict) -> float:
        """Calculate expertise score"""
        focus_areas = data.get('focus_areas', [])
        languages = data.get('languages', [])

        # Diversity of focus areas
        area_score = min(1.0, len(focus_areas) / 3.0)  # Max at 3 areas

        # Technical depth (more languages = more expertise)
        depth_score = min(1.0, len(languages) / 4.0)  # Max at 4 languages

        return min(1.0, (area_score * 0.6) + (depth_score * 0.4))

    def _calculate_impact_score(self, data: Dict) -> float:
        """Calculate impact score"""
        total_stars = data.get('total_stars_received', 0)
        repos = data.get('repositories', [])

        # Stars per repository
        if repos:
            avg_stars = total_stars / len(repos)
            star_score = min(1.0, avg_stars / 10.0)  # Max at 10 stars per repo
        else:
            star_score = 0.0

        return star_score

    def _get_rating_category(self, percentage: int) -> str:
        """Get rating category based on percentage"""
        if percentage >= 90:
            return "🍅 Certified Fresh"
        elif percentage >= 80:
            return "🍅 Fresh"
        elif percentage >= 70:
            return "🍅 Mostly Fresh"
        elif percentage >= 60:
            return "🍅 Mixed"
        elif percentage >= 50:
            return "🍅 Rotten"
        else:
            return "🍅 Mostly Rotten"

    def _get_recommendation(self, percentage: int) -> str:
        """Get hiring recommendation"""
        if percentage >= 80:
            return "Highly recommended - this developer shows strong potential"
        elif percentage >= 70:
            return "Recommended with minor concerns"
        elif percentage >= 60:
            return "Consider with caution - may need mentoring"
        elif percentage >= 50:
            return "Not recommended - significant concerns"
        else:
            return "Strong pass - major red flags present"


def extract_username_from_url(url: str) -> Optional[str]:
    """Extract username from GitHub URL"""
    match = re.search(r'github\.com/([^/?]+)', url)
    return match.group(1) if match else None


def analyze_github_profile(username: str, token: Optional[str] = None) -> Dict:
    """Analyze GitHub profile programmatically"""

    # Initialize GitHub client
    g = Github(token) if token else Github()

    try:
        # Get user object
        user = g.get_user(username)

        # Basic profile info
        profile = {
            'username': user.login,
            'name': user.name,
            'bio': user.bio,
            'location': user.location,
            'company': user.company,
            'website': user.blog,
            'followers': user.followers,
            'following': user.following,
            'public_repos': user.public_repos,
            'public_gists': user.public_gists
        }

        # Get repositories (limit for performance)
        repos = []
        languages = {}
        total_stars = 0
        recent_activity = 0

        for repo in user.get_repos()[:30]:  # Limit to 30 repos
            repo_info = {
                'name': repo.name,
                'description': repo.description,
                'language': repo.language,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'created_at': repo.created_at.isoformat() if repo.created_at else None,
                'updated_at': repo.updated_at.isoformat() if repo.updated_at else None,
                'is_fork': repo.fork
            }
            repos.append(repo_info)

            # Count languages
            if repo.language:
                languages[repo.language] = languages.get(repo.language, 0) + 1

            # Count recent activity
            if repo.updated_at and repo.updated_at > datetime.now() - timedelta(days=90):
                recent_activity += 1

            total_stars += repo.stargazers_count

        # Sort languages by usage
        languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)

        # Determine focus areas
        focus_areas = determine_focus_areas(repos)

        profile_data = {
            'profile': profile,
            'repositories': repos[:6],  # Show top 6 like GitHub
            'languages': languages,
            'total_stars_received': total_stars,
            'focus_areas': focus_areas,
            'recent_activity': recent_activity
        }

        # Calculate DevMeter rating
        devmeter = DevMeter()
        rating = devmeter.calculate_rating(profile_data)
        profile_data['devmeter'] = rating

        return profile_data

    except Exception as e:
        logger.error(f"Error analyzing profile {username}: {str(e)}")
        return {'error': str(e)}


def determine_focus_areas(repos: List[Dict]) -> List[str]:
    """Determine focus areas based on repository content"""
    focus_areas = []
    descriptions = [r.get('description', '') for r in repos if r.get('description')]
    names = [r.get('name', '') for r in repos]

    all_text = ' '.join(descriptions + names).lower()

    focus_keywords = {
        'web': ['web', 'frontend', 'backend', 'api', 'rest', 'http', 'flask', 'django', 'react', 'vue', 'angular'],
        'data': ['data', 'analytics', 'machine learning', 'ml', 'ai', 'statistics', 'pandas', 'numpy', 'tensorflow', 'pytorch'],
        'devops': ['docker', 'kubernetes', 'ci/cd', 'deployment', 'cloud', 'aws', 'gcp', 'azure', 'terraform', 'ansible'],
        'security': ['security', 'auth', 'encryption', 'privacy', 'penetration', 'hacking', 'cybersecurity'],
        'mobile': ['android', 'ios', 'mobile', 'react native', 'flutter', 'swift', 'kotlin'],
        'gaming': ['game', 'gaming', 'unity', 'unreal', 'godot', 'phaser'],
        'finance': ['trading', 'finance', 'stock', 'crypto', 'blockchain', 'bitcoin', 'ethereum'],
        'iot': ['iot', 'internet of things', 'arduino', 'raspberry pi', 'embedded'],
        'automation': ['automation', 'scripting', 'bash', 'powershell', 'selenium']
    }

    for area, keywords in focus_keywords.items():
        if any(keyword in all_text for keyword in keywords):
            focus_areas.append(area)

    return focus_areas[:5]  # Limit to top 5 areas


@app.route('/', methods=['GET'])
def index():
    """Serve the main web interface"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DevMeter - GitHub Developer Rating</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: white;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 10px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5em;
            }
            .subtitle {
                text-align: center;
                margin-bottom: 30px;
                opacity: 0.9;
                font-size: 1.2em;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
            }
            input[type="text"] {
                width: 100%;
                padding: 12px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                background: rgba(255, 255, 255, 0.9);
                color: #333;
            }
            button {
                background: #ff6b6b;
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                width: 100%;
                transition: background 0.3s;
            }
            button:hover {
                background: #ff5252;
            }
            .example {
                text-align: center;
                margin-top: 20px;
                opacity: 0.8;
                font-size: 0.9em;
            }
            .rating-display {
                text-align: center;
                margin-top: 30px;
                padding: 20px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
            }
            .score {
                font-size: 3em;
                font-weight: bold;
                margin: 10px 0;
            }
            .rating {
                font-size: 1.5em;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🍅 DevMeter</h1>
            <p class="subtitle">Rate developers like Rotten Tomatoes rates movies</p>

            <form id="analyzeForm">
                <div class="form-group">
                    <label for="githubUrl">GitHub Profile URL</label>
                    <input type="text" id="githubUrl" name="url"
                           placeholder="https://github.com/username"
                           required>
                </div>
                <button type="submit">Analyze Profile</button>
            </form>

            <div class="example">
                Example: https://github.com/octocat
            </div>

            <div id="results" style="display: none;">
                <div class="rating-display">
                    <div id="score" class="score"></div>
                    <div id="rating" class="rating"></div>
                    <div id="recommendation"></div>
                </div>
            </div>
        </div>

        <script>
            document.getElementById('analyzeForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData(e.target);
                const url = formData.get('url');

                try {
                    const response = await fetch('/analyze', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ url: url })
                    });

                    const data = await response.json();

                    if (data.error) {
                        alert('Error: ' + data.error);
                        return;
                    }

                    // Display results
                    document.getElementById('score').textContent = data.devmeter.score + '%';
                    document.getElementById('rating').textContent = data.devmeter.rating;
                    document.getElementById('recommendation').textContent = data.devmeter.recommendation;
                    document.getElementById('results').style.display = 'block';

                } catch (error) {
                    alert('Error analyzing profile: ' + error.message);
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route('/analyze', methods=['POST'])
def analyze():
    """API endpoint for GitHub profile analysis"""
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        username = extract_username_from_url(url)
        if not username:
            return jsonify({'error': 'Invalid GitHub URL'}), 400

        # Get GitHub token from environment (optional)
        token = os.getenv('GITHUB_TOKEN')

        result = analyze_github_profile(username, token)
        return jsonify(result)

    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')