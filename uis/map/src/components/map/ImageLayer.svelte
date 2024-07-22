<script>
	import { map } from "$stores/map/map";
	import { imageLayers } from "$stores/map/imageLayers";
	import { onDestroy } from "svelte";

	export let name;
	export let image;
	export let XYZ_URL;
	export let options;
	export let bands = [4, 3, 2];
	export let stretch = [0, 3000];
	export let palette = "viridis";

	let layer;
	$: if ($map) {
		const pane = options.pane;
		if ($imageLayers[pane] && $imageLayers[pane][name]) {
			$imageLayers[pane][name].setUrl(url);
		} else {
			layer = L.tileLayer(url, options).addTo($map);
			imageLayers.addImageLayer(pane, name, layer);
		}
	}

	onDestroy(() => {
		imageLayers.removeImageLayer(name, options.pane);
	});

	$: url = `${XYZ_URL}/${image}/{z}/{x}/{y}.png?stretch=${stretch}&bands=${bands}&palette=${palette}`;
</script>
