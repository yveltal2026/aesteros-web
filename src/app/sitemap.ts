import type { MetadataRoute } from "next";
import { VIEWS_META } from "@/lib/routes";
import { publicEnv } from "@/lib/env";

export default function sitemap(): MetadataRoute.Sitemap {
  const { siteUrl } = publicEnv();
  const base = siteUrl.replace(/\/+$/, "");

  return Object.values(VIEWS_META)
    .filter((meta) => !meta.noIndex)
    .map((meta) => ({
      url: `${base}${meta.path}`,
      lastModified: new Date(),
      changeFrequency: meta.mode === "main" ? "weekly" : "monthly",
      priority: meta.path === "/" ? 1.0 : meta.mode === "main" ? 0.9 : 0.7,
    }));
}
