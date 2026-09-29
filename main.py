import logic.scrapper_all_ai as scrapper_all_ai
import asyncio

async def main():
    await scrapper_all_ai.nicotine_tracer()

if __name__ == '__main__':
   asyncio.run(main())