async function getDialogues() {
  const age_group = document.getElementById("age_group").value;
  const gender = document.getElementById("gender").value;
  const emotion = document.getElementById("emotion").value;

  const response = await fetch("http://localhost:8000/get_dialogues", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ age_group, gender, emotion }),
  });
  const data = await response.json();
  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = data
    .map(
      (d) => `
    <div>
      <strong>${d.person}</strong> (${d.emotion})<br>
      사용자: ${d.user}<br>
      챗봇: ${d.bot}
    </div><hr>
  `
    )
    .join("");
}
