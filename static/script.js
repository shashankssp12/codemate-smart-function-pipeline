// Global variables
let functions = [];
let isLoading = false;

// DOM elements
const sidebar = document.getElementById("sidebar");
const sidebarToggle = document.getElementById("sidebarToggle");
const mobileMenuBtn = document.getElementById("mobileMenuBtn");
const chatContainer = document.getElementById("chatContainer");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const statusIndicator = document.getElementById("statusIndicator");
const functionsList = document.getElementById("functionsList");
const functionModal = document.getElementById("functionModal");
const modalClose = document.getElementById("modalClose");

// Initialize the app
document.addEventListener("DOMContentLoaded", function () {
  initializeApp();
  setupEventListeners();
  loadFunctions();
  checkServerStatus();
});

function initializeApp() {
  // Auto-resize textarea
  messageInput.addEventListener("input", function () {
    this.style.height = "auto";
    this.style.height = Math.min(this.scrollHeight, 120) + "px";
  });
  // Enable/disable send button based on input
  messageInput.addEventListener("input", function () {
    if (!isLoading) {
      sendButton.disabled = this.value.trim() === "";
    }
  });

  // Handle Enter key
  messageInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!sendButton.disabled) {
        sendMessage();
      }
    }
  });
}

function setupEventListeners() {
  // Send button
  sendButton.addEventListener("click", sendMessage);

  // Sidebar toggle
  sidebarToggle.addEventListener("click", toggleSidebar);
  mobileMenuBtn.addEventListener("click", toggleSidebar);

  // Modal close
  modalClose.addEventListener("click", closeModal);
  functionModal.addEventListener("click", function (e) {
    if (e.target === functionModal) {
      closeModal();
    }
  });

  // Example queries
  document.addEventListener("click", function (e) {
    if (e.target.classList.contains("example-query")) {
      const query = e.target.getAttribute("data-query");
      messageInput.value = query;
      messageInput.focus();
      sendButton.disabled = false;
    }
  });

  // Function items
  document.addEventListener("click", function (e) {
    if (e.target.closest(".function-item")) {
      const functionName = e.target
        .closest(".function-item")
        .getAttribute("data-function");
      showFunctionDetails(functionName);
    }
  });
}

async function loadFunctions() {
  try {
    const response = await fetch("/functions");
    const data = await response.json();
    functions = data.functions;
    displayFunctions(functions);
  } catch (error) {
    console.error("Error loading functions:", error);
    functionsList.innerHTML =
      '<div class="error-message">Failed to load functions</div>';
  }
}

function displayFunctions(functionsData) {
  // Simplified categories for our 10 core functions
  const categories = {
    "Invoice Management": ["get_invoices", "summarize_invoices"],
    Communication: ["send_email", "validate_email"],
    Mathematical: ["add_numbers", "check_prime"],
    Utility: [
      "get_current_time",
      "generate_random_number",
      "uppercase_string",
      "calculate_total",
    ],
  };

  let html = "";

  Object.entries(categories).forEach(([category, functionNames]) => {
    const categoryFunctions = functionNames.filter(
      (name) => functionsData[name]
    );
    if (categoryFunctions.length > 0) {
      html += `
                <div class="function-category">
                    <div class="category-title">${category}</div>
            `;

      categoryFunctions.forEach((functionName) => {
        const func = functionsData[functionName];
        html += `
                    <div class="function-item" data-function="${functionName}">
                        <div class="function-name">${functionName}</div>
                        <div class="function-description">${func.description}</div>
                    </div>
                `;
      });

      html += "</div>";
    }
  });

  functionsList.innerHTML = html;
}

