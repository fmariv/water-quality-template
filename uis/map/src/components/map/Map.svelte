<script>
	import { onMount, onDestroy, setContext } from "svelte";
	import { map } from "$stores/map/map";
	import { browser } from "$app/environment";
	import "$styles/map.css";

	export let options = {
		attributionControl: false,
		drawControls: true,
		max_zoom: 20,
	};
	export let zoomPosition = "bottomright";
	export let zoom = null;
	export let position = null;
	export let panes = null;
	export let aoi = null;

	let _map;
	onMount(async () => {
		if (browser) {
			const L = await import("leaflet");
			_map = L.map("map", options);
			if (aoi) _map.fitBounds(L.geoJSON(aoi).getBounds());
			else _map.setView(position, zoom);
			_map.zoomControl.setPosition(zoomPosition);
			panes?.forEach(({ name, zIndex }) => {
				_map.createPane(name);
				_map.getPane(name).style.zIndex = zIndex;
				_map.getPane(name).style.pointerEvents = "none";
			});
			map.init(_map);
		}
	});

	onDestroy(() => {
		map.remove();
	});

	setContext("map", {
		getMap: () => _map,
	});
</script>

<div id="map">
	{#if $map}
		<slot />
	{/if}
</div>
