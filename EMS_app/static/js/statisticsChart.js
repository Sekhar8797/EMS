document.addEventListener('DOMContentLoaded', function () {
    // Retrieve data for events by month chart
    const monthsData = JSON.parse(document.getElementById('months-data').textContent);
    const countsData = JSON.parse(document.getElementById('counts-data').textContent);

    // Render events by month chart
    const ctxEvents = document.getElementById('eventsChart').getContext('2d');
    const eventsChart = new Chart(ctxEvents, {
        type: 'bar',
        data: {
            labels: monthsData,
            datasets: [{
                label: 'Events by Month',
                data: countsData,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
