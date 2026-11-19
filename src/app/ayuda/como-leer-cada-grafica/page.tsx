import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("guia-graficas");

export default function GuiaGraficasPage() {
  return <SiteShell initialView="guia-graficas" />;
}
