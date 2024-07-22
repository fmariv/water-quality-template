<script>
	export let dates;
	export let onChange;
	export let selected;
	export let position = "left-2";
</script>

{#if dates}
	<select
		on:change={onChange}
		class={`py-2 px-2 absolute z-[9999] mt-2 bg-white border-black rounded-md hover:bg-gray-100 ${position}`}
	>
		{#each dates as date}
			<option value={date} selected={date == selected}>{date}</option>
		{/each}
	</select>
{/if}
