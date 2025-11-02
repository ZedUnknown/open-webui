import { writable } from "svelte/store";
import { SYSTEM_INFO_API_BASE_URL } from "$lib/constants";

export const systemInfo = writable({
	cpu_usage: null,
	ram_usage: null,
	gpus: {},
	uptime: '',
});

// start updating 'systemInfo'
let socket: WebSocket | null = null;
export const startSystemInfo = () => {
	// removing http:// or https:// from SYSTEM_INFO_API_BASE_URL
	const SANITIZED_SYSTEM_INFO_API_BASE_URL = `ws://${SYSTEM_INFO_API_BASE_URL.replace(/^https?:\/\//, '')}/ws/info`;
	console.log('SANITIZED_SYSTEM_INFO_API_BASE_URL', SANITIZED_SYSTEM_INFO_API_BASE_URL);
	socket = new WebSocket(SANITIZED_SYSTEM_INFO_API_BASE_URL);
	socket.onopen = () => {
		console.log('WebSocket connection opened');
	};
	socket.onmessage = (event) => {
		systemInfo.update((prev) => ({ ...prev, ...JSON.parse(event.data) }));
	}
	socket.onclose = () => {
		console.log('WebSocket connection closed');
	};
	socket.onerror = (error) => {
		console.error('WebSocket error:', error);
	}
}

// stop updating 'systemInfo' (close websocket + reset systemInfo)
export const stopSystemInfo = () => {
	socket?.close();
	systemInfo.set({
		cpu_usage: null,
		ram_usage: null,
		gpus: {},
		uptime: ""
	});
}