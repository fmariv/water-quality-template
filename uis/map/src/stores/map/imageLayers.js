import { writable } from 'svelte/store';

function createImageLayers() {
	const { subscribe, set, update } = writable({});

	const addImageLayer = (pane, name, layer) => {
		update((current) => ({ ...current, [pane]: { ...current[pane], [name]: layer } }));
	};

	const removeImageLayer = (name, pane) => {
		update((current) => {
			if (pane && current[pane]) {
				const layer = current[pane][name];
				layer?.remove();
				delete current[pane][name];
			}
			return { ...current };
		});
	};

	return {
		subscribe,
		addImageLayer,
		removeImageLayer
	};
}

export const imageLayers = createImageLayers();
