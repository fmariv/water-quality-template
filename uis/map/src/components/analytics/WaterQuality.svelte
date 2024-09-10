<script>
	import Waves from 'svelte-material-icons/Waves.svelte';
	import Opacity from 'svelte-material-icons/Opacity.svelte';
	import LeafCircle from 'svelte-material-icons/LeafCircle.svelte';
	import WaterOpacity from 'svelte-material-icons/WaterOpacity.svelte';
	import Pie from '$components/viz/Pie.svelte';
	import ImageLayer from '$components/map/ImageLayer.svelte';
	import { analyticsStore, currentAnalytic } from '$stores/analytics.js';

	export let title;
	export let analytics;
	export let date;
	export let xyz_url;
	export let api_url;
	export let left;

	$: title = $currentAnalytic;
	$: image = 'water_mask_';
	$: bands = [1];
	$: stretch = [0, 1];
	$: palette = 'RdYlGn';

	let selectedButton = 'extent';
	let selected = true;

	let options = {};
	$: if (analytics && date && title === 'Water extent') {
		palette = 'Blues';
		options = {
			series: [analytics['Water [Has]'][date], analytics['Not Water [Has]'][date]],
			labels: ['Water', 'Not Water'],
			tooltip: {
				y: {
					formatter: function (value) {
						return parseInt(value).toLocaleString('en-US') + ' Has';
					}
				}
			},
			dataLabels: {
				formatter: function (val, opts) {
					return parseInt(0.01 * val * analytics['Total']['2020-01-08']).toLocaleString('en-US');
				}
			},
			colors: ['#3550BF', '#BF3535'],
			plotOptions: {
				pie: {
					donut: {
						labels: {
							show: true,
							value: {
								formatter: function (v) {
									return Number.parseInt(v).toLocaleString('en-US') + 'Has';
								}
							},
							total: {
								show: true,
								label: 'Total',
								color: '#373d3f',
								formatter: function (w) {
									const total = w.globals.seriesTotals.reduce((a, b) => {
										return a + b;
									}, 0);
									return parseInt(total).toLocaleString('en-US') + 'Has';
								}
							}
						}
					}
				}
			},
			legend: {
				position: 'bottom'
			}
		};
	} else if (
		(analytics && date && title === 'Turbidity') ||
		title === 'Chlorophyll' ||
		title === 'DOC'
	) {
		options = {
			series: [
				analytics['Good [Has]'][date],
				analytics['Careful [Has]'][date],
				analytics['Bad [Has]'][date]
			],
			labels: ['Good', 'Careful', 'Bad'],
			colors: ['#90ee90', '#ffff00', '#ff0000'],
			plotOptions: {
				pie: {
					donut: {
						labels: {
							show: true,
							value: {
								formatter: function (v) {
									return Number.parseInt(v).toLocaleString('en-US') + ' Has';
								}
							},
							total: {
								show: true,
								label: 'Total',
								color: '#373d3f',
								formatter: function (w) {
									const total = w.globals.seriesTotals.reduce((a, b) => {
										return a + b;
									}, 0);
									return parseInt(total).toLocaleString('en-US') + ' Has';
								}
							}
						}
					}
				}
			},
			legend: {
				position: 'bottom'
			}
		};
	}

	const fecthWaterExtent = async () => {
		if (selected && $currentAnalytic === 'Water extent') {
			selected = false;
			selectedButton = '';
			currentAnalytic.set('');
			return;
		}
		if (!selected) {
			selected = true;
		}
		const response = await fetch(`${api_url}/analytics/table_water_extent`);
		const data = await response.json();
		analytics = data;
		analyticsStore.set(analytics);
		currentAnalytic.set('Water extent');
		image = 'water_mask_';
		bands = [1];
		stretch = [0, 1];
		palette = 'Blues';
		selectedButton = 'extent';
	};

	const fecthTurbidity = async () => {
		if (selected && $currentAnalytic === 'Turbidity') {
			selected = false;
			selectedButton = '';
			currentAnalytic.set('');
			return;
		}
		if (!selected) {
			selected = true;
		}
		const response = await fetch(`${api_url}/analytics/table_turbidity_Ha`);
		const data = await response.json();
		analytics = data;
		analyticsStore.set(analytics);
		currentAnalytic.set('Turbidity');
		image = 'ndti_masked_'; // Change to RGB
		bands = [1];
		stretch = [-1, 1];
		palette = 'RdYlGn_r';
		selectedButton = 'turbidity';
	};

	const fecthChlorophyll = async () => {
		if (selected && $currentAnalytic === 'Chlorophyll') {
			selected = false;
			selectedButton = '';
			currentAnalytic.set('');
			return;
		}
		if (!selected) {
			selected = true;
		}
		const response = await fetch(`${api_url}/analytics/table_chlorophyll_Ha`);
		const data = await response.json();
		analytics = data;
		analyticsStore.set(analytics);
		currentAnalytic.set('Chlorophyll');
		image = 'ndci_masked_'; // Change to RGB
		bands = [1];
		stretch = [-1, 1];
		palette = 'RdYlGn_r';
		selectedButton = 'chlorophyll';
	};

	const fecthDOC = async () => {
		if (selected && $currentAnalytic === 'Dissolved Organic Carbon') {
			selected = false;
			selectedButton = '';
			currentAnalytic.set('');
			return;
		}
		if (!selected) {
			selected = true;
		}
		const response = await fetch(`${api_url}/analytics/table_DOC_Ha`);
		const data = await response.json();
		analytics = data;
		analyticsStore.set(analytics);
		currentAnalytic.set('DOC');
		image = 'DOC_masked_'; // Change to RGB
		bands = [1];
		stretch = [0, 100];
		palette = 'RdYlGn_r';
		selectedButton = 'doc';
	};
