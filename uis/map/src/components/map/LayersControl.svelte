<script>
	/**
	 * Canonical basemap selector for SPAI template UIs.
	 * Source: spai-new/components-library/components/LayersControl.svelte
	 */
	export let layers = ['satellite', 'streets'];
	export let labels = {
		satellite: 'Satellite',
		streets: 'Streets'
	};
	export let layer = null;

	$: defaultLayer = layers.includes('satellite') ? 'satellite' : (layers[0] ?? null);
	$: if (!layer || !layers.includes(layer)) layer = defaultLayer;
</script>

<form aria-label="Basemap selector">
	{#each layers as layerId}
		<label>
			<input type="radio" bind:group={layer} name="layers" value={layerId} />
			{labels[layerId] ?? layerId}
		</label>
	{/each}
</form>

<style>
	form {
		position: absolute;
		z-index: 999999;
		left: 10px;
		bottom: 10px;
		background-color: #fafafa;
		padding: 5px;
		border-radius: 5px;
		border: 1px solid gray;
		display: flex;
		flex-direction: row;
		gap: 5px;
	}

	label {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 2px;
	}
</style>
