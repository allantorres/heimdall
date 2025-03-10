document.addEventListener('DOMContentLoaded', function() {
    // Executions Over Time Chart
    const executionsCtx = document.getElementById('executionsChart').getContext('2d');
    new Chart(executionsCtx, {
        type: 'line',
        data: {
            labels: executionDates,
            datasets: [{
                label: 'Executions',
                data: executionCounts,
                borderColor: 'rgb(59, 130, 246)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });

    // Response Time Distribution Chart
    const responseTimeCtx = document.getElementById('responseTimeChart').getContext('2d');
    new Chart(responseTimeCtx, {
        type: 'bar',
        data: {
            labels: responseTimeBuckets,
            datasets: [{
                label: 'Response Time Distribution',
                data: responseTimeCounts,
                backgroundColor: 'rgba(59, 130, 246, 0.5)',
                borderColor: 'rgb(59, 130, 246)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
});