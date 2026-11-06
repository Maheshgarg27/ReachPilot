// =====================================
// REACHPILOT LINKEDIN PANEL
// =====================================

let leads = [];
let currentIndex = 0;


// =====================================
// CREATE PANEL
// =====================================

function createPanel() {

    if (document.getElementById("reachpilot-panel")) {
        return;
    }

    const panel = document.createElement("div");

    panel.id = "reachpilot-panel";

    panel.innerHTML = `

        <div class="rp-header">
            <span>🚀 ReachPilot</span>
            <button id="rp-minimize">−</button>
        </div>

        <div class="rp-content">

            <div class="rp-progress">
                Lead <span id="rp-current">0</span>
                of <span id="rp-total">0</span>
            </div>

            <h3 id="rp-name">Loading...</h3>

            <p id="rp-company"></p>

            <p id="rp-designation"></p>

            <div id="rp-status">
                Waiting for leads...
            </div>

            <div class="rp-buttons">

                <button id="rp-previous">
                    ← Previous
                </button>

                <button id="rp-next">
                    Next →
                </button>

            </div>

            <button id="rp-skip">
                Skip Lead
            </button>

        </div>
    `;

    document.body.appendChild(panel);

    addStyles();

    document.getElementById("rp-minimize").onclick = () => {

        const content = document.querySelector(".rp-content");

        content.style.display =
            content.style.display === "none" ? "block" : "none";

    };

    document.getElementById("rp-next").onclick = nextLead;

    document.getElementById("rp-previous").onclick = previousLead;

    document.getElementById("rp-skip").onclick = skipLead;

    loadLeads();
}


// =====================================
// PANEL STYLING
// =====================================

function addStyles() {

    const style = document.createElement("style");

    style.textContent = `

        #reachpilot-panel {
            position: fixed;
            top: 160px;
            right: 20px;
            width: 280px;
            background: #111827;
            color: white;
            border-radius: 12px;
            z-index: 999999;
            font-family: Arial, sans-serif;
            box-shadow: 0 5px 25px rgba(0,0,0,0.4);
        }

        #reachpilot-panel button {
            cursor: pointer;
            border: none;
            border-radius: 6px;
            padding: 10px;
            background: #2563eb;
            color: white;
            font-weight: bold;
        }

        .rp-header {
            display: flex;
            justify-content: space-between;
            padding: 14px;
            background: #1e3a8a;
            border-radius: 12px 12px 0 0;
            font-weight: bold;
        }

        .rp-header button {
            background: transparent;
            font-size: 18px;
        }

        .rp-content {
            padding: 16px;
        }

        .rp-progress {
            color: #93c5fd;
            font-size: 13px;
        }

        #rp-name {
            font-size: 18px;
            margin-bottom: 5px;
        }

        #rp-company,
        #rp-designation {
            color: #d1d5db;
            font-size: 13px;
        }

        #rp-status {
            padding: 10px;
            background: #1f2937;
            border-radius: 6px;
            font-size: 12px;
            margin-top: 12px;
        }

        .rp-buttons {
            display: flex;
            gap: 8px;
            margin-top: 16px;
        }

        .rp-buttons button {
            flex: 1;
        }

        #rp-skip {
            width: 100%;
            margin-top: 10px;
            background: #374151;
        }

    `;

    document.head.appendChild(style);
}


// =====================================
// LOAD LEADS FROM CHROME STORAGE
// =====================================

async function loadLeads() {

    const data = await chrome.storage.local.get([
        "reachpilotLeads",
        "currentLeadIndex"
    ]);

    leads = data.reachpilotLeads || [];

    currentIndex = data.currentLeadIndex || 0;

    if (currentIndex >= leads.length) {
        currentIndex = 0;
    }

    displayLead();
}


// =====================================
// DISPLAY CURRENT LEAD
// =====================================

function displayLead() {

    if (leads.length === 0) {

        document.getElementById("rp-name").textContent =
            "No leads available";

        document.getElementById("rp-company").textContent =
            "Start an outreach campaign first.";

        document.getElementById("rp-designation").textContent = "";

        document.getElementById("rp-current").textContent = "0";

        document.getElementById("rp-total").textContent = "0";

        return;
    }

    const lead = leads[currentIndex];

    document.getElementById("rp-current").textContent =
        currentIndex + 1;

    document.getElementById("rp-total").textContent =
        leads.length;

    document.getElementById("rp-name").textContent =
        lead.name || "Unknown";

    document.getElementById("rp-company").textContent =
        lead.company || "Unknown company";

    document.getElementById("rp-designation").textContent =
        lead.designation || "";

    document.getElementById("rp-status").textContent =
        "Status: " + (lead.status || "Pending");
}


// =====================================
// SAVE CURRENT INDEX
// =====================================

async function saveIndex() {

    await chrome.storage.local.set({
        currentLeadIndex: currentIndex
    });

}


// =====================================
// CHECK IF CURRENT LINKEDIN PROFILE MATCHES
// =====================================

function isCurrentLeadProfile(lead) {

    if (!lead.linkedin_url) return false;

    try {
        const current = new URL(window.location.href);
        const target = new URL(lead.linkedin_url);

        return current.pathname.replace(/\/$/, "") ===
               target.pathname.replace(/\/$/, "");

    } catch {
        return false;
    }
}


// =====================================
// OPEN CURRENT LEAD PROFILE
// =====================================

async function openCurrentLead() {

    const lead = leads[currentIndex];

    if (!lead) return;

    const url = lead.linkedin_url;

    if (!url || !/^https:\/\/(www\.|[a-z]{2}\.)?linkedin\.com\/in\//i.test(url)) {

        alert("This lead does not have a valid LinkedIn profile URL.");
        return;
    }

    await saveIndex();

    window.location.href = url;
}


// =====================================
// NEXT LEAD
// =====================================

async function nextLead() {

    if (!leads.length) return;

    if (!isCurrentLeadProfile(leads[currentIndex])) {
        await openCurrentLead();
        return;
    }

    if (currentIndex < leads.length - 1) {

        currentIndex++;

        await saveIndex();

        await openCurrentLead();

    } else {

        alert("You have reached the last lead!");
    }
}


// =====================================
// PREVIOUS LEAD
// =====================================

async function previousLead() {

    if (!leads.length) return;

    if (currentIndex > 0) {

        currentIndex--;

        await saveIndex();

        await openCurrentLead();
    }
}


// =====================================
// SKIP LEAD
// =====================================

async function skipLead() {

    if (!leads.length) return;

    leads[currentIndex].status = "Skipped";

    await chrome.storage.local.set({
        reachpilotLeads: leads
    });

    if (currentIndex < leads.length - 1) {

        currentIndex++;

        await saveIndex();

        await openCurrentLead();

    } else {

        displayLead();

        alert("You have reached the last lead!");
    }
}

// =====================================
// INITIALIZE
// =====================================

if (document.readyState === "loading") {

    document.addEventListener("DOMContentLoaded", createPanel);

} else {

    createPanel();

}