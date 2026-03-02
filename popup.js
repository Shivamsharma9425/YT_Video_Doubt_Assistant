const askButton = document.getElementById("askBtn");
const questionInput = document.getElementById("question");
const resultBox = document.getElementById("result");

async function askAI() {
  try {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (!tab.url.includes("youtube.com/watch")) {
      resultBox.innerText = "Open a YouTube video first.";
      return;
    }

    let url = new URL(tab.url);
    let videoId = url.searchParams.get("v");

    let question = questionInput.value.trim();

    if (!question) {
      resultBox.innerText = "Please type your question.";
      return;
    }

    resultBox.innerText = "Thinking... ";

    const response = await fetch("http://127.0.0.1:8000/summarize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        video_id: videoId,
        question: question
      })
    });

    const data = await response.json();

    resultBox.innerText = data.summary;

  } catch (error) {
    console.error(error);
    resultBox.innerText =
      "Backend error. Make sure FastAPI is running.";
  }
}

// Button click
askButton.addEventListener("click", askAI);

//  enter key support
questionInput.addEventListener("keydown", function (event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();  
    askAI();
  }
});