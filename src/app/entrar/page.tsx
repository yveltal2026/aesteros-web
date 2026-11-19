import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("entrar");

export default function EntrarPage() {
  return <SiteShell initialView="entrar" />;
}
