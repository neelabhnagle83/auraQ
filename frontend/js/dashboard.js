document.addEventListener("DOMContentLoaded", function () {
    const storyForm = document.getElementById("story-form");
    const storyInput = document.getElementById("story-input");
    const moodDisplay = document.getElementById("mood-display");
    const feedbackDisplay = document.getElementById("feedback-display");
    const rewardDisplay = document.getElementById("reward-points"); // Updated ID
    const usernameDisplay = document.getElementById("username");
    const dateDisplay = document.getElementById("current-date");

    let dailyStoryCount = 0;
    let rewards = parseInt(localStorage.getItem("rewards")) || 5; // Default 5 on signup

    // Function to check and reset daily story count
    function checkDailyReset() {
        const lastResetDate = localStorage.getItem("lastResetDate");
        const today = new Date().toLocaleDateString();

        if (lastResetDate !== today) {
            dailyStoryCount = 0;
            localStorage.setItem("dailyStoryCount", "0"); // Store as string
            localStorage.setItem("lastResetDate", today);
        } else {
            dailyStoryCount = parseInt(localStorage.getItem("dailyStoryCount")) || 0; // Retrieve stored count
        }
    }

    // Call checkDailyReset when the page loads
    checkDailyReset();

    // Load stored username and current date
    usernameDisplay.textContent = localStorage.getItem("username") || "User";
    dateDisplay.textContent = new Date().toDateString();

    // Update reward display
    rewardDisplay.textContent = rewards;

    // Initialize weekly mood review
    initializeWeeklyMoodReview();

    storyForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const storyText = storyInput.value.trim();
        if (!storyText) {
            alert("⚠️ Please enter your story!");
            return;
        }

        if (dailyStoryCount >= 2) {
            rewards -= 3;
            if (rewards < 0) rewards = 0; // Ensure rewards don't go negative
            alert("⚠️ You've reached the daily limit. -3 credits.");
        } else {
            rewards++;
        }

        try {
            const response = await fetch("https://auraq.onrender.com/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ story: storyText })
            });
            console.log("🚀 Response received:", response);
            const result = await response.json();
            console.log("🔍 Parsed JSON:", result);

            if (response.ok) {
                moodDisplay.textContent = `Mood: ${result.mood}`;
                feedbackDisplay.textContent = `Feedback: ${result.feedback}`;

                // Store mood data for weekly review
                let weeklyData = JSON.parse(localStorage.getItem("weeklyMoods")) || [];
                weeklyData.push({ mood: result.mood, date: new Date().toLocaleDateString() });
                localStorage.setItem("weeklyMoods", JSON.stringify(weeklyData));

                // Update weekly review after adding new data
                initializeWeeklyMoodReview();
            } else {
                moodDisplay.textContent = "Mood: Error!";
                feedbackDisplay.textContent = `Feedback: ${result.error}`;
            }

            if (dailyStoryCount < 2) {
                dailyStoryCount++;
                localStorage.setItem("dailyStoryCount", dailyStoryCount.toString()); // Store updated count
            }

            // Update UI and save to local storage
            rewardDisplay.textContent = rewards;
            localStorage.setItem("rewards", rewards);
            storyInput.value = "";

        } catch (error) {
            console.error("🔥 Error analyzing story:", error);
            moodDisplay.textContent = "Mood: Error!";
            feedbackDisplay.textContent = "Feedback: Failed to analyze.";
        }
    });
    
    // Load footer content
    fetch("../components/footer.html")
    .then(response => response.text())
    .then(data => {
        document.getElementById("footer").innerHTML = data;
    });
});

// Function to initialize weekly mood review
function initializeWeeklyMoodReview() {
    const weeklyReview = document.getElementById("weekly-review");
    if (!weeklyReview) return; // Safety check
    
    let weeklyData = JSON.parse(localStorage.getItem("weeklyMoods")) || [];

    if (weeklyData.length > 0) {
        let moodSummary = analyzeWeeklyMood(weeklyData);
        weeklyReview.textContent = `📅 Weekly Summary: ${moodSummary}`;
    } else {
        weeklyReview.textContent = "No data yet.";
    }
}

// Function to analyze weekly mood
function analyzeWeeklyMood(data) {
    let moodCounts = {};
    data.forEach(entry => {
        moodCounts[entry.mood] = (moodCounts[entry.mood] || 0) + 1;
    });

    let mostFrequentMood = Object.keys(moodCounts).reduce((a, b) => moodCounts[a] > moodCounts[b] ? a : b, "");
    console.log("Most Frequent Mood:", mostFrequentMood); // Add this line

    return `Mostly ${mostFrequentMood}, keep journaling!`;
}

