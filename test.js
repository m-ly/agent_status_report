document.addEventListener("DOMContentLoaded", function () {
  const criterionFields = document.getElementById("criteriaFields");
  const addCriterionButton = document.getElementById("addCriterion");
  const addSubsectionButton = document.getElementById("addSubsection");
  const addTextBoxButton = document.getElementById("addTextBox");

  addCriterionButton.addEventListener("click", function () {
    const newField = document.createElement("div");
    newField.classList.add("field");
    newField.innerHTML = `
      <div>
        <p class="page-header">Daily Rating</p>
        <div class="chart-scale">
          <button class="btn btn-scale btn-scale-asc-1">1</button>
          <button class="btn btn-scale btn-scale-asc-2">2</button>
          <button class="btn btn-scale btn-scale-asc-3">3</button>
          <button class="btn btn-scale btn-scale-asc-4">4</button>
          <button class="btn btn-scale btn-scale-asc-5">5</button>
          <button class="btn btn-scale btn-scale-asc-6">6</button>
          <button class="btn btn-scale btn-scale-asc-7">7</button>
          <button class="btn btn-scale btn-scale-asc-8">8</button>
          <button class="btn btn-scale btn-scale-asc-9">9</button>
          <button class="btn btn-scale btn-scale-asc-10">10</button>
        </div>
      </div>

      <div>
        <label for="info">
          <textarea name="text" rows=15 columns=300 placeholder=""></textarea>
        </label>
      </div>
    `;
    criterionFields.appendChild(newField);
  });

  addSubsectionButton.addEventListener("click", function() {
    const newField = document.createElement("div");
    newField.classList.add("subsection");
    newField.innerHTML = `
       <h2><%= info[:text] %></h2>
    `;
    criterionFields.appendChild(newField);
  });

  addTextBoxButton.addEventListener("click", function() {
    const newField = document.createElement("div");
    newField.classList.add("text-box");
    newField.innerHTML = `
      <div>
        <label for="text">
          <textarea name="text" rows=15 columns=300 placeholder=""></textarea>
        </label>
      </div>
    `;
    criterionFields.appendChild(newField);
  });



  const form = document.getElementById("evaluationForm");

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    // Handle form submission using AJAX or other method
    const formData = new FormData(form);
    // Send formData to the server for processing
    // Example using fetch API:
    fetch("/submit-evaluation", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        // Handle the response as needed
      })
      .catch((error) => {
        // Handle errors
      });
  });
});