function showFunctionDetails(functionName) {
  const func = functions[functionName];
  if (!func) return;

  const modalTitle = document.getElementById("modalTitle");
  const modalBody = document.getElementById("modalBody");

  modalTitle.textContent = functionName;

  const inputsHtml = Object.entries(func.inputs)
    .map(
      ([key, type]) =>
        `<li><code>${key}</code>: <span class="type">${type}</span></li>`
    )
    .join("");

  const outputsHtml = Object.entries(func.outputs)
    .map(
      ([key, type]) =>
        `<li><code>${key}</code>: <span class="type">${type}</span></li>`
    )
    .join("");

  modalBody.innerHTML = `
        <div class="function-details">
            <div class="detail-section">
                <h4>Description</h4>
                <p>${func.description}</p>
            </div>
            
            <div class="detail-section">
                <h4>Inputs</h4>
                <ul class="parameter-list">${inputsHtml}</ul>
            </div>
            
            <div class="detail-section">
                <h4>Outputs</h4>
                <ul class="parameter-list">${outputsHtml}</ul>
            </div>
            
            <div class="detail-section">
                <h4>Example Usage</h4>
                <div class="example-usage">
                    ${getExampleUsage(functionName)}
                </div>
            </div>
        </div>
    `;

  // Add styles for the modal content
  const style = document.createElement("style");
  style.textContent = `
        .function-details .detail-section {
            margin-bottom: 24px;
        }
        .function-details h4 {
            color: #1e293b;
            margin-bottom: 8px;
            font-weight: 600;
        }
        .parameter-list {
            list-style: none;
            background: #f8fafc;
            border-radius: 8px;
            padding: 16px;
        }
        .parameter-list li {
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .parameter-list li:last-child {
            margin-bottom: 0;
        }
        .parameter-list code {
            background: #e2e8f0;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Monaco', monospace;
            font-weight: 600;
        }
        .parameter-list .type {
            color: #6366f1;
            font-weight: 500;
        }
        .example-usage {
            background: #f0f9ff;
            border: 1px solid #0ea5e9;
            border-radius: 8px;
            padding: 16px;
            font-family: 'Monaco', monospace;
            font-size: 14px;
            color: #0369a1;
        }
    `;

  if (!document.getElementById("modal-styles")) {
    style.id = "modal-styles";
    document.head.appendChild(style);
  }

  functionModal.style.display = "block";
}

function getExampleUsage(functionName) {
  const examples = {
    get_invoices: '"get invoices for March" or "retrieve December invoices"',
    summarize_invoices: '"summarize the invoices" (use after getting invoices)',
    send_email:
      '"send an email to john@company.com with subject Monthly Report"',
    validate_email:
      '"is this email valid test@example.com" or "check email user@domain.com"',
    add_numbers: '"add 15 and 25" or "what is 45 plus 78"',
    get_current_time:
      '"what is the current time" or "show me the current date and time"',
    generate_random_number: '"generate a random number between 1 and 100"',
    uppercase_string: '"convert hello world to uppercase"',
    check_prime: '"is 17 a prime number" or "check if 29 is prime"',
    calculate_total:
      '"calculate total amount from invoices" (use with invoice data)',
  };

  return examples[functionName] || `"Use the ${functionName} function"`;
}

function closeModal() {
  functionModal.style.display = "none";
}

function toggleSidebar() {
  sidebar.classList.toggle("open");
}

async function sendMessage() {
  const message = messageInput.value.trim();
  if (!message || isLoading) return;

  // Add user message to chat
  addMessage(message, "user");

  // Clear input and disable send button
  messageInput.value = "";
  messageInput.style.height = "auto";
  sendButton.disabled = true;
  isLoading = true;
  // Update send button to show loading state
  sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
  sendButton.classList.add("loading");

  // Add loading message
  const loadingId = addLoadingMessage();

  try {
    const response = await fetch("/execute", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: message }),
    });

    const data = await response.json();
    removeLoadingMessage(loadingId);

    if (data.success) {
      addAIResponse(data);
    } else {
      addErrorMessage(data.error || "An error occurred");
    }
  } catch (error) {
    removeLoadingMessage(loadingId);
    addErrorMessage("Failed to connect to the server");
    console.error("Error:", error);
  } finally {
    isLoading = false;
    // Reset send button
    sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
    sendButton.classList.remove("loading");
    sendButton.disabled = false;
  }
}

