/**
 * Canonical basemap configuration for SPAI template UIs.
 * Source: spai-new/components-library/components/basemaps.js
 * Docs:   spai-new/components-library/docs/Basemap.md
 *
 * To add a new basemap, add an entry to BASEMAPS — BASEMAP_LAYERS updates automatically.
 */

export const BASEMAPS = {
	satellite:
		'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
	streets:
		'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}'
};

export const BASEMAP_LAYERS = Object.keys(BASEMAPS);

export const DEFAULT_BASEMAP = 'satellite';

export const BASEMAP_OPTIONS = { maxZoom: 20, zIndex: 1 };
