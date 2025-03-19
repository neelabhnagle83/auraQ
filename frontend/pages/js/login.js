document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");
    const passwordInput = document.getElementById("password");
    const togglePassword = document.getElementById("togglePassword");

    // Toggle password visibility
    togglePassword.addEventListener("click", function () {
        passwordInput.type = passwordInput.type === "password" ? "text" : "password";
        togglePassword.src = passwordInput.type === "password" ? "./assets/mdi_hide.png" : "./assets/mdi_show.png";
    });

    // Login form submission
    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        const username = document.getElementById("username").value;
        const password = passwordInput.value;

        try {
            const response = await fetch("http://127.0.0.1:5000/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });

            const result = await response.json();

            if (response.ok) {
                alert("✅ Login successful!");
                localStorage.setItem("token", result.token);
                localStorage.setItem("username", username);
                window.location.href = "../dashboard.html"; // Redirect after login
            } else {
                alert("❌ " + (result.error || "Invalid credentials!"));
            }
        } catch (error) {
            console.error("Login Error:", error);
            alert("❌ Login failed. Try again later.");
        }
    });
});
