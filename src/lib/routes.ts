export type ViewId =
  | "inicio"
  | "producto"
  | "metodo"
  | "universidades"
  | "agencias"
  | "empresas"
  | "planes"
  | "novedades"
  | "blog"
  | "a-mapa"
  | "a-asociacion"
  | "a-practica"
  | "a-brisa"
  | "a-sonrisa"
  | "a-margen"
  | "glosario"
  | "ayuda"
  | "participar"
  | "guia-graficas"
  | "guia-inicio"
  | "privacidad"
  | "terminos"
  | "camara"
  | "entrar";

export interface ViewMeta {
  view: ViewId;
  path: string;
  title: string;
  description: string;
  nav: string;
  mode: "main" | "mas";
  tone: "home" | "prod" | "met" | "dk" | "lt";
  noIndex?: boolean;
}

export const VIEWS_META: Record<ViewId, ViewMeta> = {
  inicio: {
    view: "inicio",
    path: "/",
    title: "Aesteros: neuromarketing en línea, con personas reales",
    description:
      "Mide qué miran, qué asocian y qué opinan de tu empaque, tu anuncio o tu sitio. Cada dato dice de dónde viene y qué tan firme es.",
    nav: "inicio",
    mode: "main",
    tone: "home",
  },
  producto: {
    view: "producto",
    path: "/producto",
    title: "Cómo funciona un estudio de neuromarketing en Aesteros",
    description:
      "Sigue un estudio de principio a fin: armar, invitar, medir, leer y decidir. Nueve herramientas en una sola plataforma.",
    nav: "producto",
    mode: "main",
    tone: "prod",
  },
  metodo: {
    view: "metodo",
    path: "/metodo",
    title: "Método: lo que Aesteros puede decir y lo que no",
    description:
      "Qué mide cada prueba, con qué referencia y hasta dónde llega. El recorrido de un dato, de la cámara al informe.",
    nav: "metodo",
    mode: "main",
    tone: "met",
  },
  universidades: {
    view: "universidades",
    path: "/universidades",
    title: "Laboratorio de neuromarketing para universidades",
    description:
      "Tus alumnos diseñan un estudio, lo aplican con personas reales y leen sus resultados en un semestre. Sin comprar equipo.",
    nav: "universidades",
    mode: "mas",
    tone: "dk",
  },
  agencias: {
    view: "agencias",
    path: "/agencias",
    title: "Pruebas de creatividad para agencias, con evidencia",
    description:
      "Prueba tus rutas creativas con el público del cliente y presenta con datos. Informes con tu marca.",
    nav: "agencias",
    mode: "mas",
    tone: "dk",
  },
  empresas: {
    view: "empresas",
    path: "/empresas",
    title: "Prueba tu empaque, anuncio o precio antes de producir",
    description:
      "Sabe cuál versión funciona con personas reales: qué se ve, qué se asocia y cuánto pagarían.",
    nav: "empresas",
    mode: "mas",
    tone: "dk",
  },
  planes: {
    view: "planes",
    path: "/planes",
    title: "Planes de Aesteros: Campus, Pro y Lite",
    description:
      "Tres ediciones sobre un mismo núcleo. Qué incluye cada una y cómo se cobra. Pide tu cotización.",
    nav: "planes",
    mode: "mas",
    tone: "lt",
  },
  novedades: {
    view: "novedades",
    path: "/novedades",
    title: "Novedades de Aesteros",
    description:
      "Las herramientas disponibles y las que vienen. Cada lanzamiento se anuncia aquí.",
    nav: "novedades",
    mode: "mas",
    tone: "lt",
  },
  blog: {
    view: "blog",
    path: "/blog",
    title: "Blog de Aesteros: leer la percepción, con calma",
    description:
      "Método, práctica de clase y casos de neuromarketing, escritos para entenderse sin formación técnica.",
    nav: "blog",
    mode: "mas",
    tone: "lt",
  },
  "a-mapa": {
    view: "a-mapa",
    path: "/blog/como-leer-un-mapa-de-atencion",
    title: "Cómo leer un mapa de atención sin engañarte",
    description:
      "Tres preguntas antes de creerle a un mapa de calor: cuánta gente hay detrás, qué tan grande es el área y si mirar es entender.",
    nav: "blog",
    mode: "mas",
    tone: "lt",
  },
  "a-asociacion": {
    view: "a-asociacion",
    path: "/blog/que-mide-una-prueba-de-asociacion-implicita",
    title: "Qué mide una prueba de asociación implícita",
    description:
      "No mide lo que la gente opina de tu marca: mide qué tan rápido la une con una idea. Qué dice, qué no dice y cómo usarla.",
    nav: "blog",
    mode: "mas",
    tone: "lt",
  },
  "a-practica": {
    view: "a-practica",
    path: "/blog/practica-de-neuromarketing-cuatro-semanas",
    title: "Una práctica de neuromarketing para cuatro semanas",
    description:
      "Un guion para que cada equipo pase de una pregunta a una conclusión con datos propios, sin laboratorio.",
    nav: "blog",
    mode: "mas",
    tone: "lt",
  },
  "a-brisa": {
    view: "a-brisa",
    path: "/blog/caso-brisa-un-anuncio-tres-medidas",
    title: "Un anuncio, tres medidas: el caso de Brisa",
    description:
      "Un caso de ejemplo: cómo el seguimiento ocular, la asociación implícita y las preguntas de precio cambian una decisión.",
    nav: "blog",
    mode: "mas",
    tone: "lt",
  },
  "a-sonrisa": {
    view: "a-sonrisa",
    path: "/blog/una-sonrisa-no-es-una-emocion",
    title: "Una sonrisa no es una emoción",
    description:
      "La cámara dice qué hizo una cara en cada segundo, no qué sintió la persona. Para qué sirve y cómo leerlo.",
    nav: "blog",
    mode: "mas",
    tone: "lt",
  },
  "a-margen": {
    view: "a-margen",
    path: "/blog/margen-de-error-con-una-grafica",
    title: "Margen de error, explicado con una sola gráfica",
    description:
      "Todo resultado es una cifra y una franja. Cómo leer la franja y qué significa que toque el cero.",
    nav: "blog",
    mode: "mas",
    tone: "lt",
  },
  glosario: {
    view: "glosario",
    path: "/glosario",
    title: "Glosario de neuromarketing en español llano",
    description:
      "Área de interés, intervalo de confianza, mapa de atención y más términos, explicados en una o dos frases.",
    nav: "blog",
    mode: "mas",
    tone: "lt",
  },
  ayuda: {
    view: "ayuda",
    path: "/ayuda",
    title: "Centro de ayuda de Aesteros",
    description:
      "Guías para quien investiga, quien administra la cuenta y quien participa en un estudio.",
    nav: "ayuda",
    mode: "mas",
    tone: "lt",
  },
  participar: {
    view: "participar",
    path: "/ayuda/participar",
    title: "Voy a participar en un estudio: lo que conviene saber",
    description:
      "Qué se mide, qué se guarda de tu cámara, cómo calibrarla y qué hacer si no funciona.",
    nav: "ayuda",
    mode: "mas",
    tone: "lt",
  },
  "guia-graficas": {
    view: "guia-graficas",
    path: "/ayuda/como-leer-cada-grafica",
    title: "Cómo leer cada gráfica",
    description:
      "Cinco gráficas de Aesteros: qué mirar primero en cada una y qué no concluir.",
    nav: "ayuda",
    mode: "mas",
    tone: "lt",
  },
  "guia-inicio": {
    view: "guia-inicio",
    path: "/ayuda/tu-primer-estudio",
    title: "Tu primer estudio, en cinco pasos",
    description:
      "De subir tu pieza a leer el informe, con una imagen por paso.",
    nav: "ayuda",
    mode: "mas",
    tone: "lt",
  },
  privacidad: {
    view: "privacidad",
    path: "/privacidad",
    title: "Aviso de privacidad de Aesteros",
    description:
      "Qué datos tratamos, para qué y cómo ejercer tus derechos.",
    nav: "legal",
    mode: "mas",
    tone: "lt",
  },
  terminos: {
    view: "terminos",
    path: "/terminos",
    title: "Términos del servicio de Aesteros",
    description: "Las reglas para usar la plataforma.",
    nav: "legal",
    mode: "mas",
    tone: "lt",
  },
  camara: {
    view: "camara",
    path: "/camara",
    title: "Cómo usa Aesteros la cámara",
    description:
      "El video no sale de tu equipo: solo coordenadas y tiempos. Explicado sin letra chica.",
    nav: "legal",
    mode: "mas",
    tone: "lt",
  },
  entrar: {
    view: "entrar",
    path: "/entrar",
    title: "Entrar a Aesteros",
    description:
      "Acceso para docentes, alumnos e investigadores. Sin indexar.",
    nav: "entrar",
    mode: "mas",
    tone: "dk",
    noIndex: true,
  },
};

export const PATH_TO_VIEW: Record<string, ViewId> = Object.fromEntries(
  Object.values(VIEWS_META).map((m) => [m.path, m.view]),
) as Record<string, ViewId>;

export function resolveViewFromPath(pathname: string): ViewId {
  const clean = pathname === "/" ? "/" : pathname.replace(/\/+$/, "");
  return PATH_TO_VIEW[clean] ?? "inicio";
}
