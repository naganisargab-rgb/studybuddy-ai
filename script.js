const topic = document.getElementById("topic");
const button = document.getElementById("explainBtn");
const status = document.getElementById("status");
const result = document.getElementById("result");
const answer = document.getElementById("answer");

button.addEventListener("click", async () => {
    const value = topic.value.trim();

    if (!value) {
        status.textContent = "Please enter a topic first.";
        return;
    }

    button.disabled = true;
    status.textContent = "Your AI study buddy is thinking...";
    result.hidden = true;

    try {
        const response = await fetch("/api/study", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ topic: value })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        answer.textContent = data.answer;
        result.hidden = false;
        status.textContent = "Your explanation is ready! ✨";

    } catch (error) {
        status.textContent = error.message;
    } finally {
        button.disabled = false;
    }
});