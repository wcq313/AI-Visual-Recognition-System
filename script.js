// 通用工具函数：图片转Base64（两个功能共用）
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = e => resolve(e.target.result.split(",")[1]);
        reader.onerror = err => reject(err);
        reader.readAsDataURL(file);
    });
}

// 页面加载完成后绑定事件
document.addEventListener("DOMContentLoaded", () => {
    // ---------------------- OCR文字识别 ----------------------
    const ocrBtn = document.getElementById("ocrBtn");
    const ocrFile = document.getElementById("file1");
    const ocrResult = document.getElementById("res1");

    ocrBtn.addEventListener("click", async () => {
        if (!ocrFile.files || !ocrFile.files[0]) {
            alert("请先选择图片！");
            return;
        }

        ocrBtn.disabled = true;
        ocrBtn.textContent = "识别中...";
        ocrResult.value = "正在识别，请稍候...";

        try {
            const base64 = await fileToBase64(ocrFile.files[0]);
            const res = await fetch("http://127.0.0.1:5000/api/ocr", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({img: base64})
            }).then(r => r.json());

            ocrResult.value = res.data || res.msg;
            alert(res.msg);
        } catch (err) {
            ocrResult.value = `请求失败：${err.message}`;
            alert("请求失败，请检查后端服务");
        } finally {
            ocrBtn.disabled = false;
            ocrBtn.textContent = "识别文字";
        }
    });

    // ---------------------- 通用物体识别 ----------------------
    const imageBtn = document.getElementById("imageBtn");
    const imageFile = document.getElementById("file2");
    const imageResult = document.getElementById("res2");

    imageBtn.addEventListener("click", async () => {
        if (!imageFile.files || !imageFile.files[0]) {
            alert("请先选择图片！");
            return;
        }

        imageBtn.disabled = true;
        imageBtn.textContent = "识别中...";
        imageResult.value = "正在识别，请稍候...";

        try {
            const base64 = await fileToBase64(imageFile.files[0]);
            const res = await fetch("http://127.0.0.1:5000/api/image", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({img: base64})
            }).then(r => r.json());

            imageResult.value = res.data || res.msg;
            alert(res.msg);
        } catch (err) {
            imageResult.value = `请求失败：${err.message}`;
            alert("请求失败，请检查后端服务");
        } finally {
            imageBtn.disabled = false;
            imageBtn.textContent = "识别物体";
        }
    });
});