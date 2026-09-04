const API_BASE_URL = "http://localhost:8000/api/v1";
const WS_URL = "ws://localhost:8000/ws/transactions";

export const fetchRecentTransactions = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/recent-transactions`);
        return await response.json();
    } catch (error) {
        console.error("Error fetching historic transactions:", error);
        return [];
    }
};

export const connectWebSocket = (onMessageReceived) => {
    const ws = new WebSocket(WS_URL);

    ws.onopen = () => console.log("Connected to Real-Time Fraud Stream WS");
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        onMessageReceived(data);
    };
    ws.onerror = (err) => console.error("WebSocket Error:", err);
    ws.onclose = () => {
        console.log("WebSocket Disconnected. Reconnecting in 3s...");
        setTimeout(() => connectWebSocket(onMessageReceived), 3000);
    };

    return ws;
};