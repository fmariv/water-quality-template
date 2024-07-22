<script>
	import { map } from "$stores/map/map";
	import { imageLayers } from "$stores/map/imageLayers";
	import { GeoJSONLayers } from "$stores/map/GeoJSONLayers";
	import { onDestroy, onMount } from "svelte";
	import { browser } from "$app/environment";

	export let left = "left";
	export let right = "right";

	let lsb;
	onMount(async () => {
		if (browser) {
			lsb = await import("/src/lib/map/lsbs/leaflet-side-by-side.js");
		}
	});

	// init lsb
	let control;
	$: {
		if ($map && lsb && !control) {
			control = L.control.sideBySide().addTo($map);
		}
	}

	// react to change in imageLayers
	$: {
		if (control) {
			const leftLayers = [];
			const rightLayers = [];
			Object.keys($imageLayers).forEach((pane) => {
				if (pane == left)
					Object.keys($imageLayers[pane]).forEach((l) =>
						leftLayers.push($imageLayers[pane][l]),
					);
				else if (pane == right)
					Object.keys($imageLayers[pane]).forEach((l) =>
						rightLayers.push($imageLayers[pane][l]),
					);
			});
			Object.keys($GeoJSONLayers).forEach((pane) => {
				if (pane == left)
					Object.keys($GeoJSONLayers[pane]).forEach((l) =>
						leftLayers.push($GeoJSONLayers[pane][l]),
					);
				else if (pane == right)
					Object.keys($GeoJSONLayers[pane]).forEach((l) =>
						rightLayers.push($GeoJSONLayers[pane][l]),
					);
			});
			control.setLeftLayers(leftLayers);
			control.setRightLayers(rightLayers);
		}
	}

	onDestroy(() => {
		if (control && $map) {
			$map.removeControl(control);
		}
	});
</script>