function addMessage(content, sender) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message message-${sender}`;

  const contentDiv = document.createElement("div");
  contentDiv.className = "message-content";
  contentDiv.textContent = content;

  const timestampDiv = document.createElement("div");
  timestampDiv.className = "message-timestamp";
  timestampDiv.textContent = new Date().toLocaleTimeString();

  messageDiv.appendChild(contentDiv);
  messageDiv.appendChild(timestampDiv);

  // Remove welcome message if it exists
  const welcomeMessage = chatContainer.querySelector(".welcome-message");
  if (welcomeMessage) {
    welcomeMessage.remove();
  }

  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addAIResponse(data) {
  const messageDiv = document.createElement("div");
  messageDiv.className = "message message-ai";

  const contentDiv = document.createElement("div");
  contentDiv.className = "message-content";

  // Create result display
  let resultHtml = `
        <div class="result-container">
            <div class="result-summary">
                <h4>✅ Result</h4>
                <p>${data.summary}</p>
            </div>
    `;

  if (data.function_calls && data.function_calls.length > 0) {
    resultHtml += `
            <div class="function-calls">
                <h4>🔧 Functions Used</h4>
        `;

    data.function_calls.forEach((call) => {
      const inputsStr = JSON.stringify(call.inputs, null, 2);
      resultHtml += `
                <div class="function-call">
                    <div class="function-call-name">${call.function}</div>
                    <div class="function-call-inputs">${inputsStr}</div>
                </div>
            `;
    });

    resultHtml += "</div>";
  }

  // Show final output if available
  if (data.execution_result && data.execution_result.final_output) {
    const output = data.execution_result.final_output;
    let outputDisplay = "";

    Object.entries(output).forEach(([key, value]) => {
      if (typeof value === "boolean") {
        outputDisplay += `<div><strong>${key}:</strong> ${
          value ? "✅ Yes" : "❌ No"
        }</div>`;
      } else {
        outputDisplay += `<div><strong>${key}:</strong> ${value}</div>`;
      }
    });

    if (outputDisplay) {
      resultHtml += `
                <div style="background: #f0fdf4; border: 1px solid #22c55e; border-radius: 8px; padding: 16px; margin-top: 16px;">
                    <h4 style="color: #15803d; margin-bottom: 8px;">📊 Detailed Output</h4>
                    <div style="color: #15803d;">${outputDisplay}</div>
                </div>
            `;
    }
  }

  resultHtml += "</div>";
  contentDiv.innerHTML = resultHtml;

  const timestampDiv = document.createElement("div");
  timestampDiv.className = "message-timestamp";
  timestampDiv.textContent = new Date().toLocaleTimeString();

  messageDiv.appendChild(contentDiv);
  messageDiv.appendChild(timestampDiv);

  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addErrorMessage(error) {
  const messageDiv = document.createElement("div");
  messageDiv.className = "message message-ai";

  const contentDiv = document.createElement("div");
  contentDiv.className = "message-content";
  contentDiv.innerHTML = `
        <div class="error-message">
            <h4>❌ Error</h4>
            <p>${error}</p>
        </div>
    `;

  const timestampDiv = document.createElement("div");
  timestampDiv.className = "message-timestamp";
  timestampDiv.textContent = new Date().toLocaleTimeString();

  messageDiv.appendChild(contentDiv);
  messageDiv.appendChild(timestampDiv);

  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addLoadingMessage() {
  const messageDiv = document.createElement("div");
  messageDiv.className = "message message-ai loading-msg";

  const contentDiv = document.createElement("div");
  contentDiv.className = "message-content";

  // Random loading messages for variety
  const loadingMessages = [
    "🤖 Processing your request",
    "🔍 Analyzing your query",
    "⚡ Running functions",
    "🧠 Thinking",
    "🔧 Working on it",
  ];

  const randomMessage =
    loadingMessages[Math.floor(Math.random() * loadingMessages.length)];

  contentDiv.innerHTML = `
        <div class="loading-message">
            <i class="fas fa-spinner fa-spin"></i>
            <span>${randomMessage}</span>
        </div>
    `;

  const id = Date.now().toString();
  messageDiv.setAttribute("data-loading-id", id);

  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  return id;
}

function removeLoadingMessage(id) {
  const loadingMsg = document.querySelector(`[data-loading-id="${id}"]`);
  if (loadingMsg) {
    loadingMsg.remove();
  }
}

async function checkServerStatus() {
  try {
    const response = await fetch("/health");
    const data = await response.json();

    const statusDot = document.querySelector(".status-dot");
    const statusText = document.querySelector(".status-text");

    if (data.status === "healthy") {
      statusDot.className = "status-dot";
      statusText.textContent = "Connected";
    } else {
      statusDot.className = "status-dot connecting";
      statusText.textContent = "Degraded";
    }
  } catch (error) {
    const statusDot = document.querySelector(".status-dot");
    const statusText = document.querySelector(".status-text");

    statusDot.className = "status-dot error";
    statusText.textContent = "Disconnected";
  }
}

// Check server status periodically
setInterval(checkServerStatus, 30000);
