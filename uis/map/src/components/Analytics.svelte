<script>
	import GeoJSONLayer from '$components/map/GeoJSONLayer.svelte';
	import WaterQuality from '$components/analytics/WaterQuality.svelte';

	export let analytics;
	export let aoi;
	export let date;
	export let xyz_url;
	export let api_url;
	export let left;

	let selected = false;
</script>

<div>
	<WaterQuality {analytics} {date} {xyz_url} {api_url} {left} />
</div>

{#if selected}
	<GeoJSONLayer
		name={'aoi'}
		options={{
			style: { fillOpacity: 0, weight: 3, color: 'blue', dashArray: '' },
			pane: 'aoi',
			zIndex: 0
		}}
		geojson={aoi}
	/>
{/if}
