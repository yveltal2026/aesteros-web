import type { Metadata } from "next";
import { SiteShell } from "@/components/SiteShell";
import { buildViewMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildViewMetadata("privacidad");

export default function PrivacidadPage() {
  return <SiteShell initialView="privacidad" />;
}
