import { writable } from 'svelte/store';

function createMap() {
	const { subscribe, set, update } = writable(null);

	const init = (map) => set(map);

	const remove = () => {
		update((map) => {
			map?.remove();
			return null;
		});
	};

	return {
		subscribe,
		init,
		remove
	};
}

export const map = createMap();
