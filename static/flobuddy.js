let entries = [];
function showEntryForm() {
    document.getElementById('addForm').style.display = 'block';
    document.getElementById('entriesList').style.display = 'none';
    document.getElementById('showEntryBtn').classList.add('btn-active');
    document.getElementById('showListBtn').classList.remove('btn-active');
}
function showEntries() {
    document.getElementById('addForm').style.display = 'none';
    document.getElementById('entriesList').style.display = 'block';
    document.getElementById('showEntryBtn').classList.remove('btn-active');
    document.getElementById('showListBtn').classList.add('btn-active');
}
function addEntry(event) {
    event.preventDefault();
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const flowIntensity = document.getElementById('flowIntensity').value;
    const notes = document.getElementById('notes').value;
    const entry = {
        id: Date.now(),
        startDate,
        endDate,
        flowIntensity,
        notes
    };
    entries.unshift(entry);
    saveToLocalStorage();
    renderEntries();
    event.target.reset();
    showEntries();
}
function deleteEntry(id) {
    if (confirm('Delete this entry?')) {
        entries = entries.filter(e => e.id !== id);
        saveToLocalStorage();
        renderEntries();
    }
}
function renderEntries() {
    const container = document.getElementById('entriesList');
    if (entries.length === 0) {
        container.innerHTML = `<div class="empty-state"><p>No entries yet. Start tracking your periods!</p></div>`;
        return;
    }
    container.innerHTML = entries.map(entry => {
        const start = new Date(entry.startDate).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
        const end = entry.endDate ? " - " + new Date(entry.endDate).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }) : "";
        return `
        <div class="entry-card">
            <div class="entry-info">
                <h3>${start}${end}</h3>
                <p><strong>Flow:</strong> ${entry.flowIntensity.charAt(0).toUpperCase() + entry.flowIntensity.slice(1)}</p>
                ${entry.notes ? `<p><strong>Notes:</strong> ${entry.notes}</p>` : ""}
            </div>
            <button class="btn-primary" style="background:#ff7675;width:42px;height:42px;padding:7px 0;border-radius:12px;font-size:20px;margin-left:18px;height:fit-content;" onclick="deleteEntry(${entry.id})" title="Delete entry">🗑️</button>
        </div>
        `;
    }).join('');
}
function saveToLocalStorage() {
    localStorage.setItem('floBuddyEntries', JSON.stringify(entries));
}
function loadFromLocalStorage() {
    const saved = localStorage.getItem('floBuddyEntries');
    if (saved) entries = JSON.parse(saved);
    renderEntries();
    showEntries();
}
window.addEventListener('DOMContentLoaded', loadFromLocalStorage);
