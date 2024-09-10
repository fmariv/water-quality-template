<script>
	import Map from '$components/map/Map.svelte';
	import TileLayer from '$components/map/TileLayer.svelte';
	import LayersControl from '$components/map/LayersControl.svelte';
	import DateSelector from '$components/map/DateSelector.svelte';
	import Timeline from '$components/analytics/Timeline.svelte';
	import { compareAsc, parseISO } from 'date-fns';
	import ImageLayer from '$components/map/ImageLayer.svelte';
	import Analytics from '$components/Analytics.svelte';
	import Slider from '$components/map/Slider.svelte';
	import { analyticsStore, currentAnalytic } from '$stores/analytics.js';

	export let data;

	$: ({ api_url, images, analytics, aoi } = data);

	$: currentAnalytic.set('Water extent');
	$: analyticsStore.set(analytics);

	let layer;
	let errorMessage = '';
	let xyz_url = '';

	$: sat_images = images
		.filter((image) => image.includes('sentinel-2-l2a'))
		.map((image) => image.split('_')[1].split('.')[0])
		.sort((a, b) => compareAsc(parseISO(a), parseISO(b)));

	$: xyz_url = `${api_url}/images`;

	// Check if there are no images available
	$: if (sat_images.length === 0) {
		errorMessage = 'No images or layers have been found.';
	} else if (typeof analytics === 'object' && 'detail' in analytics) {
		errorMessage = 'No water have been found.';
	}

	let currentImageLeft, currentImageRight;
	$: if (!currentImageLeft) currentImageLeft = sat_images[0];
	$: if (!currentImageRight) currentImageRight = sat_images[sat_images.length - 1];

	// select image
	function onChangeLeft(e) {
		currentImageLeft = sat_images.find((i) => i == e.target.value);
	}
	function onChangeRight(e) {
		currentImageRight = sat_images.find((i) => i == e.target.value);
	}
</script>

{#if errorMessage}
	<div
		class="error-message"
		style="color: red; font-weight: bold; padding: 10px; background: #ffe0e0;"
	>
		{errorMessage}
	</div>
{/if}
<div class="w-screen h-screen flex flex-row gap-3 p-3">
	<div class="flex flex-col flex-1 gap-3">
		<Map
			zoom={6}
			panes={[
				{ name: 'aoi', zIndex: 9999 },
				{ name: 'left', zIndex: 999 },
				{ name: 'right', zIndex: 999 }
			]}
			{aoi}
		>
			{#if layer == 'light'}
				<TileLayer
					url={'https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png'}
					options={{ maxZoom: 20, zIndex: 1 }}
				/>
			{:else if layer == 'satellite'}
				<TileLayer
					url={'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'}
					options={{ maxZoom: 20, zIndex: 1 }}
				/>
			{:else if layer == 'streets'}
				<TileLayer
					url={'https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png'}
					options={{ maxZoom: 20, zIndex: 1 }}
				/>
			{:else if layer == 'dark'}
				<TileLayer
					url={'https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png'}
					options={{ maxZoom: 20, zIndex: 1 }}
				/>
			{/if}
			<LayersControl layers={['light', 'dark', 'streets', 'satellite']} bind:layer />
			{#if !errorMessage}
				<DateSelector dates={sat_images} onChange={onChangeLeft} selected={currentImageLeft} />
				<DateSelector
					dates={sat_images}
					onChange={onChangeRight}
					position="right-2"
					selected={currentImageRight}
				/>
				<ImageLayer
					XYZ_URL={xyz_url}
					name="sat"
					image={'sentinel-2-l2a_' + currentImageLeft + '.tif'}
					options={{
						maxZoom: 20,
						pane: 'left'
					}}
				/>
				<ImageLayer
					XYZ_URL={xyz_url}
					name="sat"
					image={'sentinel-2-l2a_' + currentImageLeft + '.tif'}
					options={{
						maxZoom: 20,
						pane: 'left'
					}}
				/>
				<ImageLayer
					XYZ_URL={xyz_url}
					name="sat"
					image={'sentinel-2-l2a_' + currentImageRight + '.tif'}
					options={{
						maxZoom: 20,
						pane: 'right'
					}}
				/>
				<Slider />
			{/if}
		</Map>
		{#if $currentAnalytic !== '' && !errorMessage}
			<Timeline height={200} />
		{/if}
	</div>
	<div class="w-[200px]">
		{#if !errorMessage}
			<Analytics
				{analytics}
				{aoi}
				date={currentImageRight}
				left={currentImageLeft}
				{xyz_url}
				{api_url}
			/>
		{/if}
	</div>
</div>
