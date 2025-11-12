document.addEventListener("DOMContentLoaded", () => {
  const openBtn = document.getElementById("openAssistant");
  const closeBtn = document.getElementById("closeAssistant");
  const box = document.getElementById("assistantBox");
  const sendBtn = document.getElementById("sendMsg");
  const chatArea = document.getElementById("chatArea");
  const input = document.getElementById("userMessage");

  openBtn.addEventListener("click", () => {
    box.classList.remove("hidden");
    openBtn.classList.add("hidden");
  });

  closeBtn.addEventListener("click", () => {
    box.classList.add("hidden");
    openBtn.classList.remove("hidden");
  });

  sendBtn.addEventListener("click", async () => {
    const msg = input.value.trim();
    if (!msg) return;
    chatArea.innerHTML += `<div class='text-right mb-2'><b>أنت:</b> ${msg}</div>`;
    input.value = "";

    const res = await fetch("/api/assistant", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg })
    });

    const data = await res.json();
    chatArea.innerHTML += `<div class='text-left mb-2 text-blue-700'><b>🤖:</b> ${data.reply}</div>`;
    chatArea.scrollTop = chatArea.scrollHeight;
  });
});
