import { env } from '$env/dynamic/private';

/** SPAI local run sets API_URL to `host:port` (e.g. localhost:8021) with no scheme — always HTTP. */
function apiBaseUrl() {
	let raw = (env.API_URL ?? '').trim();
	if (!raw) return 'http://localhost:8021';
	if (/^https?:\/\//i.test(raw)) return raw.replace(/\/$/, '');
	const isLocal =
		/^(localhost|127\.0\.0\.1)(:\d+)?$/i.test(raw) ||
		raw.startsWith('localhost:') ||
		raw.startsWith('127.0.0.1:');
	const scheme =
		isLocal ? 'http' : import.meta.env.VITE_ENV === 'PRO' ? 'https' : 'http';
	return `${scheme}://${raw}`;
}

export async function load({ fetch }) {
	const api_url = apiBaseUrl();

	const safeFetch = async (path) => {
		try {
			const res = await fetch(`${api_url}${path}`);
			if (res.ok) return await res.json();
		} catch {
			// API may be unavailable during bootstrap
		}
		return null;
	};

	const [images, analytics, aoi] = await Promise.all([
		safeFetch('/images'),
		safeFetch('/analytics/table_water_extent'),
		safeFetch('/aoi')
	]);

	return {
		api_url,
		images: images ?? [],
		analytics: analytics ?? {},
		aoi: aoi ?? null
	};
}
