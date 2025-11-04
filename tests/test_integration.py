"""
Integration tests for DevMeter - Real HTTP calls to running application
"""

import subprocess
import time
import requests
import pytest
import json
import os


class TestDevMeterIntegration:
    """Full integration tests with real HTTP calls to running DevMeter app"""

    @pytest.fixture(scope="class")
    def app_container(self):
        """Spin up Docker container for testing"""
        container_name = "devmeter-integration-test"

        # Clean up any existing container
        subprocess.run(["docker", "stop", container_name], capture_output=True)
        subprocess.run(["docker", "rm", container_name], capture_output=True)

        # Build and start container
        subprocess.run(["docker", "build", "-t", "devmeter-test", "."], check=True)

        process = subprocess.Popen([
            "docker", "run", "-d",
            "--name", container_name,
            "-p", "8081:8080",
            "-e", "FLASK_DEBUG=false",
            "devmeter-test"
        ])

        # Wait for application to be ready
        base_url = "http://localhost:8081"
        max_attempts = 30
        ready = False

        print("⏳ Waiting for DevMeter application to start...")

        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{base_url}/health", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "healthy":
                        ready = True
                        print(f"✅ Application ready after {attempt + 1} attempts")
                        break
            except requests.exceptions.RequestException:
                pass

            time.sleep(2)

        if not ready:
            # Get logs for debugging
            logs = subprocess.run(["docker", "logs", container_name],
                                capture_output=True, text=True)
            print("❌ Application failed to start. Container logs:")
            print(logs.stdout)
            print(logs.stderr)
            pytest.fail("Application failed to start within timeout")

        yield base_url

        # Cleanup
        print("🧹 Cleaning up test container...")
        subprocess.run(["docker", "stop", container_name], capture_output=True)
        subprocess.run(["docker", "rm", container_name], capture_output=True)
        subprocess.run(["docker", "rmi", "devmeter-test"], capture_output=True)

    def test_health_endpoint(self, app_container):
        """Test that the health endpoint works"""
        response = requests.get(f"{app_container}/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

        print("✅ Health check passed")

    def test_main_page_loads(self, app_container):
        """Test that the main web page loads"""
        response = requests.get(f"{app_container}/")

        assert response.status_code == 200
        assert b"DevMeter" in response.content
        assert b"GitHub Profile URL" in response.content

        print("✅ Main page loads successfully")

    def test_github_profile_analysis_octocat(self, app_container):
        """Test real GitHub profile analysis with octocat"""
        payload = {"url": "https://github.com/octocat"}

        print("🎯 Testing DevMeter analysis with GitHub profile: octocat")

        response = requests.post(
            f"{app_container}/analyze",
            json=payload,
            timeout=60  # GitHub API calls can be slow
        )

        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert "profile" in data
        assert "devmeter" in data
        assert "repositories" in data

        # Check DevMeter rating structure
        devmeter = data["devmeter"]
        assert "score" in devmeter
        assert "rating" in devmeter
        assert "recommendation" in devmeter
        assert "category_scores" in devmeter

        # Verify score is a valid percentage
        score = devmeter["score"]
        assert isinstance(score, int)
        assert 0 <= score <= 100

        # Print real results
        print("🎯 REAL DEVMETER ANALYSIS RESULTS:")
        print(f"   Profile: {data['profile'].get('name', 'N/A')} (@{data['profile'].get('username', 'N/A')})")
        print(f"   Score: {score}%")
        print(f"   Rating: {devmeter['rating']}")
        print(f"   Recommendation: {devmeter['recommendation']}")
        print(f"   Top Languages: {', '.join([lang for lang, _ in data.get('languages', [])[:3]])}")
        print(f"   Focus Areas: {', '.join(data.get('focus_areas', []))}")

        print("✅ Real GitHub profile analysis successful")

    def test_github_profile_analysis_jorgedlt(self, app_container):
        """Test real GitHub profile analysis with jorgedlt"""
        payload = {"url": "https://github.com/jorgedlt"}

        print("🎯 Testing DevMeter analysis with GitHub profile: jorgedlt")

        response = requests.post(
            f"{app_container}/analyze",
            json=payload,
            timeout=60
        )

        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert "profile" in data
        assert "devmeter" in data

        devmeter = data["devmeter"]
        score = devmeter["score"]

        # Print real results
        print("🎯 REAL DEVMETER ANALYSIS RESULTS:")
        print(f"   Profile: {data['profile'].get('name', 'N/A')} (@{data['profile'].get('username', 'N/A')})")
        print(f"   Score: {score}%")
        print(f"   Rating: {devmeter['rating']}")
        print(f"   Recommendation: {devmeter['recommendation']}")

        print("✅ Real GitHub profile analysis successful")

    def test_invalid_github_url(self, app_container):
        """Test error handling for invalid GitHub URL"""
        payload = {"url": "https://invalid-site.com/user"}

        response = requests.post(
            f"{app_container}/analyze",
            json=payload,
            timeout=30
        )

        assert response.status_code == 400
        data = response.json()
        assert "error" in data

        print("✅ Invalid URL error handling works")

    def test_missing_url_parameter(self, app_container):
        """Test error handling for missing URL parameter"""
        payload = {}

        response = requests.post(
            f"{app_container}/analyze",
            json=payload,
            timeout=30
        )

        assert response.status_code == 400
        data = response.json()
        assert "error" in data

        print("✅ Missing parameter error handling works")

    def test_curl_command_simulation(self, app_container):
        """Simulate curl command testing"""
        import subprocess

        # Test health endpoint with curl
        result = subprocess.run([
            "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
            f"{app_container}/health"
        ], capture_output=True, text=True)

        assert result.returncode == 0
        assert result.stdout.strip() == "200"

        print("✅ Curl command simulation successful")

        # Test analysis endpoint with curl
        curl_cmd = [
            "curl", "-s", "-X", "POST",
            "-H", "Content-Type: application/json",
            "-d", '{"url": "https://github.com/octocat"}',
            f"{app_container}/analyze"
        ]

        result = subprocess.run(curl_cmd, capture_output=True, text=True)

        assert result.returncode == 0

        # Parse JSON response
        try:
            data = json.loads(result.stdout)
            assert "devmeter" in data
            assert "score" in data["devmeter"]

            print(f"✅ Curl analysis result: {data['devmeter']['score']}% {data['devmeter']['rating']}")

        except json.JSONDecodeError:
            pytest.fail("Curl response is not valid JSON")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])