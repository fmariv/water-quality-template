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

	const res = [
		await fetch(`${api_url}/images`),
		await fetch(`${api_url}/analytics/table_water_extent`),
		await fetch(`${api_url}/aoi`)
	];
	const [images, analytics, aoi] = await Promise.all(res.map((r) => r.json()));
	return {
		api_url,
		aoi
	};
}
