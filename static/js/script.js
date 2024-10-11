// JavaScript code for the Flask app

// Add event listener to the document
document.addEventListener('DOMContentLoaded', function() {
  console.log('Document loaded');

  // Get the elements
  const projectNameInput = document.getElementById('project-name');
  const projectCreateButton = document.getElementById('project-create-button');
  const testSuitNameInput = document.getElementById('test-suit-name');
  const testSuitCreateButton = document.getElementById('test-suit-create-button');

  // Add event listeners to the buttons
  projectCreateButton.addEventListener('click', function() {
      const projectName = projectNameInput.value;
      console.log(`Creating project: ${projectName}`);

      // Send a POST request to the server to create a new project
      fetch('/projects/new', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name: projectName })
      })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));
  });

  testSuitCreateButton.addEventListener('click', function() {
      const testSuitName = testSuitNameInput.value;
      console.log(`Creating test suit: ${testSuitName}`);

      // Send a POST request to the server to create a new test suit
      fetch('/test_suits/new', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name: testSuitName })
      })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));
  });
});