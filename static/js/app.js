document.addEventListener('DOMContentLoaded', loadProjects);

let selectedProjectId = null;
let selectedTestSuite = null;

// Function to load projects in the sidebar
function loadProjects() {
    fetch('/api/projects')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch projects');
            }
            return response.json();
        })
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
        })
        .catch(error => {
            console.error('Error loading projects:', error);
            alert('Failed to load projects. Please try again.');
        });
}

// Function to load test suites into the main area
function loadTestSuites(project) {
    const testSuitesContainer = document.getElementById('testSuitesContainer');
    const projectName = document.getElementById('selectedProjectName');

    projectName.innerText = project.name;
    testSuitesContainer.innerHTML = '';

    if (project.test_suites.length === 0) {
        testSuitesContainer.innerHTML = '<p>No test suites available. Add one using the button above.</p>';
        return;
    }

    project.test_suites.forEach(suite => {
        const suiteDiv = document.createElement('div');
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

// Add buttons to update test suite status
document.getElementById('inProgressBtn').addEventListener('click', () => updateTestSuiteStatus('in_progress'));
document.getElementById('passBtn').addEventListener('click', () => updateTestSuiteStatus('passed'));
document.getElementById('failBtn').addEventListener('click', () => updateTestSuiteStatus('failed'));

// Function to update the status of the selected test suite
function updateTestSuiteStatus(newStatus) {
    if (!selectedTestSuite) return;

    // Disable buttons while the request is in progress
    document.getElementById('inProgressBtn').disabled = true;
    document.getElementById('passBtn').disabled = true;
    document.getElementById('failBtn').disabled = true;

    fetch(`/api/test-suite/${selectedTestSuite.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update status');
        }
        return response.json();
    })
    .then(() => {
        selectedTestSuite.status = newStatus;
        openTestSuiteDetails(selectedTestSuite); // Refresh the right panel with updated data
        loadProjects(); // Reload projects to update the project status
    })
    .catch(error => {
        console.error('Error updating test suite status:', error);
        alert('Failed to update status. Please try again.');
    })
    .finally(() => {
        // Re-enable buttons after the request is complete
        document.getElementById('inProgressBtn').disabled = false;
        document.getElementById('passBtn').disabled = false;
        document.getElementById('failBtn').disabled = false;
    });
}

// Function to add a new test suite
document.getElementById('addTestSuiteBtn').addEventListener('click', addTestSuite);

function addTestSuite() {
    const testSuiteName = prompt('Enter new test suite name:');
    if (testSuiteName && selectedProjectId) {
        fetch(`/api/projects/${selectedProjectId}/test-suite`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: testSuiteName })
        })
        .then(response => response.json())
        .then(newSuite => {
            // Append the new suite to the DOM instead of reloading everything
            const suiteDiv = document.createElement('div');
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
}
