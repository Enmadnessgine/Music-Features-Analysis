new Chart($("#genreChart"), {
	type: "doughnut",
	data: {
		labels: window.ChartData.labels,
		datasets: [{
			data: window.ChartData.dataset,
			backgroundColor: [
				'#0d6efd',
				'#6f42c1',
				'#20c997',
				'#fd7e14',
				'#adb5bd'
			]
		}]
	},
	options: {
		plugins: {
			legend: {
				position: 'bottom'
			}
		}
	}
});

new Chart($("#radarChart"), {
	type: "radar",
	data: {
		labels: window.FeaturesData.labels,
		datasets: [{
			label: "Features",
			data: window.FeaturesData.dataset,
			fill: true,
			backgroundColor: 'rgba(13,110,253,0.2)',
			borderColor: '#0d6efd',
			pointBackgroundColor: '#0d6efd'
		}]
	}
});