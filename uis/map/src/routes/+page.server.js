import { env } from '$env/dynamic/private';

export async function load({fetch}) {
	const ENV = import.meta.env.VITE_ENV;
    let origin = ENV === 'PRO' ? 'https://' : 'http://';
    const api_url = `${origin}${env.API_URL}`;

	let res = [
		await fetch(`${api_url}/images`),
		await fetch(`${api_url}/analytics/table_water_extent`),
		await fetch(`${api_url}/aoi`)
	];
	const [images, analytics, aoi] = await Promise.all(res.map(r => r.json()));
	return {
		api_url,
		images,
		analytics,
		aoi
	};
}