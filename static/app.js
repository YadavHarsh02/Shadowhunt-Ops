async function ping() {
  const res = await fetch("/api/health");
  const j = await res.json();
  document.getElementById("health-out").textContent = JSON.stringify(j, null, 2);
}

async function runModule(name, payload, outId) {
  const res = await fetch(`/api/attack/${name}`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  });
  const j = await res.json();
  document.getElementById(outId).textContent = JSON.stringify(j, null, 2);
}

async function getLogs() {
  const res = await fetch("/api/logs");
  const j = await res.json();
  document.getElementById("logs-out").textContent = JSON.stringify(j, null, 2);
}

document.addEventListener("DOMContentLoaded", () => {
  // Health check
  const h = document.getElementById("btn-health");
  if (h) h.addEventListener("click", ping);

  // Brute-Force
  const bfBtn = document.getElementById("btn-bf");
  if (bfBtn) bfBtn.addEventListener("click", () => {
    const target = document.getElementById("bf-target").value || "http://127.0.0.1:5000/login";
    const username = document.getElementById("bf-username").value || "admin";
    const wordlistInput = document.getElementById("bf-wordlist").value || "1234,password,admin123";
    const wordlist = wordlistInput.split(",").map(p => p.trim()).filter(p => p.length);

    runModule("brute-force", { target, username, wordlist }, "bf-out");
  });

  // SQL Injection
  const sqliBtn = document.getElementById("btn-sqli");
  if (sqliBtn) sqliBtn.addEventListener("click", () => {
    const url = document.getElementById("sqli-url").value || "http://127.0.0.1/item?id=1";
    runModule("sql-injection", { url }, "sqli-out");
  });

  // NTLM Extractor
  const ntlmBtn = document.getElementById("btn-ntlm");
  if (ntlmBtn) ntlmBtn.addEventListener("click", () => {
    const sample = document.getElementById("ntlm-sample").value || "dummy.ntlm";
    runModule("ntlm-extractor", { sample }, "ntlm-out");
  });

  // Recon Scanner
  const reconBtn = document.getElementById("btn-recon");
  if (reconBtn) reconBtn.addEventListener("click", () => {
    const host = document.getElementById("recon-host").value || "127.0.0.1";
    const portsInput = document.getElementById("recon-ports").value || "80,443";
    const ports = portsInput.split(",").map(p => parseInt(p.trim())).filter(p => !isNaN(p));
    runModule("recon-scanner", { host, ports }, "recon-out");
  });

  // Logs
  const logsBtn = document.getElementById("btn-logs");
  if (logsBtn) logsBtn.addEventListener("click", getLogs);
});

o
