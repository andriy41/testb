from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set
import logging
import json
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

class WebSocketManager:
    """
    Manages WebSocket connections and broadcasts market data updates.
    """
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.logger = logging.getLogger(__name__)
        
    async def connect(self, websocket: WebSocket, symbol: str):
        """
        Connect a client to receive updates for a specific symbol.
        
        Args:
            websocket: WebSocket connection
            symbol: Trading symbol to subscribe to
        """
        await websocket.accept()
        
        if symbol not in self.active_connections:
            self.active_connections[symbol] = set()
        self.active_connections[symbol].add(websocket)
        
        self.logger.info(f"Client connected to {symbol} feed. Total connections: {len(self.active_connections[symbol])}")
        
    async def disconnect(self, websocket: WebSocket, symbol: str):
        """
        Disconnect a client from a symbol's updates.
        
        Args:
            websocket: WebSocket connection
            symbol: Trading symbol to unsubscribe from
        """
        self.active_connections[symbol].remove(websocket)
        if not self.active_connections[symbol]:
            del self.active_connections[symbol]
            
        self.logger.info(f"Client disconnected from {symbol} feed")
        
    async def broadcast(self, symbol: str, message: dict):
        """
        Broadcast a message to all clients subscribed to a symbol.
        
        Args:
            symbol: Trading symbol
            message: Message to broadcast
        """
        if symbol not in self.active_connections:
            return
            
        # Add timestamp to message
        message['timestamp'] = datetime.now().isoformat()
        
        # Broadcast to all connected clients
        disconnected = set()
        for connection in self.active_connections[symbol]:
            try:
                await connection.send_json(message)
            except Exception as e:
                self.logger.error(f"Error broadcasting to client: {str(e)}")
                disconnected.add(connection)
                
        # Clean up disconnected clients
        for connection in disconnected:
            await self.disconnect(connection, symbol)

# Create WebSocket manager instance
ws_manager = WebSocketManager()

async def websocket_endpoint(websocket: WebSocket, symbol: str):
    """
    WebSocket endpoint for real-time market data updates.
    
    Args:
        websocket: WebSocket connection
        symbol: Trading symbol to subscribe to
    """
    try:
        await ws_manager.connect(websocket, symbol)
        
        try:
            while True:
                # Wait for any client messages (e.g., ping/pong)
                data = await websocket.receive_text()
                
                # Echo back to confirm connection is alive
                await websocket.send_json({
                    "type": "pong",
                    "symbol": symbol,
                    "timestamp": datetime.now().isoformat()
                })
                
        except WebSocketDisconnect:
            await ws_manager.disconnect(websocket, symbol)
            
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        raise

async def start_market_data_broadcast():
    """
    Start broadcasting market data updates to connected clients.
    This would typically be called when the application starts.
    """
    while True:
        try:
            # Broadcast updates for each symbol with active connections
            for symbol in list(ws_manager.active_connections.keys()):
                # Here you would typically get real market data
                # For now, we'll just send a heartbeat
                await ws_manager.broadcast(symbol, {
                    "type": "heartbeat",
                    "symbol": symbol,
                    "status": "active"
                })
                
            # Wait before next update
            await asyncio.sleep(1)
            
        except Exception as e:
            logger.error(f"Broadcast error: {str(e)}")
            await asyncio.sleep(5)  # Wait longer on error
