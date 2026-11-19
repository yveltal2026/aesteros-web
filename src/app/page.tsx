import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("inicio");

export default function InicioPage() {
  return <SiteShell initialView="inicio" />;
}
