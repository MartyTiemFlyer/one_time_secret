document.addEventListener("DOMContentLoaded", () => {
  const showBtn = document.getElementById("show-uuid");
  const card = document.getElementById("uuid-field");
  const getBtn = document.getElementById("get-secret");
  const output = document.getElementById("secret-output");
  const input = document.getElementById("uuid-input");

  showBtn.addEventListener("click", () => {
  card.classList.toggle("active");
  });

    requestAnimationFrame(() => card.classList.add("show"));
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
