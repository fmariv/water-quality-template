<script>
	import '$styles/app.css';
	import Logo from '$components/branding/Logo.svelte';
</script>

<div class="drawer">
	<input id="nav-drawer" type="checkbox" class="drawer-toggle" />
	<div class="drawer-content flex flex-col min-h-screen">
		<div class="w-full navbar border-b flex justify-between">
			<div>
				<div class="flex-none lg:hidden">
					<label for="nav-drawer" class="btn btn-square btn-ghost">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							class="inline-block w-6 h-6 stroke-current"
							><path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M4 6h16M4 12h16M4 18h16"
							/></svg
						>
					</label>
				</div>
				<div class="px-2 hidden sm:block">
					<Logo />
				</div>
			</div>
		</div>

		<main class="flex-1 h-full">
			<slot />
		</main>
	</div>
	<div class="drawer-side">
		<label for="nav-drawer" class="drawer-overlay"></label>
		<div
			class="menu p-4 overflow-y-auto w-60 bg-base-100 flex flex-col items-center justify-between h-full"
		>
			<div class="flex flex-col items-center space-y-6 w-full"></div>
		</div>
	</div>
</div>
