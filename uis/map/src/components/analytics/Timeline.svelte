<script>
	import { compareAsc, parseISO } from 'date-fns';
	import Lines from '$components/viz/Lines.svelte';
	import { analyticsStore, currentAnalytic } from '$stores/analytics.js';

	export let height;
	export let data;

	let analytic;

	$: data = $analyticsStore;
	$: analytic = $currentAnalytic;

	let options = {};
	$: sorted_dates = Object.keys(data['Total']).sort((a, b) => compareAsc(parseISO(a), parseISO(b)));

	$: if (sorted_dates)
		if (analytic === 'Water extent') {
			options = {
				colors: ['#3550BF'],
				xaxis: {
					categories: sorted_dates,
					type: 'datetime'
				},
				series: [
					{
						name: 'Water extent',
						data: sorted_dates.map((date) => data['Percentage [%]'][date])
					}
				]
			};
		} else if (analytic === 'Turbidity' || analytic === 'Chlorophyll' || analytic === 'DOC') {
			options = {
				colors: ['#90ee90', '#ffff00', '#ff0000'],
				xaxis: {
					categories: sorted_dates,
					type: 'datetime'
				},
				series: [
					{
						name: 'Good',
						data: sorted_dates.map((date) => ({
							x: date,
							y: data['Good [Has]'][date]
								? ((data['Good [Has]'][date] / data['Total'][date]) * 100).toFixed(2)
								: 0
						}))
					},
					{
						name: 'Careful',
						data: sorted_dates.map((date) => ({
							x: date,
							y: data['Careful [Has]'][date]
								? ((data['Careful [Has]'][date] / data['Total'][date]) * 100).toFixed(2)
								: 0
						}))
					},
					{
						name: 'Bad',
						data: sorted_dates.map((date) => ({
							x: date,
							y: data['Bad [Has]'][date]
								? ((data['Bad [Has]'][date] / data['Total'][date]) * 100).toFixed(2)
								: 0
						}))
					}
				]
			};
		}
</script>

<Lines {options} {height} />
