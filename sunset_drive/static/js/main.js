// Sunset Drive - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize variables
    const chartColors = {
        scenario1: {
            borderColor: '#39FF14', // Neon green
            backgroundColor: 'rgba(57, 255, 20, 0.1)',
            pointHoverBackgroundColor: '#39FF14',
            pointHoverBorderColor: '#FFFFFF'
        },
        scenario2: {
            borderColor: '#0099FF', // Blue
            backgroundColor: 'rgba(0, 153, 255, 0.1)',
            pointHoverBackgroundColor: '#0099FF',
            pointHoverBorderColor: '#FFFFFF'
        },
        gridColor: '#CCCCCC'
    };

    // Store charts and data
    const charts = {
        scenario1: null,
        scenario2: null,
        comparison: null
    };

    const scenarioData = {
        scenario1: null,
        scenario2: null
    };

    // Format currency
    const formatCurrency = (value) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            maximumFractionDigits: 0
        }).format(value);
    };

    // Initialize chart
    const initChart = (chartId, scenario) => {
        const ctx = document.getElementById(chartId).getContext('2d');

        let colorSet = chartColors.scenario1;
        if (scenario === 2) {
            colorSet = chartColors.scenario2;
        }

        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: `Scenario ${scenario} Retirement Savings`,
                    data: [],
                    borderColor: colorSet.borderColor,
                    backgroundColor: colorSet.backgroundColor,
                    borderWidth: 3,
                    pointRadius: 2,
                    pointHoverRadius: 6,
                    pointHoverBackgroundColor: colorSet.pointHoverBackgroundColor,
                    pointHoverBorderColor: colorSet.pointHoverBorderColor,
                    pointHoverBorderWidth: 2,
                    tension: 0.2 // Slightly curved lines
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            boxWidth: 15,
                            usePointStyle: true,
                            font: {
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(51, 51, 51, 0.8)',
                        titleFont: {
                            size: 13
                        },
                        bodyFont: {
                            size: 12
                        },
                        padding: 10,
                        cornerRadius: 5,
                        displayColors: false,
                        callbacks: {
                            title: function(tooltipItems) {
                                return `Age: ${tooltipItems[0].label}`;
                            },
                            label: function(context) {
                                return `Savings: ${formatCurrency(context.raw)}`;
                            }
                        }
                    },
                    zoom: {
                        pan: {
                            enabled: true,
                            mode: 'x'
                        },
                        zoom: {
                            wheel: {
                                enabled: true
                            },
                            pinch: {
                                enabled: true
                            },
                            mode: 'x'
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Age',
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        },
                        grid: {
                            color: chartColors.gridColor,
                            borderColor: chartColors.gridColor,
                            tickColor: chartColors.gridColor
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Savings Amount ($)',
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        },
                        grid: {
                            color: chartColors.gridColor,
                            borderColor: chartColors.gridColor,
                            tickColor: chartColors.gridColor
                        },
                        ticks: {
                            callback: function(value) {
                                return formatCurrency(value);
                            }
                        }
                    }
                },
                animations: {
                    tension: {
                        duration: 1000,
                        easing: 'linear'
                    }
                }
            }
        });
    };

    // Initialize the comparison chart
    const initComparisonChart = () => {
        const ctx = document.getElementById('comparisonChart').getContext('2d');

        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Scenario 1',
                        data: [],
                        borderColor: chartColors.scenario1.borderColor,
                        backgroundColor: chartColors.scenario1.backgroundColor,
                        borderWidth: 3,
                        pointRadius: 2,
                        pointHoverRadius: 6,
                        pointHoverBackgroundColor: chartColors.scenario1.pointHoverBackgroundColor,
                        pointHoverBorderColor: chartColors.scenario1.pointHoverBorderColor,
                        tension: 0.2
                    },
                    {
                        label: 'Scenario 2',
                        data: [],
                        borderColor: chartColors.scenario2.borderColor,
                        backgroundColor: chartColors.scenario2.backgroundColor,
                        borderWidth: 3,
                        pointRadius: 2,
                        pointHoverRadius: 6,
                        pointHoverBackgroundColor: chartColors.scenario2.pointHoverBackgroundColor,
                        pointHoverBorderColor: chartColors.scenario2.pointHoverBorderColor,
                        tension: 0.2
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        backgroundColor: 'rgba(51, 51, 51, 0.8)',
                        callbacks: {
                            title: function(tooltipItems) {
                                return `Age: ${tooltipItems[0].label}`;
                            },
                            label: function(context) {
                                const label = context.dataset.label || '';
                                return `${label}: ${formatCurrency(context.raw)}`;
                            }
                        }
                    },
                    zoom: {
                        pan: {
                            enabled: true,
                            mode: 'x'
                        },
                        zoom: {
                            wheel: {
                                enabled: true
                            },
                            pinch: {
                                enabled: true
                            },
                            mode: 'x'
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Age',
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Savings Amount ($)',
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        },
                        ticks: {
                            callback: function(value) {
                                return formatCurrency(value);
                            }
                        }
                    }
                }
            }
        });
    };

    // Update chart with new data
    const updateChart = (chart, chartData, scenario) => {
        if (chart === null) {
            if (scenario === 'comparison') {
                charts.comparison = initComparisonChart();
                chart = charts.comparison;
            } else {
                charts[`scenario${scenario}`] = initChart(`savingsChart-${scenario}`, scenario);
                chart = charts[`scenario${scenario}`];
            }
        }

        chart.data.labels = chartData.labels;

        if (scenario === 'comparison') {
            // For comparison chart, we update both datasets
            if (scenarioData.scenario1) {
                chart.data.datasets[0].data = scenarioData.scenario1.chartData.datasets[0].data;
            }
            if (scenarioData.scenario2) {
                chart.data.datasets[1].data = scenarioData.scenario2.chartData.datasets[0].data;
            }
        } else {
            // For individual scenario charts
            chart.data.datasets[0].data = chartData.datasets[0].data;

            // Add vertical line at retirement age
            const retirementAge = parseInt(document.getElementById(`retirementAge-${scenario}`).value);
            const retirementIndex = chartData.labels.indexOf(retirementAge);

            if (retirementIndex !== -1) {
                chart.options.plugins.annotation = {
                    annotations: {
                        retirementLine: {
                            type: 'line',
                            xMin: retirementIndex,
                            xMax: retirementIndex,
                            borderColor: 'rgba(255, 99, 132, 0.7)',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                content: 'Retirement',
                                enabled: true,
                                position: 'top'
                            }
                        }
                    }
                };
            }
        }

        chart.update();
    };

    // Update analytics section
    const updateAnalytics = (analytics, scenario) => {
        // Update scenario tab analytics
        document.getElementById(`maxSavings-${scenario}`).textContent = formatCurrency(analytics.maxSavings);
        document.getElementById(`maxSavingsAge-${scenario}`).textContent = analytics.maxSavingsAge;
        document.getElementById(`ssIncome-${scenario}`).textContent = formatCurrency(analytics.ssIncome);

        if (analytics.retirementFundDepletionAge) {
            document.getElementById(`fundDepletionAge-${scenario}`).textContent = analytics.retirementFundDepletionAge;
        } else {
            document.getElementById(`fundDepletionAge-${scenario}`).textContent = 'N/A';
        }

        // Update comparison tab analytics
        document.getElementById(`compare-maxSavings-${scenario}`).textContent = formatCurrency(analytics.maxSavings);
        document.getElementById(`compare-maxSavingsAge-${scenario}`).textContent = analytics.maxSavingsAge;
        document.getElementById(`compare-ssIncome-${scenario}`).textContent = formatCurrency(analytics.ssIncome);

        if (analytics.retirementFundDepletionAge) {
            document.getElementById(`compare-fundDepletionAge-${scenario}`).textContent = analytics.retirementFundDepletionAge;
        } else {
            document.getElementById(`compare-fundDepletionAge-${scenario}`).textContent = 'N/A';
        }
    };

    // Collect form data
    const collectFormData = (scenario) => {
        return {
            currentAge: document.getElementById(`currentAge-${scenario}`).value,
            retirementAge: document.getElementById(`retirementAge-${scenario}`).value,
            lifeExpectancy: document.getElementById(`lifeExpectancy-${scenario}`).value,
            currentIncome: document.getElementById(`currentIncome-${scenario}`).value,
            incomeGrowthRate: document.getElementById(`incomeGrowthRate-${scenario}`).value,
            currentSavings: document.getElementById(`currentSavings-${scenario}`).value,
            savingsRate: document.getElementById(`savingsRate-${scenario}`).value,
            investmentReturn: document.getElementById(`investmentReturn-${scenario}`).value,
            retirementSpending: document.getElementById(`retirementSpending-${scenario}`).value,
            ssBenefit: document.getElementById(`ssBenefit-${scenario}`).value,
            ssStartAge: document.getElementById(`ssStartAge-${scenario}`).value
        };
    };

    // Calculate a single scenario
    const calculateScenario = (scenario) => {
        const formData = collectFormData(scenario);

        // Send data to server
        fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            // Store scenario data for comparison
            scenarioData[`scenario${scenario}`] = data;

            // Update chart and analytics
            updateChart(charts[`scenario${scenario}`], data.chartData, scenario);
            updateAnalytics(data.analytics, scenario);

            // Update comparison chart if both scenarios have data
            if (scenario === 2 && scenarioData.scenario1) {
                updateComparisonChart();
            } else if (scenario === 1 && scenarioData.scenario2) {
                updateComparisonChart();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while calculating your retirement plan. Please try again.');
        });
    };

    // Update the comparison chart
    const updateComparisonChart = () => {
        if (!scenarioData.scenario1 || !scenarioData.scenario2) {
            return;
        }

        // Merge labels from both scenarios (take the longer range)
        const allLabels = new Set([
            ...scenarioData.scenario1.chartData.labels,
            ...scenarioData.scenario2.chartData.labels
        ]);
        const sortedLabels = Array.from(allLabels).sort((a, b) => a - b);

        // Create a combined data structure
        const comparisonData = {
            labels: sortedLabels,
            datasets: [
                {
                    label: 'Scenario 1',
                    data: []
                },
                {
                    label: 'Scenario 2',
                    data: []
                }
            ]
        };

        // Fill in the data for each scenario
        sortedLabels.forEach((age) => {
            // Scenario 1
            const index1 = scenarioData.scenario1.chartData.labels.indexOf(age);
            if (index1 !== -1) {
                comparisonData.datasets[0].data.push(scenarioData.scenario1.chartData.datasets[0].data[index1]);
            } else {
                comparisonData.datasets[0].data.push(null);
            }

            // Scenario 2
            const index2 = scenarioData.scenario2.chartData.labels.indexOf(age);
            if (index2 !== -1) {
                comparisonData.datasets[1].data.push(scenarioData.scenario2.chartData.datasets[0].data[index2]);
            } else {
                comparisonData.datasets[1].data.push(null);
            }
        });

        updateChart(charts.comparison, comparisonData, 'comparison');
    };

    // Validate relationships between form fields
    const validateFormRelationships = (scenario) => {
        const currentAge = parseInt(document.getElementById(`currentAge-${scenario}`).value);
        const retirementAge = parseInt(document.getElementById(`retirementAge-${scenario}`).value);
        const lifeExpectancy = parseInt(document.getElementById(`lifeExpectancy-${scenario}`).value);
        const ssStartAge = parseInt(document.getElementById(`ssStartAge-${scenario}`).value);

        // Ensure retirement age is greater than current age
        if (retirementAge <= currentAge) {
            document.getElementById(`retirementAge-${scenario}`).value = currentAge + 1;
            alert('Retirement age must be greater than current age.');
        }

        // Ensure life expectancy is greater than retirement age
        if (lifeExpectancy <= retirementAge) {
            document.getElementById(`lifeExpectancy-${scenario}`).value = retirementAge + 1;
            alert('Life expectancy must be greater than retirement age.');
        }

        // Ensure SS start age is between 62 and 70
        if (ssStartAge < 62) {
            document.getElementById(`ssStartAge-${scenario}`).value = 62;
            alert('Social Security start age cannot be earlier than 62.');
        } else if (ssStartAge > 70) {
            document.getElementById(`ssStartAge-${scenario}`).value = 70;
            alert('Social Security start age cannot be later than 70.');
        }
    };

    // Initialize event listeners

    // Form submissions
    document.querySelectorAll('.retirement-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const scenario = this.getAttribute('data-scenario');
            calculateScenario(scenario);
        });
    });

    // Reset zoom buttons
    document.querySelectorAll('.reset-zoom').forEach(button => {
        button.addEventListener('click', function() {
            const id = this.id;
            if (id === 'reset-zoom-compare' && charts.comparison) {
                charts.comparison.resetZoom();
            } else if (id === 'reset-zoom-1' && charts.scenario1) {
                charts.scenario1.resetZoom();
            } else if (id === 'reset-zoom-2' && charts.scenario2) {
                charts.scenario2.resetZoom();
            }
        });
    });

    // Tab change event to update comparison chart
    document.querySelectorAll('button[data-bs-toggle="pill"]').forEach(tab => {
        tab.addEventListener('shown.bs.tab', function (e) {
            if (e.target.id === 'compare-tab') {
                // Make sure both scenarios have data before updating comparison
                if (scenarioData.scenario1 && scenarioData.scenario2) {
                    // Refresh or initialize comparison chart
                    if (charts.comparison) {
                        updateComparisonChart();
                    } else {
                        charts.comparison = initComparisonChart();
                        updateComparisonChart();
                    }
                }
            }
        });
    });

    // Field validation
    document.querySelectorAll('.retirement-form input').forEach(field => {
        field.addEventListener('change', function() {
            const scenario = this.closest('form').getAttribute('data-scenario');
            validateFormRelationships(scenario);
        });
    });

    // Initialize charts
    charts.scenario1 = initChart('savingsChart-1', 1);
    charts.scenario2 = initChart('savingsChart-2', 2);

    // Calculate initial projections with default values
    document.getElementById('retirement-form-1').dispatchEvent(new Event('submit'));
    document.getElementById('retirement-form-2').dispatchEvent(new Event('submit'));
});
