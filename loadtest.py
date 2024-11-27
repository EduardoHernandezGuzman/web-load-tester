import asyncio
import time
import playwright.async_api as playwright

async def conectar_a_web(url, browser):  
    inicio = time.time()
    try:
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle") 
        fin = time.time()
        tiempo_respuesta = fin - inicio
        print(f"Conexión exitosa a {url}: Tiempo: {tiempo_respuesta:.2f}s")
        await page.close()
        return tiempo_respuesta
    except Exception as e:
        print(f"Error al conectar a {url}: {e}")
        return 0

async def simular_usuarios(url, num_usuarios):
    async with playwright.async_playwright() as p:
        browser = await p.chromium.launch() 
        tasks = [conectar_a_web(url, browser) for _ in range(num_usuarios)]
        tiempos_respuesta = await asyncio.gather(*tasks)
        await browser.close()  
        return tiempos_respuesta

async def main():
    url = input("Introduce la URL (incluyendo https://): ").strip()
    num_usuarios = int(input("Introduce el número de usuarios a simular: "))
    inicio = time.time()
    tiempos = await simular_usuarios(url, num_usuarios)
    fin = time.time()
    tiempo_total = fin - inicio

    tiempos_validos = [t for t in tiempos if t > 0]
    tiempo_promedio = sum(tiempos_validos) / len(tiempos_validos) if tiempos_validos else 0

    print(f"Tiempo total: {tiempo_total:.2f} segundos")
    print(f"Tiempo de respuesta promedio: {tiempo_promedio:.2f} segundos")

if __name__ == "__main__":
    asyncio.run(main())