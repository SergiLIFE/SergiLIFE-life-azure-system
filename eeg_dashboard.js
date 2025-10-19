(function () {
    function $(id) { return document.getElementById(id); }

    window.adjustComplexity = function () {
        console.log('[UI] Auto-Adjust Complexity clicked');
        alert('Complexity adjusted based on recent engagement.');
    };

    window.insertBreak = function () {
        console.log('[UI] Suggest Break clicked');
        alert('Break suggested to restore attention.');
    };

    // Simple drawing function for EEG-like data
    function drawEEG(values) {
        var canvas = $('eeg-viz');
        if (!canvas) return;
        var ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.beginPath();
        var len = values.length;
        for (var i = 0; i < len; i++) {
            var x = (i / len) * canvas.width;
            var y = canvas.height / 2 + values[i] * (canvas.height / 2 - 10);
            if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.strokeStyle = '#2a6';
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    // Demo updater (random data)
    function updateDemo() {
        var data = [];
        for (var i = 0; i < 128; i++) { data.push((Math.random() - 0.5) * 0.5); }
        drawEEG(data);
        var engagement = Math.max(0, Math.min(1, 0.6 + (Math.random() - 0.5) * 0.2));
        var el = $('engagement-value'); if (el) el.textContent = engagement.toFixed(2);
    }

    // Lightweight personalization updater from metrics endpoint
    function updatePersonalization() {
        try {
            fetch('/api/dashboard/metrics', { cache: 'no-store' })
                .then(function (r) { return r.json(); })
                .then(function (j) {
                    if (!j || j.status !== 'success') return;
                    var t = j.trait_summary || {};
                    var text = $('personalization-text');
                    if (!text) return;
                    var style = t.cognitive_style ? (t.cognitive_style.charAt(0).toUpperCase() + t.cognitive_style.slice(1)) : 'Adaptive';
                    var cur = (typeof t.curiosity === 'number') ? t.curiosity.toFixed(2) : '—';
                    var res = (typeof t.resilience === 'number') ? t.resilience.toFixed(2) : '—';
                    text.textContent = 'Personalized: ' + style + ' • Curiosity ' + cur + ' • Resilience ' + res;
                })
                .catch(function () { /* silent */ });
        } catch (e) { /* silent */ }
    }

    setInterval(updateDemo, 1000);
    setInterval(updatePersonalization, 4000);
    updatePersonalization();
})();
