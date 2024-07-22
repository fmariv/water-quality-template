import { env } from '$env/dynamic/private';

export async function load({fetch}) {
	const xyz_url = 'http://' +  env.XYZ_URL;
	const analytics_url = 'http://' +  env.ANALYTICS_URL;
	let res = [
		await fetch(`${xyz_url}/`),
		await fetch(`${analytics_url}/table_water_extent`),
		await fetch(`${xyz_url}/aoi`)
	];
	const [images, analytics, aoi] = await Promise.all(res.map(r => r.json()));
	return {
		xyz_url,
		images,
		analytics,
		analytics_url,
		aoi
	};
}