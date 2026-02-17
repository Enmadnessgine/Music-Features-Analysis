const ChartData = JSON.parse("{{ chart_data|escapejs }}");
const FeaturesData = JSON.parse("{{ features_data|escapejs }}");

new Chart($("#genreChart"), {
	type: "doughnut",
	data: {
		labels: ChartData.labels,
		datasets: [{
			data: ChartData.dataset,
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
		labels: FeaturesData.labels,
		datasets: [{
			label: "Features",
			data: FeaturesData.dataset,
			fill: true,
			backgroundColor: 'rgba(13,110,253,0.2)',
			borderColor: '#0d6efd',
			pointBackgroundColor: '#0d6efd'
		}]
	}
});