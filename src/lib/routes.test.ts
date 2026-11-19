import { describe, expect, it, beforeEach } from "vitest";
import { VIEWS_META, resolveViewFromPath } from "@/lib/routes";
import { leadSchema } from "@/lib/leads";
import { rateLimit, resetRateLimits } from "@/lib/rate-limit";
import viewsHtmlData from "@/lib/views-html.json";

describe("Rutas y metadatos SEO (buscadores.csv)", () => {
  it("define las 24 vistas del sitio comercial con sus rutas y títulos", () => {
    const views = Object.values(VIEWS_META);
    expect(views).toHaveLength(24);
    for (const v of views) {
      expect(v.title.length).toBeGreaterThan(5);
      expect(v.description.length).toBeGreaterThan(10);
      expect(v.path.startsWith("/")).toBe(true);
      expect((viewsHtmlData as Record<string, unknown>)[v.view]).toBeDefined();
    }
  });

  it("resuelve correctamente rutas limpias y con diagonal final", () => {
    expect(resolveViewFromPath("/")).toBe("inicio");
    expect(resolveViewFromPath("/producto")).toBe("producto");
    expect(resolveViewFromPath("/producto/")).toBe("producto");
    expect(resolveViewFromPath("/blog/como-leer-un-mapa-de-atencion")).toBe(
      "a-mapa",
    );
    expect(resolveViewFromPath("/ayuda/participar")).toBe("participar");
    expect(resolveViewFromPath("/ruta-inexistente")).toBe("inicio");
  });

  it("marca /entrar como noIndex para buscadores", () => {
    expect(VIEWS_META.entrar.noIndex).toBe(true);
    expect(VIEWS_META.inicio.noIndex).toBeUndefined();
  });
});

describe("Validación de formulario de demostración y lista de espera", () => {
  it("acepta una solicitud válida de demostración", () => {
    const res = leadSchema.safeParse({
      nombre: "María López",
      correo: "maria@universidad.edu.mx",
      org: "Universidad Nacional",
      pregunta: "¿Cómo enseño neuromarketing sin laboratorio?",
      tipo: "u",
      espera: false,
    });
    expect(res.success).toBe(true);
  });

  it("rechaza solicitudes sin nombre o con correo inválido con los mensajes de la guía de voz", () => {
    const noName = leadSchema.safeParse({
      nombre: "   ",
      correo: "maria@universidad.edu.mx",
    });
    expect(noName.success).toBe(false);
    if (!noName.success) {
      expect(noName.error.issues[0]?.message).toBe("Falta tu nombre.");
    }

    const badEmail = leadSchema.safeParse({
      nombre: "María",
      correo: "maria-sin-dominio",
    });
    expect(badEmail.success).toBe(false);
    if (!badEmail.success) {
      expect(badEmail.error.issues[0]?.message).toBe(
        "Revisa el correo: falta algo, como la arroba o el dominio.",
      );
    }
  });
});

describe("Limitador de peticiones (rateLimit)", () => {
  beforeEach(() => {
    resetRateLimits();
  });

  it("permite peticiones dentro de la ventana y bloquea al exceder", () => {
    expect(rateLimit("ip1", 2, 1000, 100).ok).toBe(true);
    expect(rateLimit("ip1", 2, 1000, 200).ok).toBe(true);
    const blocked = rateLimit("ip1", 2, 1000, 300);
    expect(blocked.ok).toBe(false);
    expect(blocked.retryAfterMs).toBe(800);
  });
});
