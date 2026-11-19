import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("empresas");

export default function EmpresasPage() {
  return <SiteShell initialView="empresas" />;
}
