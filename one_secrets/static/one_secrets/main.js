document.addEventListener("DOMContentLoaded", () => {
  const showBtn = document.getElementById("show-uuid");
  const card = document.getElementById("uuid-field");
  const getBtn = document.getElementById("get-secret");
  const output = document.getElementById("secret-output");
  const input = document.getElementById("uuid-input");

  showBtn.addEventListener("click", () => {
    card.classList.toggle("active");
  });

  getBtn.addEventListener("click", async () => {
    const uuid = input.value.trim();
    if (!uuid) {
      output.textContent = "Введите UUID";
      return;
    }

    try {
      const res = await fetch(`/api/secrets/${uuid}/`);
      if (res.ok) {
        const data = await res.json();
        output.textContent = data.text;
      } else {
        output.textContent = "Секрет недоступен";
      }
    } catch {
      output.textContent = "Ошибка сети";
    }
  });
});
const overlay = document.getElementById("overlay");

showBtn.addEventListener("click", () => {
  card.classList.add("active");
  overlay.classList.add("active");
});

overlay.addEventListener("click", () => {
  card.classList.remove("active");
  overlay.classList.remove("active");
});
