document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("ocrForm");
    if (!form) return;

    const fileInput = document.getElementById("id_original_image");
    const uploadZone = document.getElementById("uploadZone");
    const previewWrap = document.getElementById("previewWrap");
    const preview = document.getElementById("imagePreview");
    const fileName = document.getElementById("fileName");
    const clearPreview = document.getElementById("clearPreview");
    const processButton = document.getElementById("processButton");
    const formError = document.getElementById("formError");
    const emptyResult = document.getElementById("emptyResult");
    const processingState = document.getElementById("processingState");
    const resultContent = document.getElementById("resultContent");
    const resultState = document.getElementById("resultState");
    const progressBar = document.getElementById("progressBar");
    const processingLabel = document.getElementById("processingLabel");

    let objectUrl = null;
    let progressTimer = null;

    function showError(message) {
        formError.textContent = message;
        formError.hidden = false;
    }

    function resetError() {
        formError.textContent = "";
        formError.hidden = true;
    }

    function setFile(file) {
        resetError();
        if (!file) return;
        if (!file.type.startsWith("image/")) {
            showError("لطفاً یک فایل تصویری انتخاب کن.");
            return;
        }
        if (file.size > 5 * 1024 * 1024) {
            showError("حجم تصویر باید کمتر از ۵ مگابایت باشد.");
            return;
        }
        const transfer = new DataTransfer();
        transfer.items.add(file);
        fileInput.files = transfer.files;
        if (objectUrl) URL.revokeObjectURL(objectUrl);
        objectUrl = URL.createObjectURL(file);
        preview.src = objectUrl;
        fileName.textContent = `${file.name} · ${(file.size / 1024).toFixed(0)} KB`;
        previewWrap.hidden = false;
        uploadZone.hidden = true;
        processButton.disabled = false;
    }

    fileInput.addEventListener("change", () => setFile(fileInput.files[0]));
    ["dragenter", "dragover"].forEach((eventName) => uploadZone.addEventListener(eventName, (event) => {
        event.preventDefault();
        uploadZone.classList.add("dragging");
    }));
    ["dragleave", "drop"].forEach((eventName) => uploadZone.addEventListener(eventName, (event) => {
        event.preventDefault();
        uploadZone.classList.remove("dragging");
    }));
    uploadZone.addEventListener("drop", (event) => setFile(event.dataTransfer.files[0]));

    clearPreview.addEventListener("click", () => {
        fileInput.value = "";
        if (objectUrl) URL.revokeObjectURL(objectUrl);
        objectUrl = null;
        previewWrap.hidden = true;
        uploadZone.hidden = false;
        processButton.disabled = true;
        resetError();
    });

    function setProcessing(isProcessing) {
        emptyResult.hidden = isProcessing;
        resultContent.hidden = true;
        processingState.hidden = !isProcessing;
        processButton.disabled = isProcessing;
        resultState.className = isProcessing ? "result-state processing" : "result-state";
        resultState.innerHTML = isProcessing ? '<span class="state-dot"></span> در حال پردازش' : '<span class="state-dot"></span> در انتظار ورودی';
    }

    function renderResult(data) {
        if (progressTimer) window.clearInterval(progressTimer);
        progressBar.style.width = "100%";
        processingState.hidden = true;
        resultContent.hidden = false;
        resultState.className = "result-state success";
        resultState.innerHTML = '<span class="state-dot"></span> پردازش کامل شد';
        document.getElementById("recognizedText").textContent = data.text;
        document.getElementById("confidenceValue").textContent = `${data.confidence.toFixed(1)}٪`;
        document.getElementById("timeValue").textContent = `${data.processing_time.toFixed(2)}s`;
        document.getElementById("modelValue").textContent = data.model;
        document.getElementById("resultDetailLink").href = data.detail_url;
        document.getElementById("analysisLink").href = data.analysis_url;
        document.getElementById("keywordList").innerHTML = data.keywords.map((keyword) => `<span class="keyword">${keyword}</span>`).join("");
        processButton.disabled = false;
        window.showToast?.("نتیجه با موفقیت ذخیره شد.");
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        resetError();
        if (!fileInput.files[0]) {
            showError("ابتدا یک تصویر انتخاب کن.");
            return;
        }
        setProcessing(true);
        progressBar.style.width = "8%";
        const labels = ["پیش‌پردازش تصویر...", "استخراج ویژگی‌های بصری...", "تشخیص توالی متن فارسی..."];
        let labelIndex = 0;
        progressTimer = window.setInterval(() => {
            labelIndex = Math.min(labelIndex + 1, labels.length - 1);
            processingLabel.textContent = labels[labelIndex];
            progressBar.style.width = `${30 + labelIndex * 28}%`;
        }, 430);

        try {
            const csrf = form.querySelector("[name=csrfmiddlewaretoken]").value;
            const response = await fetch(window.FARSAKHAN.ocrUrl, {
                method: "POST",
                body: new FormData(form),
                headers: { "X-CSRFToken": csrf, "X-Requested-With": "XMLHttpRequest" }
            });
            const data = await response.json();
            if (!response.ok || !data.success) {
                const messages = Object.values(data.errors || {}).flat();
                throw new Error(messages[0] || "پردازش تصویر انجام نشد.");
            }
            renderResult(data);
        } catch (error) {
            if (progressTimer) window.clearInterval(progressTimer);
            setProcessing(false);
            showError(error.message || "خطایی در ارتباط با سرور رخ داد.");
        }
    });

    document.getElementById("copyResult")?.addEventListener("click", async () => {
        const text = document.getElementById("recognizedText")?.textContent || "";
        if (!text) return;
        try {
            await navigator.clipboard.writeText(text);
            window.showToast?.("متن در کلیپ‌بورد کپی شد.");
        } catch {
            window.showToast?.("کپی خودکار در این مرورگر در دسترس نیست.");
        }
    });
});
