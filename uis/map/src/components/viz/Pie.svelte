<script>
	import Chart from "./Chart.svelte";

	export let options;
	export let height;

	const base_options = {
		series: [],
		labels: [],
		chart: {
			type: "donut",
			height,
		},
		dataLabels: {
			enabled: true,
			formatter: function (val) {
				return val.toFixed(2) + "%";
			},
		},
		plotOptions: {
			pie: {
				customScale: 1,
				donut: {
					size: "50%",
					// labels: {
					// 	show: true,
					// 	name: {
					// 		show: true
					// 	},
					// 	value: {
					// 		show: true
					// 	}
					// }
					total: {
						show: true,
					},
				},
			},
		},
		noData: {
			text: "Loading...",
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
		};
	}
</script>

<Chart options={combined_options} />
