async function startScan() {
    const url = document.getElementById('urlInput').value;
    const resultElement = document.getElementById('result');
    resultElement.textContent = '🔍 Scanning...';

    try {
        const response = await fetch('/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });

        const data = await response.json();
        if (data.error) {
            resultElement.textContent = `❌ Error: ${data.error}`;
        } else {
            resultElement.textContent = `✅ Result:\n${data.result}`;
        }
    } catch (error) {
        resultElement.textContent = `⚠️ Failed to scan: ${error.message}`;
    }
}
