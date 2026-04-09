<script>
	/**
	 * EarthPulse light wordmark. Requires `static/earthpulse-logo-light.png` in the SvelteKit app.
	 * Canonical source: `components-library/components/Logo.svelte` — copy to `uis/map/src/components/branding/Logo.svelte`.
	 * Reference PNG: `components-library/assets/earthpulse-logo-light.png` (see `docs/Logo.md`).
	 */
	export let src = '/earthpulse-logo-light.png';
	export let alt = 'EarthPulse';
	export let href = 'https://earthpulse.ai';
	export let width = 132;
	export let height = 26;
	export let imgClass = '';
</script>

<a
	{href}
	class="inline-flex items-center"
	target="_blank"
	rel="noopener noreferrer"
>
	<img
		{src}
		{alt}
		{width}
		{height}
		class="h-auto w-auto max-h-14 object-contain {imgClass}"
		loading="lazy"
		decoding="async"
	/>
</a>
