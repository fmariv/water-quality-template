<script>
	import { onMount } from "svelte";
	import { browser } from "$app/environment";

	export let options;

	let ApexCharts, viz, chart;

	onMount(async () => {
		if (browser) {
			ApexCharts = (await import("apexcharts")).default;
		}
	});

	$: {
		if (ApexCharts) {
			if (!chart) {
				chart = new ApexCharts(viz, options);
				chart.render();
			} else chart.updateOptions(options);
		}
	}
</script>

<div bind:this={viz} />
