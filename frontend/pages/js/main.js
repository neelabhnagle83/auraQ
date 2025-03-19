// Function to load components dynamically
function loadComponent(id, file) {
    fetch(file)
        .then(response => response.text())
        .then(data => {
            document.getElementById(id).innerHTML = data;
            // Add event listener to the logout button after the component is loaded
            if (id === "navbar") {
                const logoutButton = document.querySelector('.signout-btn');
                if (logoutButton) {
                    logoutButton.addEventListener('click', logout);
                }
            }
        })
        .catch(error => console.error(`Error loading ${file}:`, error));
}

// Load Navbar & Footer on all pages
document.addEventListener("DOMContentLoaded", () => {
    loadComponent("navbar", "/frontend/pages/navbar.html");
    loadComponent("footer", "/frontend/pages/footer.html");
});

// Logout function
function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    window.location.href = "login.html";
}

// Function to view a file
