<script>
	import Map from '$components/map/Map.svelte';
	import TileLayer from '$components/map/TileLayer.svelte';
	import LayersControl from '$components/map/LayersControl.svelte';
	import { BASEMAPS, BASEMAP_LAYERS, DEFAULT_BASEMAP, BASEMAP_OPTIONS } from '$components/map/basemaps.js';
	import DateSelector from '$components/map/DateSelector.svelte';
	import Timeline from '$components/analytics/Timeline.svelte';
	import { compareAsc, parseISO } from 'date-fns';
	import ImageLayer from '$components/map/ImageLayer.svelte';
	import Analytics from '$components/Analytics.svelte';
	import Slider from '$components/map/Slider.svelte';
	import { analyticsStore, currentAnalytic } from '$stores/analytics.js';
	import PipelineStatusBanner from '$components/PipelineStatusBanner.svelte';

	export let data;

	$: ({ api_url, images, analytics, aoi } = data);

	$: currentAnalytic.set('Water extent');
	$: analyticsStore.set(analytics);

	let layer = DEFAULT_BASEMAP;
	let xyz_url = '';

	$: sat_images = (images || [])
		.filter((image) => image.includes('sentinel-2-l2a'))
		.map((image) => image.split('_')[1].split('.')[0])
		.sort((a, b) => compareAsc(parseISO(a), parseISO(b)));

	$: hasImages = sat_images.length > 0;
	$: xyz_url = `${api_url}/images`;

	let currentImageLeft, currentImageRight;
	$: if (!currentImageLeft && hasImages) currentImageLeft = sat_images[0];
	$: if (!currentImageRight && hasImages) currentImageRight = sat_images[sat_images.length - 1];

	function onChangeLeft(e) {
		currentImageLeft = sat_images.find((i) => i == e.target.value);
	}
	function onChangeRight(e) {
		currentImageRight = sat_images.find((i) => i == e.target.value);
	}
</script>

<div class="flex min-h-0 flex-1 flex-col">
	<div class="flex min-h-0 flex-1 flex-row gap-3 p-3">
		<div class="relative flex min-h-0 min-w-0 flex-1 flex-col gap-3">
			<PipelineStatusBanner {api_url} />
			<Map
				zoom={6}
				panes={[
					{ name: 'aoi', zIndex: 9999 },
					{ name: 'left', zIndex: 999 },
					{ name: 'right', zIndex: 999 }
				]}
				{aoi}
			>
				{#key layer}
					<TileLayer url={BASEMAPS[layer]} options={BASEMAP_OPTIONS} />
				{/key}
				<LayersControl layers={BASEMAP_LAYERS} bind:layer />
				{#if hasImages}
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
			{#if $currentAnalytic !== '' && hasImages}
				<div class="flex-shrink-0">
					<Timeline height={200} />
				</div>
			{/if}
		</div>
		<div class="flex w-[250px] flex-shrink-0 flex-col overflow-y-auto">
			<Analytics
				{analytics}
				{aoi}
				date={currentImageRight}
				left={currentImageLeft}
				{xyz_url}
				{api_url}
			/>
		</div>
	</div>
</div>
