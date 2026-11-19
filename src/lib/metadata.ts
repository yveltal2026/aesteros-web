import type { Metadata } from "next";
import { VIEWS_META, type ViewId } from "@/lib/routes";
import { publicEnv } from "@/lib/env";

export function buildViewMetadata(viewId: ViewId): Metadata {
  const meta = VIEWS_META[viewId];
  const { siteUrl } = publicEnv();
  const canonicalUrl = `${siteUrl.replace(/\/+$/, "")}${meta.path}`;

  return {
    title: meta.title,
    description: meta.description,
    alternates: {
      canonical: canonicalUrl,
    },
    openGraph: {
      title: meta.title,
      description: meta.description,
      url: canonicalUrl,
      siteName: "Aesteros",
      locale: "es_MX",
      type: "website",
      images: [
        {
          url: "/img/hero.jpg",
          width: 1200,
          height: 700,
          alt: meta.title,
        },
      ],
    },
    twitter: {
      card: "summary_large_image",
      title: meta.title,
      description: meta.description,
      images: ["/img/hero.jpg"],
    },
    robots: meta.noIndex
      ? { index: false, follow: false }
      : { index: true, follow: true },
  };
}
