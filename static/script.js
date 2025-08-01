document.addEventListener("mousemove", function(e) {
    const cursor = document.querySelector(".cursor-effect");
    if (cursor) {
        cursor.style.left = e.clientX + "px";
        cursor.style.top = e.clientY + "px";
    }
});

window.onload = () => {
    const cursor = document.createElement("div");
    cursor.classList.add("cursor-effect");
    document.body.appendChild(cursor);

    document.addEventListener("click", () => {
        cursor.classList.add("clicked");
        setTimeout(() => {
            cursor.classList.remove("clicked");
        }, 100);
    });
};

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});