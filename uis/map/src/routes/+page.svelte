<script>
	import Map from '$components/map/Map.svelte';
	import TileLayer from '$components/map/TileLayer.svelte';
	import LayersControl from '$components/map/LayersControl.svelte';
	import { BASEMAPS, BASEMAP_LAYERS, DEFAULT_BASEMAP, BASEMAP_OPTIONS } from '$components/map/basemaps.js';

	export let data;

	$: ({ aoi } = data);

	let layer = DEFAULT_BASEMAP;
</script>
<div class="w-full h-full p-3">
	<Map
		zoom={6}
		panes={[
			{ name: 'aoi', zIndex: 9999 }
		]}
		{aoi}
	>
		{#key layer}
			<TileLayer url={BASEMAPS[layer]} options={BASEMAP_OPTIONS} />
		{/key}
		<LayersControl layers={BASEMAP_LAYERS} bind:layer />
	</Map>
</div>
