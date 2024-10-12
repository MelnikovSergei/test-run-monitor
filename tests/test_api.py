import pytest
import requests

# Base URL for your Flask app
BASE_URL = "http://127.0.0.1:5000"  # Ensure your app is running on this URL

# Test adding a new project
def test_add_project():
    payload = {
        'name': 'Test Project',
        'test_suites': []
    }
    response = requests.post(f"{BASE_URL}/api/projects", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert data['name'] == 'Test Project'
    assert isinstance(data['test_suites'], list)


# Test retrieving all projects
def test_get_projects():
    response = requests.get(f"{BASE_URL}/api/projects")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Should return a list of projects

# Test adding a test suite to an existing project
def test_add_test_suite():
    project_id = 1  # Replace with a valid project ID
    payload = {
        'name': 'New Test Suite'
    }
    response = requests.post(f"{BASE_URL}/api/projects/{project_id}/test-suite", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert data['name'] == 'New Test Suite'
    assert data['project_id'] == project_id
    assert data['status'] == 'not_run'


# Test updating the status of a test suite
def test_update_test_suite_status():
    # Create a project to attach the test suite
    project_payload = {'name': 'Project for Status Update', 'test_suites': []}
    project_response = requests.post(f"{BASE_URL}/api/projects", json=project_payload)
    project_id = project_response.json()['id']

    # Create a test suite within the new project
    suite_payload = {'name': 'Test Suite for Status Update'}
    suite_response = requests.post(f"{BASE_URL}/api/projects/{project_id}/test-suite", json=suite_payload)
    test_suite_id = suite_response.json()['id']

    # Now update the status of the created test suite
    payload = {
        'status': 'in_progress'
    }
    response = requests.patch(f"{BASE_URL}/api/test-suite/{test_suite_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'in_progress'


# Test removing a test suite
def test_remove_test_suite():
    # Create a project to attach the test suite
    project_payload = {'name': 'Project for Test Suite Removal', 'test_suites': []}
    project_response = requests.post(f"{BASE_URL}/api/projects", json=project_payload)
    project_id = project_response.json()['id']

    # Create a test suite within the new project
    suite_payload = {'name': 'Test Suite for Removal'}
    suite_response = requests.post(f"{BASE_URL}/api/projects/{project_id}/test-suite", json=suite_payload)
    test_suite_id = suite_response.json()['id']

    # Now delete the created test suite
    response = requests.delete(f"{BASE_URL}/api/test-suite/{test_suite_id}")
    assert response.status_code == 204  # No content

