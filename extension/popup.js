const startButton = document.getElementById("startButton");
const statusText = document.getElementById("status");


startButton.addEventListener("click", async () => {

    const prompt = document.getElementById("searchPrompt").value.trim();

    const numberOfLeads = Number(
        document.getElementById("leadCount").value
    );

    const messageTemplate = document.getElementById("messageTemplate").value.trim();


    if (!prompt || !messageTemplate) {

        statusText.textContent = "Please complete all fields.";
        return;
    }

    if (!Number.isInteger(numberOfLeads) ||
        numberOfLeads < 1 ||
        numberOfLeads > 50) {

        statusText.textContent = "Enter a number between 1 and 50.";
        return;
    }


    startButton.disabled = true;
    startButton.textContent = "Researching...";

    statusText.textContent = "Connecting to ReachPilot backend...";


    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/leads",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    prompt: prompt,
                    number_of_leads: numberOfLeads,
                    message_template: messageTemplate
                })
            }
        );


        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Research failed.");
        }


        // Save leads for the next extension milestone
        await chrome.storage.local.set({
            reachpilotLeads: data.leads,
            currentLeadIndex: 0
        });


        statusText.textContent =
            `Successfully discovered ${data.total} leads!`;

        startButton.textContent = "Research Complete";

    }

    catch (error) {

        statusText.textContent = error.message;

        startButton.disabled = false;
        startButton.textContent = "🚀 Start Outreach";

    }

});