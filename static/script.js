document.getElementById('solve-btn').addEventListener('click', async () => {
    const input = document.getElementById('coefficients').value;
    const coeffs = input.trim().split(/\s+/).map(Number);

    if (coeffs.some(isNaN) || coeffs.length === 0) {
        alert("Please enter valid space-separated numbers.");
        return;
    }

    // UI State
    const loader = document.getElementById('loader');
    const results = document.getElementById('results-container');
    loader.classList.remove('hidden');
    results.classList.add('hidden');

    try {
        // 1. Solve Roots
        const solveRes = await fetch('/api/solve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ coefficients: coeffs })
        });
        const solveData = await solveRes.json();

        // 2. Get Plot
        const plotRes = await fetch('/api/plot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ coefficients: coeffs })
        });
        const plotData = await plotRes.json();

        // 3. Get Explanation
        let explainData = {};
        if (solveData.degree <= 2) {
            const explainRes = await fetch('/api/explain', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ coefficients: coeffs })
            });
            explainData = await explainRes.json();
        }

        updateUI(solveData, plotData, explainData);
    } catch (err) {
        console.error(err);
        alert("An error occurred while communicating with the API.");
    } finally {
        loader.classList.add('hidden');
    }
});

function updateUI(solve, plot, explain) {
    const results = document.getElementById('results-container');
    results.classList.remove('hidden');

    // Update Metadata
    document.getElementById('degree-tag').textContent = `Degree: ${solve.degree}`;
    document.getElementById('type-tag').textContent = `Type: ${solve.type}`;

    // Update Roots
    const rootsList = document.getElementById('roots-list');
    rootsList.innerHTML = solve.roots.map((r, i) => {
        const val = r.imag !== 0 
            ? `${r.real.toFixed(4)} ${r.imag > 0 ? '+' : '-'} ${Math.abs(r.imag).toFixed(4)}i`
            : r.real.toFixed(4);
        return `<div class="root-item"><span>Root ${i+1}:</span> <strong>${val}</strong></div>`;
    }).join('');

    // Update Graph
    if (plot.plot) {
        document.getElementById('polynomial-graph').src = `data:image/png;base64,${plot.plot}`;
    }

    // Update Explanation
    const expCard = document.getElementById('explanation-card');
    if (explain.steps && explain.steps.length > 0 && solve.degree <= 2) {
        expCard.classList.remove('hidden');
        document.getElementById('steps-content').innerHTML = explain.steps.map(s => `<div class="step-row">${s}</div>`).join('');
    } else {
        expCard.classList.add('hidden');
    }
}
