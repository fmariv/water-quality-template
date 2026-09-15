<script>
	/**
	 * Portable SPAI pipeline status banner.
	 *
	 * Copy to: uis/<ui-name>/src/components/PipelineStatusBanner.svelte
	 * Mount at page level above the map (relative parent), not in the sidebar.
	 *
	 * Props:
	 *   api_url — base URL of the API that exposes GET /pipeline/status
	 */
	import { onMount, onDestroy } from 'svelte';

	export let api_url;

	const POLL_MS = 5000;
	const READY_HIDE_MS = 3000;
	const UNREACHABLE_AFTER = 6; // ~30s of sustained failures
	const EP_TURQUOISE = '#00C9B1';

	/** @type {'Idle'|'Building'|'Warning'|'Error'|'Ready'|'Unreachable'} */
	let status = 'Idle';
	let message = '';
	let visible = true;
	let pollId = null;
	let hideTimeout = null;
	let consecutiveFailures = 0;

	const KNOWN = new Set(['Idle', 'Building', 'Warning', 'Error', 'Ready']);

	/** Unwrap pandas column-orient leftovers: {"0":"Error"} → "Error" */
	const unwrap = (value) => {
		if (value == null) return null;
		if (typeof value === 'object' && !Array.isArray(value)) {
			if (Object.prototype.hasOwnProperty.call(value, '0')) return unwrap(value['0']);
			if (Object.prototype.hasOwnProperty.call(value, 0)) return unwrap(value[0]);
			const vals = Object.values(value);
			if (vals.length === 1) return unwrap(vals[0]);
		}
		if (Array.isArray(value) && value.length === 1) return unwrap(value[0]);
		return value;
	};

	const normalizeStatus = (raw) => {
		const s = unwrap(raw);
		if (s == null || s === '') return null;
		const text = String(s).trim();
		return KNOWN.has(text) ? text : null;
	};

	const isProcessing = (s) => s === 'Idle' || s === 'Building';

	const titleFor = (s) => {
		if (s === 'Error') return 'Error downloading data';
		if (s === 'Unreachable') return 'Unable to read pipeline status';
		if (s === 'Warning') return 'Heads up';
		if (s === 'Ready') return 'Your data is ready';
		return 'Preparing your data';
	};

	const subtitleFor = (s, msg) => {
		if (s === 'Error') return 'Check the logs or contact support.';
		if (s === 'Unreachable') {
			return 'Could not reach the status API. Check the logs or contact support.';
		}
		if (s === 'Warning') return msg || 'Processing continues with incomplete layers.';
		if (s === 'Ready') return msg || 'Layers are available on the map.';
		return 'Downloading and processing the required layers. Please wait a few minutes…';
	};

	const cardStyle = (s) => {
		if (s === 'Error' || s === 'Unreachable') {
			return 'border-color: #FECACA; background: #FFF7F7;';
		}
		if (s === 'Warning') return 'border-color: #FDE68A; background: #FFFBEB;';
		if (s === 'Ready') return 'border-color: #BBF7D0; background: #F0FDF4;';
		return 'border-color: #E5E7EB; background: #FFFFFF;';
	};

	const accentFor = (s) => {
		if (s === 'Error' || s === 'Unreachable') return '#E11D48';
		if (s === 'Warning') return '#D97706';
		if (s === 'Ready') return '#16A34A';
		return EP_TURQUOISE;
	};

	const stopPolling = () => {
		if (pollId != null) {
			clearInterval(pollId);
			pollId = null;
		}
	};

	const markUnreachable = () => {
		consecutiveFailures += 1;
		// Stay on Idle/Building ("Preparing…") during early / transient failures.
		// Only surface Unreachable after sustained failure (~30s).
		if (consecutiveFailures >= UNREACHABLE_AFTER) {
			status = 'Unreachable';
			message = '';
			visible = true;
		}
	};

	const fetchStatus = async () => {
		try {
			const res = await fetch(`${api_url}/pipeline/status`);
			if (!res.ok) {
				markUnreachable();
				return;
			}
			const data = await res.json();
			// Also unwrap if the whole payload is column-orient
			let statusRaw = data?.status;
			if (
				statusRaw == null &&
				data &&
				typeof data === 'object' &&
				data.status == null &&
				Object.prototype.hasOwnProperty.call(data, '0')
			) {
				statusRaw = data;
			}
			const next = normalizeStatus(statusRaw);
			if (!next) {
				markUnreachable();
				return;
			}

			consecutiveFailures = 0;
			status = next;
			const msg = unwrap(data?.message);
			message = msg == null ? '' : String(msg);

			if (next === 'Ready') {
				stopPolling();
				visible = true;
				if (hideTimeout != null) clearTimeout(hideTimeout);
				hideTimeout = setTimeout(() => {
					visible = false;
				}, READY_HIDE_MS);
			} else if (next === 'Error') {
				stopPolling();
				visible = true;
			} else {
				visible = true;
			}
		} catch {
			markUnreachable();
		}
	};

	onMount(() => {
		fetchStatus();
		pollId = setInterval(fetchStatus, POLL_MS);
	});

	onDestroy(() => {
		stopPolling();
		if (hideTimeout != null) clearTimeout(hideTimeout);
	});
</script>

{#if visible}
	<div class="pointer-events-none fixed inset-x-0 top-16 z-[5000] flex justify-center px-3">
		<div
			class="flex w-full max-w-[440px] items-start gap-3 border px-4 py-3 shadow-md"
			style={`border-radius: 12px; ${cardStyle(status)}`}
			role="status"
			aria-live="assertive"
		>
			{#if isProcessing(status)}
				<span
					class="mt-0.5 inline-block h-4 w-4 flex-shrink-0 animate-spin rounded-full border-2 border-transparent"
					style={`border-top-color: ${EP_TURQUOISE}; border-right-color: ${EP_TURQUOISE};`}
					aria-hidden="true"
				/>
			{:else}
				<span
					class="mt-1.5 h-2.5 w-2.5 flex-shrink-0 rounded-full"
					style={`background-color: ${accentFor(status)};`}
					aria-hidden="true"
				/>
			{/if}
			<div class="min-w-0 flex-1">
				<p class="text-sm font-semibold leading-snug text-neutral-800">{titleFor(status)}</p>
				<p class="mt-0.5 text-xs leading-snug text-neutral-600">
					{subtitleFor(status, message)}
				</p>
			</div>
		</div>
	</div>
{/if}
