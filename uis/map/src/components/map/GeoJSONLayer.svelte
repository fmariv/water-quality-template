<script>
	import { map } from "$stores/map/map";
	import { GeoJSONLayers } from "$stores/map/GeoJSONLayers";
	import { onDestroy } from "svelte";

	export let name;
	export let geojson;
	export let options;
	export let fit = false;

	$: if ($map && geojson)
		GeoJSONLayers.addGeoJSONLayer(name, geojson, options, $map, fit);

	onDestroy(() => {
		GeoJSONLayers.removeGeoJSONLayer(name);
	});
</script>
