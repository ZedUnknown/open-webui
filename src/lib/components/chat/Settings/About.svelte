<script lang="ts">
	import { getVersionUpdates } from '$lib/apis';
	import { getOllamaVersion } from '$lib/apis/ollama';
	import { WEBUI_BUILD_HASH, WEBUI_VERSION } from '$lib/constants';
	import { WEBUI_NAME, config, showChangelog } from '$lib/stores';
	import { compareVersion } from '$lib/utils';
	import { onMount, getContext, onDestroy } from 'svelte';
	import { user } from '$lib/stores';
	import { startSystemInfo, stopSystemInfo, systemInfo } from '$lib/apis/system_info/index';

	import Tooltip from '$lib/components/common/Tooltip.svelte';

	const i18n = getContext('i18n');
	
	let ollamaVersion = '';
	
	let updateAvailable = null;
	let version = {
		current: '',
		latest: ''
	};

	const checkForVersionUpdates = async () => {
		updateAvailable = null;
		version = await getVersionUpdates(localStorage.token).catch((error) => {
			return {
				current: WEBUI_VERSION,
				latest: WEBUI_VERSION
			};
		});
		console.log(version);
		updateAvailable = compareVersion(version.latest, version.current);
		console.log(updateAvailable);
	};

	onMount(async () => {
		ollamaVersion = await getOllamaVersion(localStorage.token).catch((error) => {
			return '';
		});
		if ($config?.features?.enable_version_update_check) {
			checkForVersionUpdates();
		}
		startSystemInfo();
	});

	onDestroy(() => {
		stopSystemInfo();
	});
	
</script>

