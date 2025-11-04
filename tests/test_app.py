"""
Tests for DevMeter GitHub Profile Analyzer
"""

import pytest
import json
from unittest.mock import Mock, patch
from src.app import app, DevMeter, extract_username_from_url, analyze_github_profile


class TestDevMeter:
    """Test the DevMeter rating system"""

    def setup_method(self):
        self.devmeter = DevMeter()

    def test_calculate_rating_perfect_profile(self):
        """Test rating calculation for a high-quality profile"""
        profile_data = {
            'repositories': [{'is_fork': False, 'updated_at': '2024-01-01T00:00:00Z'}] * 25,
            'languages': [('Python', 10), ('JavaScript', 8), ('Go', 5), ('Rust', 3), ('TypeScript', 2)],
            'total_stars_received': 500,
            'recent_activity': 20,
            'focus_areas': ['web', 'data', 'devops'],
            'profile': {'followers': 100, 'following': 50}
        }

        result = self.devmeter.calculate_rating(profile_data)

        assert 'score' in result
        assert 'rating' in result
        assert 'category_scores' in result
        assert result['score'] >= 80  # Should be high score
        assert 'Fresh' in result['rating']

    def test_calculate_rating_poor_profile(self):
        """Test rating calculation for a low-quality profile"""
        profile_data = {
            'repositories': [{'is_fork': True, 'updated_at': '2020-01-01T00:00:00Z'}] * 2,
            'languages': [('Unknown', 1)],
            'total_stars_received': 0,
            'recent_activity': 0,
            'focus_areas': [],
            'profile': {'followers': 1, 'following': 100}
        }

        result = self.devmeter.calculate_rating(profile_data)

        assert result['score'] <= 30  # Should be low score
        assert 'Rotten' in result['rating']

    def test_activity_score_calculation(self):
        """Test activity score calculation"""
        # High activity
        data = {'repositories': [{}] * 25, 'recent_activity': 15}
        score = self.devmeter._calculate_activity_score(data)
        assert score >= 0.8

        # Low activity
        data = {'repositories': [{}], 'recent_activity': 0}
        score = self.devmeter._calculate_activity_score(data)
        assert score <= 0.2

    def test_quality_score_calculation(self):
        """Test code quality score calculation"""
        # Diverse popular languages
        data = {'languages': [('Python', 5), ('JavaScript', 4), ('Go', 3), ('Rust', 2), ('Java', 1)]}
        score = self.devmeter._calculate_quality_score(data)
        assert score >= 0.8

        # Limited languages
        data = {'languages': [('Unknown', 1)]}
        score = self.devmeter._calculate_quality_score(data)
        assert score <= 0.3


class TestURLExtraction:
    """Test GitHub URL parsing"""

    def test_valid_github_urls(self):
        """Test extraction from valid GitHub URLs"""
        test_cases = [
            ('https://github.com/octocat', 'octocat'),
            ('https://github.com/user-name', 'user-name'),
            ('https://github.com/test/repo', 'test'),
            ('github.com/simpleuser', 'simpleuser')
        ]

        for url, expected in test_cases:
            result = extract_username_from_url(url)
            assert result == expected

    def test_invalid_urls(self):
        """Test extraction from invalid URLs"""
        invalid_urls = [
            'https://gitlab.com/user',
            'https://bitbucket.org/user',
            'not-a-url',
            'https://github.com/',
            ''
        ]

        for url in invalid_urls:
            result = extract_username_from_url(url)
            assert result is None


class TestFlaskApp:
    """Test Flask application endpoints"""

    def setup_method(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'status' in data
        assert 'timestamp' in data
        assert data['status'] == 'healthy'

    def test_index_endpoint(self):
        """Test main page endpoint"""
        response = self.app.get('/')
        assert response.status_code == 200
        assert b'DevMeter' in response.data
        assert b'GitHub Profile URL' in response.data

    @patch('src.app.analyze_github_profile')
    def test_analyze_endpoint_success(self, mock_analyze):
        """Test successful profile analysis"""
        mock_analyze.return_value = {
            'profile': {'username': 'testuser'},
            'devmeter': {'score': 85, 'rating': '🍅 Fresh'}
        }

        response = self.app.post('/analyze',
                               data=json.dumps({'url': 'https://github.com/testuser'}),
                               content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'profile' in data
        assert 'devmeter' in data

    def test_analyze_endpoint_missing_url(self):
        """Test analyze endpoint with missing URL"""
        response = self.app.post('/analyze',
                               data=json.dumps({}),
                               content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_analyze_endpoint_invalid_url(self):
        """Test analyze endpoint with invalid URL"""
        response = self.app.post('/analyze',
                               data=json.dumps({'url': 'https://invalid.com/user'}),
                               content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data


class TestGitHubIntegration:
    """Test GitHub API integration (mocked)"""

    @patch('src.app.Github')
    def test_profile_analysis_structure(self, mock_github_class):
        """Test that profile analysis returns expected structure"""
        # Mock GitHub API responses
        mock_user = Mock()
        mock_user.login = 'testuser'
        mock_user.name = 'Test User'
        mock_user.bio = 'Test bio'
        mock_user.location = 'Test City'
        mock_user.company = 'Test Company'
        mock_user.blog = 'https://test.com'
        mock_user.followers = 10
        mock_user.following = 5
        mock_user.public_repos = 8
        mock_user.public_gists = 2

        mock_repo = Mock()
        mock_repo.name = 'test-repo'
        mock_repo.description = 'A test repository'
        mock_repo.language = 'Python'
        mock_repo.stargazers_count = 5
        mock_repo.forks_count = 2
        mock_repo.created_at = None
        mock_repo.updated_at = None
        mock_repo.fork = False

        mock_github_instance = Mock()
        mock_github_instance.get_user.return_value = mock_user
        mock_github_instance.get_user.return_value.get_repos.return_value = [mock_repo]
        mock_github_class.return_value = mock_github_instance

        result = analyze_github_profile('testuser')

        # Check basic structure
        assert 'profile' in result
        assert 'repositories' in result
        assert 'languages' in result
        assert 'devmeter' in result

        # Check profile data
        profile = result['profile']
        assert profile['username'] == 'testuser'
        assert profile['name'] == 'Test User'

        # Check DevMeter rating
        devmeter = result['devmeter']
        assert 'score' in devmeter
        assert 'rating' in devmeter
        assert 'recommendation' in devmeter


if __name__ == '__main__':
    pytest.main([__file__])