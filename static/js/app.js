document.addEventListener('DOMContentLoaded', loadProjects);

let selectedProjectId = null;

function loadProjects() {
    fetch('/api/projects')
        .then(response => response.json())
        .then(projects => {
            const projectsList = document.getElementById('projectsList');
            projectsList.innerHTML = '';

            projects.forEach(project => {
                const projectStatus = getProjectStatus(project.test_suites);
                
                const listItem = document.createElement('li');
                listItem.classList.add('menu-item');
                listItem.style.color = projectStatus === 'failed' ? 'red' : 'green'; // Set color based on status
                
                listItem.innerHTML = `<a href="#">${project.name}</a>`;
                listItem.onclick = () => {
                    selectedProjectId = project.id;
                    loadTestSuites(project);  // Load full project details
                };
                projectsList.appendChild(listItem);
            });

            // Auto-select the first project if no project is selected yet
            if (!selectedProjectId && projects.length > 0) {
                selectedProjectId = projects[0].id;
                loadTestSuites(projects[0]);
            }
        });
}

// Function to determine the overall status of the project based on its test suites
function getProjectStatus(testSuites) {
    let hasFailed = false;
    let allPassed = true;

    testSuites.forEach(suite => {
        if (suite.status === 'failed') {
            hasFailed = true;
        }
        if (suite.status !== 'passed') {
            allPassed = false;
        }
    });

    if (hasFailed) return 'failed';
    if (allPassed) return 'passed';
    return 'in_progress'; // If not all passed or failed, it's likely in progress
}

function loadTestSuites(project) {
    const testSuitesContainer = document.getElementById('testSuitesContainer');
    const projectName = document.getElementById('selectedProjectName');

    // Ensure project has name and test_suites before rendering
    if (project && project.name && project.test_suites) {
        projectName.innerText = project.name;
        testSuitesContainer.innerHTML = '';

        project.test_suites.forEach(suite => {
            const suiteDiv = document.createElement('div');
            suiteDiv.classList.add('suite');
            suiteDiv.innerHTML = `
                <h3>${suite.name}</h3>
                <p class="status ${suite.status}">${suite.status}</p>
                <p>Execution Time: ${suite.execution_time || 'N/A'} seconds</p>
                <p>Last Run: ${suite.last_run_timestamp || 'N/A'}</p>
                <div class="suite-actions">
                    <button onclick="changeStatus(${suite.id}, 'in_progress')">In Progress</button>
                    <button onclick="changeStatus(${suite.id}, 'passed')">Pass</button>
                    <button onclick="changeStatus(${suite.id}, 'failed')">Fail</button>
                    <button class="remove-suite-btn" onclick="deleteTestSuite(${suite.id})">Remove Test Suite</button>
                </div>
            `;
            testSuitesContainer.appendChild(suiteDiv);
        });
    } else {
        projectName.innerText = 'Project not found';
        testSuitesContainer.innerHTML = '<p>No test suites available.</p>';
    }
}

function changeStatus(suiteId, newStatus) {
    fetch(`/api/test-suite/${suiteId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
    })
    .then(() => {
        // Reload the current project's test suites
        loadProjectById(selectedProjectId);
    });
}

function deleteTestSuite(suiteId) {
    fetch(`/api/test-suite/${suiteId}`, {
        method: 'DELETE',
    })
    .then(() => loadProjectById(selectedProjectId));  // Reload the current project
}

function addProject() {
    const projectName = prompt('Enter new project name:');
    if (projectName) {
        fetch('/api/projects', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: projectName, test_suites: [] })
        })
        .then(() => loadProjects());
    }
}

function addTestSuite() {
    const testSuiteName = prompt('Enter new test suite name:');
    if (testSuiteName && selectedProjectId) {
        fetch(`/api/projects/${selectedProjectId}/test-suite`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: testSuiteName })
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to add test suite');
            }
        })
        .then(project => {
            // After successfully adding the test suite, reload the current project to update the UI
            loadProjectById(selectedProjectId);
        })
        .catch(error => {
            console.error('Error adding test suite:', error);
        });
    }
}

// Helper function to reload a project by ID
function loadProjectById(projectId) {
    fetch(`/api/projects/${projectId}`)
        .then(response => response.json())
        .then(project => {
            if (project && project.id) {
                loadTestSuites(project);  // Load the full project data
            } else {
                console.error('Failed to load project by ID:', projectId);
            }
        });
}

document.getElementById('addProjectBtn').addEventListener('click', addProject);
document.getElementById('addTestSuiteBtn').addEventListener('click', addTestSuite);
