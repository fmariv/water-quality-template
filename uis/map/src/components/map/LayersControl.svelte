<script>
	export let layers = ['satellite', 'streets'];
	let _layers = layers[0];

	export let layer = null;
	$: layer = _layers;
</script>

<form>
	{#each layers as layer}
		<label>
			<input type="radio" bind:group={_layers} name="layers" value={layer} />
			{layer}
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
