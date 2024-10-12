document.addEventListener('DOMContentLoaded', loadProjects);

let selectedProjectId = null;
let selectedTestSuite = null;

// Function to load projects in the sidebar
function loadProjects() {
    fetch('/api/projects')
        .then(response => response.json())
        .then(projects => {
            const projectsList = document.getElementById('projectsList');
            projectsList.innerHTML = '';

            projects.forEach(project => {
                const listItem = document.createElement('li');
                listItem.classList.add('menu-item');
                listItem.innerHTML = `<a href="#">${project.name}</a>`;
                listItem.onclick = () => {
                    selectedProjectId = project.id;
                    loadTestSuites(project);
                };
                projectsList.appendChild(listItem);
            });
        });
}

// Function to load test suites into the main area
function loadTestSuites(project) {
    const testSuitesContainer = document.getElementById('testSuitesContainer');
    const projectName = document.getElementById('selectedProjectName');

    projectName.innerText = project.name;
    testSuitesContainer.innerHTML = '';

    if (project.test_suites.length === 0) {
        testSuitesContainer.innerHTML = '<p>No test suites available. Add one using the input above.</p>';
        return;
    }

    project.test_suites.forEach(suite => {
        const suiteDiv = document.createElement('div');
        suiteDiv.id = `suite-${suite.id}`; // Use the ID to uniquely identify the suite
        suiteDiv.classList.add('suite-item', suite.status);
        suiteDiv.innerHTML = `
            <h3>${suite.name}</h3>
            <p>Status: ${suite.status}</p>
        `;
        suiteDiv.onclick = () => openTestSuiteDetails(suite); // Open details in the right panel
        testSuitesContainer.appendChild(suiteDiv);
    });
}

// Function to open the right panel with test suite details
function openTestSuiteDetails(suite) {
    selectedTestSuite = suite;

    const rightPanel = document.getElementById('rightPanel');
    const suiteName = document.getElementById('suiteName');
    const suiteStatus = document.getElementById('suiteStatus');
    const suiteExecutionTime = document.getElementById('suiteExecutionTime');
    const suiteLastRun = document.getElementById('suiteLastRun');
    const mainArea = document.getElementById('mainArea');
    
    suiteName.textContent = suite.name;
    suiteStatus.textContent = suite.status;
    suiteExecutionTime.textContent = suite.execution_time || 'N/A';
    suiteLastRun.textContent = suite.last_run_timestamp || 'N/A';

    // Add event listeners for the status update buttons inside the details panel
    document.getElementById('inProgressBtn').onclick = () => updateTestSuiteStatus('in_progress');
    document.getElementById('passBtn').onclick = () => updateTestSuiteStatus('passed');
    document.getElementById('failBtn').onclick = () => updateTestSuiteStatus('failed');

    // Slide in the right panel and adjust main area
    rightPanel.classList.add('open');
    mainArea.classList.add('adjusted');
}

// Function to close the right panel
document.getElementById('closePanelBtn').addEventListener('click', () => {
    const rightPanel = document.getElementById('rightPanel');
    const mainArea = document.getElementById('mainArea');
    
    rightPanel.classList.remove('open');
    mainArea.classList.remove('adjusted');
});

// Add event listener for adding a project when pressing "Enter"
document.getElementById('addProjectInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        const projectName = this.value.trim();
        if (projectName) {
            addProject(projectName);
            this.value = ''; // Clear the input box
        }
    }
});

// Function to add a new project
function addProject(projectName) {
    fetch('/api/projects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: projectName, test_suites: [] })
    })
    .then(() => loadProjects())
    .catch(error => {
        console.error('Error adding project:', error);
        alert('Failed to add project. Please try again.');
    });
}

// Add event listener for adding a test suite when pressing "Enter"
document.getElementById('addTestSuiteInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        const testSuiteName = this.value.trim();
        if (testSuiteName && selectedProjectId) {
            addTestSuite(testSuiteName);
            this.value = ''; // Clear the input box
        }
    }
});

// Function to add a new test suite
function addTestSuite(testSuiteName) {
    fetch(`/api/projects/${selectedProjectId}/test-suite`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: testSuiteName })
    })
    .then(response => response.json())
    .then(newSuite => {
        // Append the new suite to the DOM instead of reloading everything
        const suiteDiv = document.createElement('div');
        suiteDiv.id = `suite-${newSuite.id}`;
        suiteDiv.classList.add('suite-item', newSuite.status);
        suiteDiv.innerHTML = `
            <h3>${newSuite.name}</h3>
            <p>Status: ${newSuite.status}</p>
        `;
        suiteDiv.onclick = () => openTestSuiteDetails(newSuite);
        document.getElementById('testSuitesContainer').appendChild(suiteDiv);
    })
    .catch(error => {
        console.error('Error adding test suite:', error);
        alert('Failed to add test suite. Please try again.');
    });
}

// Function to update the status of the selected test suite
function updateTestSuiteStatus(newStatus) {
    if (!selectedTestSuite) return;

    fetch(`/api/test-suite/${selectedTestSuite.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => response.json())
    .then(() => {
        selectedTestSuite.status = newStatus;

        // Update the status dynamically by targeting the suite div by its ID
        const suiteDiv = document.getElementById(`suite-${selectedTestSuite.id}`);
        if (suiteDiv) {
            // Remove previous status classes and add the new one
            suiteDiv.classList.remove('failed', 'passed', 'in_progress', 'not_run');
            suiteDiv.classList.add(newStatus);
            suiteDiv.querySelector('p').textContent = `Status: ${newStatus}`;
        }
    })
    .catch(error => {
        console.error('Error updating test suite status:', error);
        alert('Failed to update status. Please try again.');
    });
}

// Function to remove a test suite dynamically without refreshing
document.getElementById('removeSuiteBtn').addEventListener('click', () => {
    if (!selectedTestSuite) return;

    fetch(`/api/test-suite/${selectedTestSuite.id}`, {
        method: 'DELETE'
    })
    .then(() => {
        const suiteDiv = document.getElementById(`suite-${selectedTestSuite.id}`);
        if (suiteDiv) {
            suiteDiv.remove();
        }

        // Close the right panel after removal
        document.getElementById('rightPanel').classList.remove('open');
        document.getElementById('mainArea').classList.remove('adjusted');
    })
    .catch(error => {
        console.error('Error removing test suite:', error);
        alert('Failed to remove test suite. Please try again.');
    });
});
