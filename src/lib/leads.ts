import { z } from "zod";

export const leadSchema = z.object({
  nombre: z
    .string()
    .trim()
    .min(1, "Falta tu nombre.")
    .max(160, "El nombre es demasiado largo."),
  correo: z
    .string()
    .trim()
    .regex(
      /^[^@\s]+@[^@\s]+\.[^@\s]+$/,
      "Revisa el correo: falta algo, como la arroba o el dominio.",
    )
    .max(254, "El correo es demasiado largo."),
  org: z.string().trim().max(200).optional().default(""),
  pregunta: z.string().trim().max(600).optional().default(""),
  tipo: z.enum(["u", "e"]).default("u"),
  espera: z.boolean().default(false),
});

export type LeadInput = z.infer<typeof leadSchema>;
