// ── DOM refs ──────────────────────────────────────────────────
const btnClasificar = document.getElementById("btnClasificar");
const btnLimpiar    = document.getElementById("btnLimpiar");
const textoInput    = document.getElementById("textoInput");
const charCount     = document.getElementById("charCount");
const resultado     = document.getElementById("resultado");
const btnText       = btnClasificar.querySelector(".btn-text");
const btnLoading    = btnClasificar.querySelector(".btn-loading");

// ── Category → CSS class mapping ─────────────────────────────
const categoryClass = {
    "contrato":                "cat-contrato",
    "sentencia":               "cat-sentencia",
    "demanda":                 "cat-demanda",
    "requiere_revision_humana":"cat-revision",
};

const MIN_CHARS = 50;
const MAX_CHARS = 2000;
const validationMsg = document.getElementById("validationMsg");

// ── Character counter + live validation ──────────────────────
textoInput.addEventListener("input", () => {
    const len = textoInput.value.length;
    charCount.textContent = len.toLocaleString("es-AR");

    if (len === 0) {
        clearValidation();
    } else if (len < MIN_CHARS) {
        showValidation(`Mínimo ${MIN_CHARS} caracteres (faltan ${MIN_CHARS - len})`, "error");
    } else if (len >= MAX_CHARS) {
        showValidation(`Límite de ${MAX_CHARS} caracteres alcanzado`, "warning");
    } else {
        clearValidation();
    }
});

// ── Limpiar ───────────────────────────────────────────────────
btnLimpiar.addEventListener("click", () => {
    textoInput.value = "";
    charCount.textContent = "0";
    clearValidation();
    resultado.classList.add("hidden");
    textoInput.focus();
});

// ── Clasificar ───────────────────────────────────────────────
btnClasificar.addEventListener("click", clasificarTexto);

async function clasificarTexto() {
    const texto = textoInput.value.trim();

    if (texto.length === 0) {
        showValidation("Por favor ingrese un texto jurídico.", "error");
        textoInput.focus();
        return;
    }
    if (texto.length < MIN_CHARS) {
        showValidation(`El texto debe tener al menos ${MIN_CHARS} caracteres (tiene ${texto.length}).`, "error");
        textoInput.focus();
        return;
    }
    if (texto.length > MAX_CHARS) {
        showValidation(`El texto no puede superar los ${MAX_CHARS} caracteres.`, "error");
        textoInput.focus();
        return;
    }

    clearValidation();

    setLoading(true);

    try {
        const response = await fetch("/clasificar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ texto }),
        });

        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();
        renderResultado(data);
    } catch (err) {
        console.error(err);
        alert("Error al conectar con el servidor. Verifique que la API esté activa.");
    } finally {
        setLoading(false);
    }
}

// ── Render resultado ──────────────────────────────────────────
function renderResultado(data) {
    // Categoría badge
    const catEl = document.getElementById("categoria");
    catEl.textContent = formatCategoria(data.categoria);
    catEl.className = "category-badge";
    catEl.classList.add(categoryClass[data.categoria] ?? "cat-other");

    // Confianza
    const pct = data.confianza * 100;
    document.getElementById("confianza").textContent = pct.toFixed(1) + "%";
    // Animated bar — trigger after paint
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            document.getElementById("confianzaBar").style.width = pct + "%";
            // Color: verde si >70, ámbar si >45, rojo si ≤45
            const bar = document.getElementById("confianzaBar");
            bar.style.background =
                pct >= 70 ? "linear-gradient(90deg,#16a34a,#4ade80)" :
                pct >= 45 ? "linear-gradient(90deg,#d97706,#fbbf24)" :
                            "linear-gradient(90deg,#dc2626,#f87171)";
        });
    });

    // Alerta revisión
    const revMsg = document.getElementById("revisionMsg");
    if (data.categoria === "requiere_revision_humana") {
        revMsg.classList.remove("hidden");
    } else {
        revMsg.classList.add("hidden");
    }

    // Probabilidades
    const probsDiv = document.getElementById("probabilidades");
    const entries = Object.entries(data.probabilidades).sort((a, b) => b[1] - a[1]);

    probsDiv.innerHTML = entries.map(([cat, prob]) => `
        <div class="barra-container">
            <span class="barra-label" title="${cat}">${formatCategoria(cat)}</span>
            <div class="barra">
                <div class="barra-fill" data-width="${prob * 100}"></div>
            </div>
            <span class="barra-pct">${(prob * 100).toFixed(1)}%</span>
        </div>
    `).join("");

    // Animate bars after insertion
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            probsDiv.querySelectorAll(".barra-fill").forEach(el => {
                el.style.width = el.dataset.width + "%";
            });
        });
    });

    // Show card
    resultado.classList.remove("hidden");
    resultado.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// ── Helpers ───────────────────────────────────────────────────
function setLoading(on) {
    btnClasificar.disabled = on;
    btnText.classList.toggle("hidden", on);
    btnLoading.classList.toggle("hidden", !on);
}

function showValidation(msg, type) {
    validationMsg.textContent = msg;
    validationMsg.className = `validation-msg validation-${type}`;
    textoInput.classList.toggle("input-error",   type === "error");
    textoInput.classList.toggle("input-warning", type === "warning");
}

function clearValidation() {
    validationMsg.textContent = "";
    validationMsg.className = "validation-msg hidden";
    textoInput.classList.remove("input-error", "input-warning");
}

function formatCategoria(cat) {
    return cat.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
}
