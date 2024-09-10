import { env } from '$env/dynamic/private';

export async function load({fetch}) {
	const api_url = 'https://' +  env.API_URL;
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