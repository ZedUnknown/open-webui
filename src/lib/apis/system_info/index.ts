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
	// wss:/ for secure websocket
	const SANITIZED_URL = SYSTEM_INFO_API_BASE_URL
						.replace('/^http://', 'ws://')
						.replace('/^https://', 'wss://') + '/ws/info';

	console.log('SANITIZED_URL', SANITIZED_URL);
	socket = new WebSocket(SANITIZED_URL);
	socket.onopen = () => {
		console.log('WebSocket connection opened');
	};
	socket.onmessage = (event) => {
		systemInfo.update((prev) => ({ ...prev, ...JSON.parse(event.data) }));
		console.log('systemInfo updated', systemInfo);
	}
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