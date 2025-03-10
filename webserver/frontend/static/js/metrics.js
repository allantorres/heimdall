document.addEventListener('DOMContentLoaded', function() {
    // Chart.js global configuration
    Chart.defaults.font.family = "'Inter', 'Helvetica', 'Arial', sans-serif";
    Chart.defaults.color = '#6B7280';
    Chart.defaults.scale.grid.color = '#E5E7EB';
    
    // Common chart options
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: true,
        interaction: {
            mode: 'index',
            intersect: false,
        },
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    usePointStyle: true,
                    padding: 20
                }
            },
            tooltip: {
                backgroundColor: 'rgba(17, 24, 39, 0.8)',
                padding: 12,
                titleFont: {
                    size: 14,
                    weight: 'bold'
                },
                bodyFont: {
                    size: 13
                },
                cornerRadius: 4,
                displayColors: true
            }
        }
    };
    
    // Time range selector
    const timeRangeSelector = document.getElementById('timeRangeSelector');
    
    // Function to filter data by selected time range
    function filterDataByDays(data, days) {
        if (!data || !data.length) return data;
        
        const cutoffDate = new Date();
        cutoffDate.setDate(cutoffDate.getDate() - days);
        
        return data.filter(item => new Date(item.date) >= cutoffDate);
    }
    
    // Executions Over Time Chart
    const executionsCtx = document.getElementById('executionsChart').getContext('2d');
    const executionsChart = new Chart(executionsCtx, {
        type: 'line',
        data: {
            labels: metricsData.executionDates,
            datasets: [{
                label: 'Executions',
                data: metricsData.executionCounts,
                borderColor: 'rgb(59, 130, 246)',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 2,
                tension: 0.2,
                fill: true,
                pointBackgroundColor: 'rgb(59, 130, 246)',
                pointRadius: 3,
                pointHoverRadius: 5
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day',
                        tooltipFormat: 'MMM d, yyyy',
                        displayFormats: {
                            day: 'MMM d'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Executions'
                    },
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
    
    // Daily Cost Trend Chart
    const costCtx = document.getElementById('costChart').getContext('2d');
    const costChart = new Chart(costCtx, {
        type: 'line',
        data: {
            labels: metricsData.executionDates,
            datasets: [{
                label: 'Daily Cost ($)',
                data: metricsData.dailyCosts,
                borderColor: 'rgb(16, 185, 129)',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                borderWidth: 2,
                tension: 0.2,
                fill: true,
                pointBackgroundColor: 'rgb(16, 185, 129)',
                pointRadius: 3,
                pointHoverRadius: 5
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day',
                        tooltipFormat: 'MMM d, yyyy',
                        displayFormats: {
                            day: 'MMM d'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Cost ($)'
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            }
        }
    });
    
    // Response Time Distribution Chart
    const responseTimeCtx = document.getElementById('responseTimeChart').getContext('2d');
    const responseTimeChart = new Chart(responseTimeCtx, {
        type: 'bar',
        data: {
            labels: ['0-1s', '1-2s', '2-3s', '3-4s', '4-5s', '5s+'],
            datasets: [{
                label: 'Response Time Distribution',
                data: calculateResponseTimeBuckets(metricsData.responseTimes),
                backgroundColor: 'rgba(124, 58, 237, 0.7)',
                borderColor: 'rgb(124, 58, 237)',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Executions'
                    },
                    ticks: {
                        precision: 0
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Response Time'
                    }
                }
            }
        }
    });
    
    // Token Usage Trend Chart
    const tokenUsageCtx = document.getElementById('tokenUsageChart').getContext('2d');
    const tokenUsageChart = new Chart(tokenUsageCtx, {
        type: 'line',
        data: {
            labels: metricsData.executionDates,
            datasets: [{
                label: 'Token Usage',
                data: metricsData.tokenUsage,
                borderColor: 'rgb(236, 72, 153)',
                backgroundColor: 'rgba(236, 72, 153, 0.1)',
                borderWidth: 2,
                tension: 0.2,
                fill: true,
                pointBackgroundColor: 'rgb(236, 72, 153)',
                pointRadius: 3,
                pointHoverRadius: 5
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day',
                        tooltipFormat: 'MMM d, yyyy',
                        displayFormats: {
                            day: 'MMM d'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Tokens Used'
                    }
                }
            }
        }
    });

    // Cost Breakdown by Agent Chart
    const costBreakdownCtx = document.getElementById('costBreakdownChart').getContext('2d');
    const costBreakdownChart = new Chart(costBreakdownCtx, {
        type: 'doughnut',
        data: {
            labels: metricsData.agentNames,
            datasets: [{
                data: metricsData.agentCosts,
                backgroundColor: [
                    'rgba(59, 130, 246, 0.7)',
                    'rgba(16, 185, 129, 0.7)',
                    'rgba(124, 58, 237, 0.7)',
                    'rgba(236, 72, 153, 0.7)',
                    'rgba(245, 158, 11, 0.7)'
                ],
                borderColor: [
                    'rgb(59, 130, 246)',
                    'rgb(16, 185, 129)',
                    'rgb(124, 58, 237)',
                    'rgb(236, 72, 153)',
                    'rgb(245, 158, 11)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            ...commonOptions,
            cutout: '60%',
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        label: function(context) {
                            const value = context.raw;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${context.label}: $${value.toFixed(2)} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });

    // Helper function to calculate response time distribution
    function calculateResponseTimeBuckets(times) {
        const buckets = [0, 0, 0, 0, 0, 0]; // 0-1s, 1-2s, 2-3s, 3-4s, 4-5s, 5s+
        
        times.forEach(time => {
            if (time < 1) buckets[0]++;
            else if (time < 2) buckets[1]++;
            else if (time < 3) buckets[2]++;
            else if (time < 4) buckets[3]++;
            else if (time < 5) buckets[4]++;
            else buckets[5]++;
        });
        
        return buckets;
    }

    // Export to CSV functionality
    document.getElementById('exportCSV').addEventListener('click', function() {
        const rows = [
            ['Date', 'Agent', 'Status', 'Response Time (s)', 'Tokens Used', 'Cost ($)']
        ];

        // Add data rows
        metricsData.executionDates.forEach((date, i) => {
            rows.push([
                date,
                metricsData.agentNames[i],
                metricsData.statuses[i],
                metricsData.responseTimes[i].toFixed(2),
                metricsData.tokenUsage[i],
                metricsData.dailyCosts[i].toFixed(4)
            ]);
        });

        // Create CSV content
        const csvContent = rows.map(row => row.join(',')).join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.setAttribute('href', url);
        a.setAttribute('download', 'agent_metrics.csv');
        a.click();
    });

    // Time range selector event handler
    timeRangeSelector.addEventListener('change', function() {
        const days = parseInt(this.value);
        updateChartsTimeRange(days);
    });

    function updateChartsTimeRange(days) {
        const filteredData = {
            executionDates: filterDataByDays(metricsData.executionDates, days),
            executionCounts: filterDataByDays(metricsData.executionCounts, days),
            dailyCosts: filterDataByDays(metricsData.dailyCosts, days),
            tokenUsage: filterDataByDays(metricsData.tokenUsage, days),
            responseTimes: filterDataByDays(metricsData.responseTimes, days)
        };

        // Update each chart with filtered data
        updateChart(executionsChart, filteredData.executionDates, filteredData.executionCounts);
        updateChart(costChart, filteredData.executionDates, filteredData.dailyCosts);
        updateChart(tokenUsageChart, filteredData.executionDates, filteredData.tokenUsage);
        updateResponseTimeChart(responseTimeChart, filteredData.responseTimes);
    }

    function updateChart(chart, labels, data) {
        chart.data.labels = labels;
        chart.data.datasets[0].data = data;
        chart.update();
    }

    function updateResponseTimeChart(chart, times) {
        chart.data.datasets[0].data = calculateResponseTimeBuckets(times);
        chart.update();
    }
});