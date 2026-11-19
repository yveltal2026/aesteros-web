import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("terminos");

export default function TerminosPage() {
  return <SiteShell initialView="terminos" />;
}