</script>

<h1>Water Body</h1>

<button
	data-tip="Water extent"
	class={`w-10 h-10 p-1 hover:bg-gray-100 ${selectedButton === 'extent' ? 'text-green-600' : 'text-gray-800'} tooltip tooltip-bottom`}
	on:click={fecthWaterExtent}
>
	<Waves size="100%" />
</button>

<h1>Monitoring of</h1>

<button
	data-tip="Turbidity"
	class={`w-10 h-10 p-1 hover:bg-gray-100 ${selectedButton === 'turbidity' ? 'text-green-600' : 'text-gray-800'} tooltip tooltip-bottom`}
	on:click={fecthTurbidity}
>
	<Opacity size="100%" />
</button>

<button
	data-tip="Chlorophyll"
	class={`w-10 h-10 p-1 hover:bg-gray-100 ${selectedButton === 'chlorophyll' ? 'text-green-600' : 'text-gray-800'} tooltip tooltip-bottom`}
	on:click={fecthChlorophyll}
>
	<LeafCircle size="100%" />
</button>

<button
	data-tip="Dissolved Organic Carbon"
	class={`w-10 h-10 p-1 hover:bg-gray-100 ${selectedButton === 'doc' ? 'text-green-600' : 'text-gray-800'} tooltip tooltip-bottom`}
	on:click={fecthDOC}
>
	<WaterOpacity size="100%" />
</button>

{#if selected}
	<h3>{title}</h3>
	<Pie {options} height={300} />
{/if}

{#if selected}
	<ImageLayer
		XYZ_URL={xyz_url}
		name="vegetation"
		image={image + left + '.tif'}
		options={{
			maxZoom: 20,
			pane: 'left'
		}}
		{bands}
		{stretch}
		{palette}
	/>
	<ImageLayer
		XYZ_URL={xyz_url}
		name="vegetation"
		image={image + date + '.tif'}
		options={{
			maxZoom: 20,
			pane: 'right'
		}}
		{bands}
		{stretch}
		{palette}
	/>
{/if}
