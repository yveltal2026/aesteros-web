import { test, expect } from "@playwright/test";

test.describe("Sitio comercial de Aesteros", () => {
  test("renderiza la portada, capítulos, laboratorio interactivo y formulario", async ({
    page,
  }) => {
    await page.goto("/");
    await expect(page).toHaveTitle(
      "Aesteros: neuromarketing en línea, con personas reales",
    );
    await expect(page.locator("#v-inicio h1")).toContainText("Percepción,");
    await expect(page.locator("#c-mirada h2")).toContainText("¿Qué miran?");
    await expect(page.locator("#c-asocia h2")).toContainText("¿Qué asocian?");
    await expect(page.locator("#c-precio h2")).toContainText("¿Qué opinan?");
    await expect(page.locator("#c-sellos h2")).toContainText(
      "Cada dato dice de dónde viene",
    );

    // Envío del formulario de demostración
    await page.locator("#f-nombre").fill("Cristian");
    await page.locator("#f-correo").fill("cristian@aesteros.com");
    await page.locator("#f-demo button[type='submit']").click();
    await expect(page.locator("#f-msg")).toContainText("Gracias, Cristian");
  });

  test("navega con direcciones propias por página (/producto, /metodo, /blog, /ayuda)", async ({
    page,
  }) => {
    await page.goto("/producto");
    await expect(page).toHaveTitle(
      "Cómo funciona un estudio de neuromarketing en Aesteros",
    );
    await expect(page.locator("#v-producto")).toBeVisible();
    await expect(page.locator("#v-producto h1")).toContainText("Un estudio,");

    await page.goto("/metodo");
    await expect(page).toHaveTitle(
      "Método: lo que Aesteros puede decir y lo que no",
    );
    await expect(page.locator("#v-metodo")).toBeVisible();

    await page.goto("/blog/como-leer-un-mapa-de-atencion");
    await expect(page).toHaveTitle(
      "Cómo leer un mapa de atención sin engañarte",
    );
    await expect(page.locator("#v-a-mapa")).toBeVisible();

    await page.goto("/ayuda/participar");
    await expect(page).toHaveTitle(
      "Voy a participar en un estudio: lo que conviene saber",
    );
    await expect(page.locator("#v-participar")).toBeVisible();
  });
});
