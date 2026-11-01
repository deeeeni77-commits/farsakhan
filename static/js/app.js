document.addEventListener("DOMContentLoaded", () => {
    const menuButton = document.getElementById("mobileMenu");
    const sidebar = document.getElementById("sidebar");
    if (menuButton && sidebar) {
        menuButton.addEventListener("click", () => sidebar.classList.toggle("open"));
        document.addEventListener("click", (event) => {
            if (window.innerWidth <= 800 && sidebar.classList.contains("open") && !sidebar.contains(event.target) && event.target !== menuButton) {
                sidebar.classList.remove("open");
            }
        });
    }
});

window.showToast = function (message) {
    const toast = document.getElementById("toast");
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add("visible");
    window.setTimeout(() => toast.classList.remove("visible"), 2600);
};