<div id="tab-about" class="flex flex-col h-full justify-between space-y-3 text-sm mb-6">
	<div class=" space-y-3 overflow-y-scroll max-h-[28rem] md:max-h-full">
		<div>
			<div class=" mb-2.5 text-lg font-medium flex space-x-2 items-center justify-center">
				<div>
					{$WEBUI_NAME}
				</div>
			</div>
			{#if $user?.role === 'admin'}
				<div class="flex w-full justify-between items-center">
					<div class="flex flex-col text-xs text-gray-700 dark:text-gray-200">
						<div class="flex gap-1">
							<Tooltip content={WEBUI_BUILD_HASH}>
								v{WEBUI_VERSION}
							</Tooltip>

							{#if $config?.features?.enable_version_update_check}
								<a
									href="https://github.com/open-webui/open-webui/releases/tag/v{version.latest}"
									target="_blank"
								>
									{updateAvailable === null
										? $i18n.t('Checking for updates...')
										: updateAvailable
											? `(v${version.latest} ${$i18n.t('available!')})`
											: $i18n.t('(latest)')}
								</a>
							{/if}
						</div>

						<button
							class=" underline flex items-center space-x-1 text-xs text-gray-500 dark:text-gray-500"
							on:click={() => {
								showChangelog.set(true);
							}}
						>
							<div>{$i18n.t("See what's new")}</div>
						</button>
					</div>
				</div>
			{/if}
		</div>

		<hr class=" border-gray-100 dark:border-gray-850" />

		<h3 class="text-base font-medium text-gray-900 dark:text-white">
			{$i18n.t('System Information: ')}
		</h3>

		<!-- CPU USAGE -->
		<div class="grid grid-cols-2 gap-4">
			<div class="bg-white/5 dark:bg-gray-500/5 border border-gray-100 dark:border-gray-850 p-4 rounded-lg">
				<div class="text-sm font-medium text-gray-500">CPU Usage</div>
				<div class="text-2xl font-bold text-gray-900 dark:text-white">
					{#if $systemInfo?.cpu_usage}
						{$systemInfo?.cpu_usage}%
					{:else}
						<!-- loading animation -->
						<div class="flex">
							<div class="relative flex w-64 gap-2 pt-2">
								<div class="flex-1">
									<div class="mb-1 h-8 w-3/5 rounded-lg animate-[shimmer_1.5s_infinite_linear]"></div>
								</div>
							</div>
						</div>
					{/if}
				</div>
			</div>

			<!-- Uptime -->
			<div class="bg-white/5 dark:bg-gray-500/5 border border-gray-100 dark:border-gray-850 p-4 rounded-lg">
				<div class="text-sm font-medium text-gray-500">Service Uptime</div>
				<div class="text-2xl font-bold text-gray-900 dark:text-white">
					{#if $systemInfo?.uptime}
						{$systemInfo?.uptime}
					{:else}
						<!-- loading animation -->
						<div class="flex">
							<div class="relative flex w-64 gap-2 pt-2">
								<div class="flex-1">
									<div class="mb-1 h-8 w-3/5 rounded-lg animate-[shimmer_1.5s_infinite_linear]"></div>
								</div>
							</div>
						</div>
					{/if}
				</div>
			</div>
		</div>

		<!-- RAM USAGE -->
		<div class="bg-white/5 dark:bg-gray-500/5 border border-gray-100 dark:border-gray-850 p-4 rounded-lg">
			<div class="text-sm font-medium text-gray-500 mb-2">RAM Usage</div>
			{#if $systemInfo?.ram_usage}
				<div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
					<div
						class="bg-green-500 h-2.5 rounded-full"
						style="width: {$systemInfo?.ram_usage ?? 0}%"
					></div>
				</div>
				<p class="text-xs text-right mt-1 text-gray-600 dark:text-gray-400">{$systemInfo?.ram_usage}% Used</p>
			{:else}
				<!-- loading animation -->
				<div class="flex">
					<div class="relative flex w-64 gap-2 pt-2">
						<div class="flex-1">
							<div class="mb-1 h-8 w-full rounded-lg animate-[shimmer_1.5s_infinite_linear]"></div>
						</div>
					</div>
				</div>
			{/if}
		</div>

		<!-- VRAM USAGE -->
		<div class="grid grid-cols-2 gap-4 mt-4">
			{#if $systemInfo?.gpus && Object.keys($systemInfo.gpus).length > 0}
				{#each Object.entries($systemInfo.gpus) as [gpuId, gpu]}
					<div class="bg-white/5 dark:bg-gray-500/5 border border-gray-100 dark:border-gray-850 p-4 rounded-lg">
						<div class="text-sm font-medium text-gray-500 mb-2">
							<div class="flex items-center space-x-2 gap-2">
								{gpu.name}
							</div>
						</div>
						<div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
							<div
								class="bg-[#00c950] h-2.5 rounded-full"
								style="width: {((gpu.memory_used / gpu.memory_total) * 100).toFixed(1)}%"
							></div>
						</div>
						<p class="text-xs text-right mt-1 text-gray-600 dark:text-gray-400">
							{gpu.memory_used} / {gpu.memory_total} GB Used
						</p>
					</div>
				{/each}
			{/if}
		</div>

	</div>
	{#if $config?.license_metadata}
		<div class="mb-2 text-xs text-center">
			{#if !$WEBUI_NAME.includes('Open WebUI')}
				<span class=" text-gray-500 dark:text-gray-300 font-medium">{$WEBUI_NAME}</span> -
			{/if}

			<span class=" capitalize font-bold">{$config?.license_metadata?.type}</span> license purchased by
			<span class=" capitalize">{$config?.license_metadata?.organization_name}</span>
		</div>
	{/if}

<style>
	@keyframes shimmer {
		0% {
			background: linear-gradient(90deg, #0000001E 25%, #EEEEEE1F 50%, #0000001E 75%);
			background-size: 200% 100%;
			background-position: 200% 0;
		}
		100% {
			background: linear-gradient(90deg, #0000001E 25%, #EEEEEE1F 50%, #0000001E 75%);
			background-size: 200% 100%;
			background-position: -200% 0;
		}
	}
</style>
</div>
