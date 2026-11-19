/**
 * Variables públicas (se inlinean en el cliente). Se leen con acceso estático
 * `process.env.NEXT_PUBLIC_*` para que Next las sustituya en el bundle.
 */
export function publicEnv() {
  return {
    supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL ?? "",
    supabaseAnonKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? "",
    siteUrl: process.env.NEXT_PUBLIC_SITE_URL ?? "https://aesteros.com",
    appUrl: process.env.NEXT_PUBLIC_APP_URL ?? "https://app.aesteros.com",
  };
}

export function isSupabaseServerConfigured(): boolean {
  const { supabaseUrl } = publicEnv();
  return Boolean(supabaseUrl && process.env.SUPABASE_SERVICE_ROLE_KEY);
}
