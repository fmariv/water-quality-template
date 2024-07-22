import { writable } from 'svelte/store';

function createGeoJSONLayers() {
	const { subscribe, set, update } = writable({});

	const addGeoJSONLayer = (name, geojson, options, map, fit = false) => {
		update((current) => {
			const pane = options.pane;
			if (current[pane]) current[pane][name]?.remove();
			const layer = L.geoJSON(geojson, options);
			if (fit) map.fitBounds(layer.getBounds());
			layer.addTo(map);
			return {
				...current,
				[pane]: { ...current[pane], [name]: layer }
			};
		});
	};

	const removeGeoJSONLayer = (name) => {
		update((current) => {
			Object.keys(current).forEach((pane) => {
				current[pane][name]?.remove();
				delete current[pane][name];
			});
			return { ...current };
		});
	};

	return {
		subscribe,
		addGeoJSONLayer,
		removeGeoJSONLayer
	};
}

export const GeoJSONLayers = createGeoJSONLayers();
