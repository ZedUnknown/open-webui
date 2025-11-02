<script lang="ts">
	import { getVersionUpdates } from '$lib/apis';
	import { WEBUI_BUILD_HASH, WEBUI_VERSION } from '$lib/constants';
	import { WEBUI_NAME, config, showChangelog } from '$lib/stores';
	import { compareVersion } from '$lib/utils';
	import { onMount, getContext, onDestroy } from 'svelte';
	import { user } from '$lib/stores';
	import { startSystemInfo, stopSystemInfo, systemInfo } from '$lib/apis/system_info';

	import Tooltip from '$lib/components/common/Tooltip.svelte';

	const i18n = getContext('i18n');
	
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
	<div class="space-y-3 overflow-y-scroll max-h-[28rem] md:max-h-full p-2">
		<div class="mb-2.5 text-xl font-medium flex space-x-2 items-center justify-center">
			<div>
				{$WEBUI_NAME}
			</div>
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

		<hr class=" border-gray-100 dark:border-gray-850" />
		
		<div class="flex flex-col border border-gray-100 dark:border-gray-850 p-4 rounded-xl">
			<div class="flex w-full justify-end ">
				<div class="text-xs text-gray-500 whitespace-nowrap">
					Copyright (c) {new Date().getFullYear()} <br>
					<span class="text-gray-500 underline">Open WebUI</span>
				</div>
				<!-- Update Available  -->
				{#if $user?.role === 'admin'}
					<div class="flex w-full justify-end items-end">
						<div class="flex flex-col text-xs text-gray-700 dark:text-gray-200">
							<div class="flex gap-1">
								<Tooltip content={WEBUI_BUILD_HASH}>
									v{WEBUI_VERSION}
								</Tooltip>
	
								{#if $config?.features?.enable_version_update_check}
									<a href="https://github.com/open-webui/open-webui/releases/tag/v{version.latest}" target="_blank">
										{updateAvailable === null ? $i18n.t('Checking for updates...') : updateAvailable ? `(v${version.latest} ${$i18n.t('available!')})` : $i18n.t('(latest)')}
									</a>
								{/if}
							</div>
	
							<button class=" underline flex items-center space-x-1 text-xs text-gray-500 dark:text-gray-500"
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
	
			<div class="text-xs text-gray-400 dark:text-gray-500">
				<pre class="text-xs text-gray-400 dark:text-gray-500">
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

4. Notwithstanding any other provision of this License, and as a material condition of the rights granted herein, licensees are strictly prohibited from altering, removing, obscuring, or replacing any "Open WebUI" branding, including but not limited to the name, logo, or any visual, textual, or symbolic identifiers that distinguish the software and its interfaces, in any deployment or distribution, regardless of the number of users, except as explicitly set forth in Clauses 5 and 6 below.

5. The branding restriction enumerated in Clause 4 shall not apply in the following limited circumstances: 
(i) deployments or distributions where the total number of end users (defined as individual natural persons with direct access to the application) does not exceed fifty (50) within any rolling thirty (30) day period; 
(ii) cases in which the licensee is an official contributor to the codebase—with a substantive code change successfully merged into the main branch of the official codebase maintained by the copyright holder—who has obtained specific prior written permission for branding adjustment from the copyright holder; or 
(iii) where the licensee has obtained a duly executed enterprise license expressly permitting such modification. For all other cases, any removal or alteration of the "Open WebUI" branding shall constitute a material breach of license.

6. All code, modifications, or derivative works incorporated into this project prior to the incorporation of this branding clause remain licensed under the BSD 3-Clause License, and prior contributors retain all BSD-3 rights therein; if any such contributor requests the removal of their BSD-3-licensed code, the copyright holder will do so, and any replacement code will be licensed under the project's primary license then in effect. By contributing after this clause's adoption, you agree to the project's Contributor License Agreement (CLA) and to these updated terms for all new contributions.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
					</pre>
			</div>
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
