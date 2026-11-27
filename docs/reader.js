const root = document.documentElement;
const theme = document.getElementById("theme");
const storage = {
  get(key) { try { return localStorage.getItem("gyeong-" + key); } catch { return null; } },
  set(key, value) { try { localStorage.setItem("gyeong-" + key, value); } catch {} },
};

function setTheme(dark) {
  root.classList.toggle("dark", dark);
  theme.setAttribute("aria-pressed", String(dark));
}

setTheme(storage.get("dark") === "true");
theme.addEventListener("click", () => {
  const dark = !root.classList.contains("dark");
  setTheme(dark);
  storage.set("dark", dark);
});

let size = Number(storage.get("size")) || 19;
root.style.setProperty("--size", size + "px");
for (const button of document.querySelectorAll("[data-size]")) {
  button.addEventListener("click", () => {
    size = Math.min(28, Math.max(15, size + Number(button.dataset.size)));
    root.style.setProperty("--size", size + "px");
    storage.set("size", size);
  });
}

const chapter = document.querySelector("[data-chapter]");
if (chapter) storage.set("chapter", chapter.dataset.chapter);
const resume = document.getElementById("resume");
const last = storage.get("chapter");
if (resume && last && Array.from(document.links).some(link => link.getAttribute("href") === last + ".html")) {
  resume.href = last + ".html";
  resume.hidden = false;
}
