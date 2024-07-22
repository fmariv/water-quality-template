<script>
	import Chart from "./Chart.svelte";

	export let options;
	export let height;
	export let loading = false;

	const base_options = {
		chart: {
			height,
			type: "area",
		},
		series: [],
		dataLabels: {
			enabled: false,
		},
		stroke: {
			curve: "smooth",
		},
		// markers: {
		// 	size: 5
		// },
		yaxis: {
			labels: {
				formatter: function (value) {
					return value + "%";
				},
			},
		},
		fill: {
			type: "gradient",
			gradient: {
				shadeIntensity: 1,
				opacityFrom: 0.7,
				opacityTo: 0.9,
				stops: [0, 90, 100],
			},
		},
		legend: {
			show: true,
			position: "bottom",
		},
		tooltip: {
			y: {
				formatter: function (value) {
					return value?.toFixed(2) + "%";
				},
			},
		},
		noData: {
			text: loading ? "Loading..." : "No data",
			align: "center",
			verticalAlign: "middle",
			offsetX: 0,
			offsetY: 0,
			style: {
				color: "#000000",
				fontSize: "14px",
				fontFamily: "Helvetica",
			},
		},
	};

	let combined_options = { ...options };
	$: {
		combined_options = {
			...base_options,
			...options,
			noData: {
				...base_options.noData,
				...options.noData,
				text: loading ? "Loading..." : "No data",
			},
		};
	}
</script>

<Chart options={combined_options} />
