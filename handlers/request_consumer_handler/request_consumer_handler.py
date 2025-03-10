import threading

class RequestConsumerHandler:
    
    async def consume_requests (
        self,
    ) -> None:
        
        try:
            while self.running:
                client_socket, client_address = self.server_socket.accept()
                
                client_thread = threading.Thread (
                    target=self.IORouter.handle_request, 
                    args=(client_socket, self.allowed_hosts,)
                )
                client_thread.start()
                self.threads.append(client_thread)

        except Exception as e:
            print(f"Error: {e}")

        finally:
            await self.shutdown()