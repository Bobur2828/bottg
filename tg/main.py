import asyncio

class AsyncContextManager:
    async def __aenter__(self):
        print("Entering async context")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Exiting async context")

async def use_async_context_manager():
    async with AsyncContextManager() as cm:
        print("Inside async context manager")

# Running the asyncio event loop
asyncio.run(use_async_context_manager())



async def async_data_generator():
    for i in range(5):
        yield i
        await asyncio.sleep(1)  # Simulate asynchronous operation

async def consume_async_data():
    async for value in async_data_generator():
        print(f"Received value asynchronously: {value}")

async def main():
    await consume_async_data()

if __name__ == "__main__":
    asyncio.run(main())