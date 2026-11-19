import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("novedades");

export default function NovedadesPage() {
  return <SiteShell initialView="novedades" />;
}
