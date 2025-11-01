import { writable } from "svelte/store";
import { SYSTEM_INFO_API_BASE_URL } from "$lib/constants";

export const systemInfo = writable({
	cpu_usage: null,
	ram_usage: null,
	gpus: {},
	uptime: '',
});

export const requestSystemInfo = async (): Promise<object> => {
	const result = await fetch(`${SYSTEM_INFO_API_BASE_URL}/info`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
		}
	})
	if (!result.ok) {
		const error = await result.text();
		throw error;
	}
	const data = await result.json();
	return data;
};

let handler: ReturnType<typeof setInterval> | null = null;

// start updating 'systemInfo'
export const startSystemInfo = (interval=1000) => {
	
	const fetchResult = async () => {
		try {
			const result = await requestSystemInfo();
			systemInfo.update((prev) => ({ ...prev, ...result }));
		} catch (e) {}
	}
	fetchResult()
	handler = setInterval(fetchResult, interval);
}

// stop updating 'systemInfo'
export const stopSystemInfo = () => {
	if (handler) {
		clearInterval(handler);
	}
}