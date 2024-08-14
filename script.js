document.getElementById('clickButton').addEventListener('click', function() {
    fetch('/click', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('balance').textContent = data.balance;
    });
});

// Инициализация баланса при загрузке страницы
window.onload = function() {
    fetch('/balance')
    .then(response => response.json())
    .then(data => {
        document.getElementById('balance').textContent = data.balance;
    });
};
