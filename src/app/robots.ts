import type { MetadataRoute } from "next";
import { publicEnv } from "@/lib/env";

export default function robots(): MetadataRoute.Robots {
  const { siteUrl } = publicEnv();
  const base = siteUrl.replace(/\/+$/, "");

  return {
    rules: {
      userAgent: "*",
      allow: "/",
      disallow: ["/entrar", "/api/"],
    },
    sitemap: `${base}/sitemap.xml`,
  };
}
