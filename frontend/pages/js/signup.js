document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signup-form");
    const passwordInput = document.getElementById("signup-password");
    const togglePassword = document.getElementById("toggleSignupPassword");

    // Toggle password visibility
    togglePassword.addEventListener("click", function () {
        passwordInput.type = passwordInput.type === "password" ? "text" : "password";
        togglePassword.src = passwordInput.type === "password" ? "./assets/mdi_hide.png" : "./assets/mdi_show.png";
    });

    // Signup form submission
    signupForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        const username = document.getElementById("username").value.trim();
        const password = passwordInput.value.trim();

        if (!username || !password) {
            alert("❌ Username and password are required!");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:5000/auth/signup", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });

            const result = await response.json();

            if (response.ok) {
                alert("✅ Signup successful! Please login.");
                window.location.href = "login.html";
            } else {
                alert("❌ " + (result.error || "Signup failed. Please try again."));
            }
        } catch (error) {
            console.error("Signup Error:", error);
            alert("❌ Signup failed. Try again later.");
        }
    });
});
