"use client";

import React, { useEffect, useRef } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { Logo } from "@/components/Logo";
import { VIEWS_META, resolveViewFromPath, type ViewId } from "@/lib/routes";
import viewsHtmlData from "@/lib/views-html.json";
import curvasData from "@/lib/curvas.json";

const VIEWS_HTML = viewsHtmlData as Record<
  ViewId,
  { className: string; html: string }
>;

const CURV = curvasData as Record<string, number[][]>;

interface AesterosRuntime {
  blip?: (name: string) => void;
  tone?: (f: number) => void;
  tline?: () => void;
  pill?: (anim: boolean) => void;
  view?: (name: string) => void;
  on?: number;
  dbg?: { raw: number[]; p: number[] };
}

declare global {
  interface Window {
    AE?: AesterosRuntime;
  }
}

export function SiteShell({ initialView }: { initialView: ViewId }) {
  const pathname = usePathname();
  const router = useRouter();
  const currentView: ViewId = pathname
    ? resolveViewFromPath(pathname)
    : initialView;

  const initializedRef = useRef(false);

  // Synchronize currentView to DOM attributes, hidden states, and animations
  useEffect(() => {
    const root = document.documentElement;
    const meta = VIEWS_META[currentView] ?? VIEWS_META.inicio;

    root.dataset.view = currentView;
    root.dataset.mode = meta.mode;

    // Show active view, hide others
    (Object.keys(VIEWS_META) as ViewId[]).forEach((v) => {
      const el = document.getElementById(`v-${v}`);
      if (el) {
        el.hidden = v !== currentView;
      }
    });

    // Update dock aria-current
    const curNav = meta.nav;
    document.querySelectorAll<HTMLAnchorElement>(".dock nav a").forEach((a) => {
      if (a.dataset.v === curNav) {
        a.setAttribute("aria-current", "page");
      } else {
        a.removeAttribute("aria-current");
      }
    });

    // Update sheet aria-current and "more" button state
    const mb = document.getElementById("more");
    if (mb) {
      mb.classList.toggle("here", meta.mode === "mas");
    }
    document.querySelectorAll<HTMLAnchorElement>("#sheet a").forEach((a) => {
      const href = a.getAttribute("href");
      const navMeta =
        VIEWS_META[curNav as ViewId] ?? VIEWS_META[currentView];
      if (href && navMeta && href === navMeta.path) {
        a.setAttribute("aria-current", "page");
      } else {
        a.removeAttribute("aria-current");
      }
    });

    // Close sheet if open
    const sh = document.getElementById("sheet");
    if (sh && !sh.hidden) {
      sh.hidden = true;
      mb?.setAttribute("aria-expanded", "false");
    }

    // Handle hash / data-go target scrolling
    const hashTarget = window.location.hash
      ? window.location.hash.slice(1)
      : "";
    const targetEl = hashTarget ? document.getElementById(hashTarget) : null;
    if (targetEl) {
      if (targetEl.tagName === "DETAILS") {
        (targetEl as HTMLDetailsElement).open = true;
      }
      targetEl.scrollIntoView({ block: "start", behavior: "instant" });
      if (hashTarget === "espera") {
        const c = document.getElementById(
          "f-espera",
        ) as HTMLInputElement | null;
        if (c) c.checked = true;
      }
    } else {
      window.scrollTo({ top: 0, behavior: "instant" });
    }

    // Notify runtime & move pill
    if (window.AE?.view) {
      window.AE.view(currentView);
    }
    if (window.AE?.pill) {
      requestAnimationFrame(() => {
        window.AE?.pill?.(true);
      });
    }
  }, [currentView]);

  // Initialize interactive engines once on mount
  useEffect(() => {
    if (initializedRef.current) return;
    initializedRef.current = true;

    const AE: AesterosRuntime = (window.AE = window.AE || {});
    const root = document.documentElement;
    const $ = <T extends Element = HTMLElement>(
      s: string,
      c?: ParentNode | null,
    ) => (c || document).querySelector<T>(s);
    const $$ = <T extends Element = HTMLElement>(
      s: string,
      c?: ParentNode | null,
    ) => Array.from((c || document).querySelectorAll<T>(s));

    const reduce = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;
    const finePtr = window.matchMedia(
      "(hover:hover) and (pointer:fine)",
    ).matches;
    const small = () => window.innerWidth <= 820;
    const clamp = (x: number) => (x < 0 ? 0 : x > 1 ? 1 : x);
    const ease = (x: number) => {
      const c = clamp(x);
      return c * c * (3 - 2 * c);
    };

    const CH = [
      "c-hero",
      "c-mirada",
      "c-asocia",
      "c-precio",
      "c-sellos",
    ].map((i) => document.getElementById(i)!);
    const P = [0, 0, 0, 0, 0];
    const PR = [0, 0, 0, 0, 0];
    let view: string = root.dataset.view || "inicio";

    function prog(el: HTMLElement | null) {
      if (!el) return 0;
      const r = el.getBoundingClientRect();
      const t = r.height - window.innerHeight;
      return t > 0 ? clamp(-r.top / t) : 0;
    }

    /* ---------- Intercept internal link clicks for smooth Next.js routing + data-go ---------- */
    const handleDocClick = (e: MouseEvent) => {
      const target = e.target as Element | null;
      const a = target?.closest<HTMLAnchorElement>("a[href]");
      if (!a) return;
      const href = a.getAttribute("href") || "";
      if (href === "#contenido") return;
      if (a.classList.contains("wip")) {
        e.preventDefault();
        return;
      }
      if (href.startsWith("/")) {
        e.preventDefault();
        const [pathPart, hashPart] = href.split("#");
        const targetPath = pathPart || "/";
        const goTarget = a.dataset.go || hashPart || "";

        if (targetPath === window.location.pathname) {
          if (goTarget) {
            window.history.replaceState(null, "", `${targetPath}#${goTarget}`);
            const el = document.getElementById(goTarget);
            if (el) {
              if (el.tagName === "DETAILS") {
                (el as HTMLDetailsElement).open = true;
              }
              el.scrollIntoView({ block: "start", behavior: "instant" });
              if (goTarget === "espera") {
                const c = document.getElementById(
                  "f-espera",
                ) as HTMLInputElement | null;
                if (c) c.checked = true;
              }
            }
          } else {
            window.scrollTo({ top: 0, behavior: "smooth" });
          }
        } else {
          const fullDest = goTarget ? `${targetPath}#${goTarget}` : targetPath;
          router.push(fullDest);
        }
      }
    };
    document.addEventListener("click", handleDocClick);

    /* ---------- Formulario de demostración y lista de espera ---------- */
    const fDemo = document.getElementById("f-demo") as HTMLFormElement | null;
    if (fDemo) {
      fDemo.addEventListener("submit", async (e) => {
        e.preventDefault();
        const m = document.getElementById("f-msg");
        const n = document.getElementById(
          "f-nombre",
        ) as HTMLInputElement | null;
        const c = document.getElementById(
          "f-correo",
        ) as HTMLInputElement | null;
        const org = document.getElementById(
          "f-org",
        ) as HTMLInputElement | null;
        const preg = document.getElementById(
          "f-preg",
        ) as HTMLInputElement | null;
        const espera = document.getElementById(
          "f-espera",
        ) as HTMLInputElement | null;
        const t2 = document.getElementById("f-t2") as HTMLInputElement | null;

        if (!m || !n || !c) return;
        if (!n.value.trim()) {
          m.textContent = "Falta tu nombre.";
          n.focus();
          return;
        }
        if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(c.value.trim())) {
          m.textContent =
            "Revisa el correo: falta algo, como la arroba o el dominio.";
          c.focus();
          return;
        }

        m.textContent = "Enviando…";
        try {
          const res = await fetch("/api/leads", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              nombre: n.value.trim(),
              correo: c.value.trim(),
              org: org?.value.trim() ?? "",
              pregunta: preg?.value.trim() ?? "",
              tipo: t2?.checked ? "e" : "u",
              espera: Boolean(espera?.checked),
            }),
          });
          const data = await res.json();
          if (!res.ok || !data.ok) {
            m.textContent =
              data.error ||
              "No pudimos registrar tu solicitud. Inténtalo de nuevo.";
            return;
          }
          m.textContent = data.message;
          AE.blip?.("ok");
        } catch {
          m.textContent =
            "Recibimos tu solicitud en esta sesión. Pronto nos pondremos en contacto.";
        }
      });
    }

    /* ---------- Pruebas en miniatura (Pruébalo tú) ---------- */
    (function initHeatmapDemo() {
      const wrap = $<HTMLElement>("#demo-heat .canvas-wrap");
      const cv = $<HTMLCanvasElement>("#heat");
      const go = $<HTMLButtonElement>("#heat-go");
      const bar = $<HTMLElement>("#heat-bar");
      const out = $<HTMLElement>("#heat-out");
      if (!wrap || !cv || !go || !bar || !out) return;

      const W = 64;
      const H = 40;
      const g = cv.getContext("2d");
      if (!g) return;
      let I = new Float32Array(W * H);
      let run = false;
      let px = -1;
      let py = -1;
      let t0 = 0;
      let last = 0;
      let aoi = { t: 0, v: [0, 0, 0, 0, 0] };
      const A: [string, number, number, number, number][] = [
        ["el titular", 0.04, 0.2, 0.45, 0.57],
        ["el producto", 0.72, 0.07, 0.93, 0.93],
        ["el botón", 0.04, 0.63, 0.32, 0.8],
        ["el precio", 0.52, 0.62, 0.66, 0.85],
        ["el logotipo", 0.04, 0.04, 0.18, 0.15],
      ];
      cv.width = W;
      cv.height = H;

      function paint() {
        const im = g!.createImageData(W, H);
        const d = im.data;
        let m = 0.3;
        for (let i = 0; i < I.length; i++) if (I[i] > m) m = I[i];
        for (let i = 0; i < I.length; i++) {
          const n = Math.min(1, I[i] / m);
          const k = Math.min(1, n * 1.6);
          d[i * 4] = 20 + 235 * k;
          d[i * 4 + 1] = 17 + 159 * k;
          d[i * 4 + 2] = 12 - 12 * k;
          d[i * 4 + 3] = 255 * (0.64 - 0.5 * n);
        }
        g!.putImageData(im, 0, 0);
      }

      function move(e: PointerEvent) {
        const r = wrap!.getBoundingClientRect();
        px = (e.clientX - r.left) / r.width;
        py = (e.clientY - r.top) / r.height;
      }

      function end() {
        run = false;
        wrap!.classList.remove("run");
        go!.textContent = "Repetir";
        go!.hidden = false;
        if (aoi.t < 0.4) {
          out!.textContent =
            "No detectamos movimiento sobre el anuncio. Inténtalo otra vez.";
          return;
        }
        const o = A.map((a, k) => [
          a[0],
          Math.round((aoi.v[k] / aoi.t) * 100),
        ] as [string, number]).sort((a, b) => b[1] - a[1]);
        const tx =
          o[0][1] > 0
            ? `Tu cursor pasó más tiempo en <b>${o[0][0]} (${o[0][1]} %)</b>${
                o[1][1] > 0 ? ` y en ${o[1][0]} (${o[1][1]} %)` : ""
              }.`
            : "Tu cursor casi no tocó las áreas del anuncio.";
        out!.innerHTML = `${tx} En el estudio de ejemplo, la mirada de 52 personas fue primero al titular. Aquí seguimos tu cursor; en un estudio real, la cámara estima la mirada.`;
        AE.blip?.("ok");
      }

      function tick(now: number) {
        if (!run) return;
        const dt = Math.min(0.05, (now - last) / 1000);
        last = now;
        const el = (now - t0) / 5000;
        if (px >= 0 && px <= 1 && py >= 0 && py <= 1) {
          const cx = px * W;
          const cy = py * H;
          for (
            let y = Math.max(0, (cy - 7) | 0);
            y < Math.min(H, cy + 8);
            y++
          ) {
            for (
              let x = Math.max(0, (cx - 7) | 0);
              x < Math.min(W, cx + 8);
              x++
            ) {
              const q =
                ((x + 0.5 - cx) * (x + 0.5 - cx) +
                  (y + 0.5 - cy) * (y + 0.5 - cy)) /
                14;
              I[y * W + x] += dt * Math.exp(-q);
            }
          }
          aoi.t += dt;
          A.forEach((a, k) => {
            if (px >= a[1] && px <= a[3] && py >= a[2] && py <= a[4]) {
              aoi.v[k] += dt;
            }
          });
        }
        paint();
        bar!.style.width = `${Math.min(100, el * 100)}%`;
        if (el >= 1) {
          end();
          return;
        }
        requestAnimationFrame(tick);
      }

      go.addEventListener("click", () => {
        I = new Float32Array(W * H);
        aoi = { t: 0, v: [0, 0, 0, 0, 0] };
        px = py = -1;
        run = true;
        go.hidden = true;
        wrap.classList.add("run");
        out.textContent = "Muévete sobre el anuncio…";
        t0 = last = performance.now();
        requestAnimationFrame(tick);
      });
      wrap.addEventListener("pointermove", move);
      wrap.addEventListener("pointerdown", move);
    })();

    (function initReactionTimeDemo() {
      const word = $<HTMLElement>("#rt-word");
      const L = $<HTMLButtonElement>("#rt-l");
      const R = $<HTMLButtonElement>("#rt-r");
      const go = $<HTMLButtonElement>("#rt-go");
      const bar = $<HTMLElement>("#rt-bar");
      const out = $<HTMLElement>("#rt-out");
      if (!word || !L || !R || !go || !bar || !out) return;

      const base: [string, number][] = [
        ["Fresca", 0],
        ["Pura", 0],
        ["Química", 1],
        ["Limpia", 0],
        ["Sintética", 1],
        ["Viva", 0],
      ];
      let q: [string, number][] = [];
      let i = 0;
      let t0 = 0;
      let rts: number[] = [];
      let err = 0;
      let on = false;
      let wait = false;

      function end() {
        on = false;
        L!.disabled = R!.disabled = true;
        go!.hidden = false;
        go!.textContent = "Repetir";
        word!.className = "rt-word";
        word!.textContent = "Listo";
        if (!rts.length) {
          out!.textContent =
            "Ninguna respuesta correcta esta vez. Inténtalo otra vez.";
          return;
        }
        const m = Math.round(rts.reduce((a, b) => a + b, 0) / rts.length);
        out!.innerHTML = `Tu promedio: <b>${m} ms</b> en ${rts.length} respuestas${
          err ? `, con ${err}${err > 1 ? " errores" : " error"}` : ""
        }. Una prueba completa junta cientos de respuestas como estas, y de la diferencia entre tiempos sale la fuerza de la asociación.`;
        AE.blip?.("ok");
      }

      function next() {
        if (i >= q.length) {
          end();
          return;
        }
        wait = true;
        word!.className = "rt-word";
        word!.textContent = "+";
        setTimeout(
          () => {
            if (!on) return;
            word!.textContent = q[i][0];
            wait = false;
            t0 = performance.now();
          },
          520 + Math.random() * 380,
        );
      }

      function ans(side: number) {
        if (!on || wait) return;
        const rt = performance.now() - t0;
        wait = true;
        if (side === q[i][1]) {
          rts.push(rt);
          i++;
          bar!.style.width = `${(i / q.length) * 100}%`;
          next();
        } else {
          err++;
          word!.className = "rt-word bad";
          word!.textContent = "×";
          i++;
          bar!.style.width = `${(i / q.length) * 100}%`;
          setTimeout(next, 480);
        }
      }

      go.addEventListener("click", () => {
        q = base.slice().sort(() => Math.random() - 0.5);
        i = 0;
        rts = [];
        err = 0;
        on = true;
        go.hidden = true;
        L.disabled = R.disabled = false;
        bar.style.width = "0";
        out.textContent = "Responde lo más rápido que puedas.";
        next();
      });
      L.addEventListener("click", () => ans(0));
      R.addEventListener("click", () => ans(1));
      document.addEventListener("keydown", (e) => {
        if (!on || e.metaKey || e.ctrlKey || e.altKey) return;
        const k = e.key.toLowerCase();
        if (k === "e") {
          e.preventDefault();
          ans(0);
        } else if (k === "i") {
          e.preventDefault();
          ans(1);
        }
      });
    })();

    /* ---------- Sonido opcional: lo borroso suena filtrado y se abre al enfocar ---------- */
    (function initSound() {
      const b = $<HTMLButtonElement>("#snd");
      if (!b) return;
      const lab = $<HTMLElement>("span", b);
      let ctx: AudioContext | null = null;
      let filt: BiquadFilterNode | null = null;
      let master: GainNode | null = null;
      const buf: Record<string, AudioBuffer> = {};
      let ready = false;
      let on = false;

      function load(n: string) {
        return fetch(`/snd/${n}.mp3`)
          .then((r) => {
            if (!r.ok) throw new Error("audio fetch error");
            return r.arrayBuffer();
          })
          .then(
            (a) =>
              new Promise<AudioBuffer>((ok, no) => {
                ctx!.decodeAudioData(a, ok, no);
              }),
          )
          .then((d) => {
            buf[n] = d;
          });
      }

      function play(n: string, g?: number) {
        if (!on || !buf[n] || !ctx || !master) return;
        const s = ctx.createBufferSource();
        const v = ctx.createGain();
        s.buffer = buf[n];
        v.gain.value = g || 0.5;
        s.connect(v);
        v.connect(master);
        s.start();
      }

      AE.blip = (n: string) => play(n, 0.45);
      AE.tone = (f: number) => {
        if (on && filt && ctx) {
          filt.frequency.setTargetAtTime(
            750 * Math.pow(24, clamp(f)),
            ctx.currentTime,
            0.25,
          );
        }
      };

      let want = true;
      let started = false;
      try {
        if (localStorage.getItem("ae-snd") === "0") want = false;
      } catch {}

      function fail() {
        on = false;
        want = false;
        b!.setAttribute("aria-pressed", "false");
        b!.disabled = true;
        if (lab) lab.textContent = "Sin sonido aquí";
        b!.title = "El sonido no está disponible en este visor";
      }

      function mark() {
        b!.setAttribute("aria-pressed", want ? "true" : "false");
      }

      function go() {
        on = want;
        if (started) return;
        started = true;
        if (!ready) {
          ready = true;
          Promise.all(["base", "foco", "sello", "logo", "ok", "menu"].map(load))
            .then(() => {
              if (!ctx || !filt) return;
              play("logo", 0.85);
              const s = ctx.createBufferSource();
              const v = ctx.createGain();
              const t0 = ctx.currentTime + 2.6;
              s.buffer = buf.base;
              s.loop = true;
              v.gain.setValueAtTime(0, ctx.currentTime);
              v.gain.setValueAtTime(0, t0);
              v.gain.linearRampToValueAtTime(0.4, t0 + 3.5);
              s.connect(v);
              v.connect(filt);
              s.start(t0);
            })
            .catch(fail);
        }
      }

      function start() {
        if (!want) return;
        try {
          if (!ctx) {
            const C =
              window.AudioContext ||
              (window as unknown as { webkitAudioContext: typeof AudioContext })
                .webkitAudioContext;
            ctx = new C();
            master = ctx.createGain();
            master.gain.value = 0.8;
            master.connect(ctx.destination);
            filt = ctx.createBiquadFilter();
            filt.type = "lowpass";
            filt.frequency.value = 900;
            filt.Q.value = 0.3;
            filt.connect(master);
          }
          const p = ctx.resume();
          if (p && p.catch) p.catch(() => {});
          if (ctx.state !== "running" && !started) {
            setTimeout(() => {
              if (ctx && ctx.state === "running") go();
            }, 250);
          } else {
            go();
          }
        } catch {
          fail();
        }
      }

      function first(e: Event) {
        const target = e.target as Element | null;
        if (target?.closest && target.closest("#snd")) return;
        start();
      }

      ["pointerdown", "touchend", "keydown", "click"].forEach((n) => {
        window.addEventListener(n, first, { passive: true });
      });
      mark();
      start();

      b.addEventListener("click", () => {
        want = !want;
        mark();
        try {
          localStorage.setItem("ae-snd", want ? "1" : "0");
        } catch {}
        if (!want) {
          on = false;
          if (ctx) ctx.suspend();
          return;
        }
        start();
        if (ctx && started) {
          on = true;
          ctx.resume();
        }
      });
    })();

    /* ---------- Cursor propio: un punto difuso sobre lo interactivo ---------- */
    if (finePtr && !reduce) {
      const c = $<HTMLElement>("#cur");
      if (c) {
        let x = 0,
          y = 0,
          tx = 0,
          ty = 0,
          sc = 0.22,
          ts = 0.22,
          op = 0,
          seen = false;
        root.classList.add("hascur");
        window.addEventListener(
          "pointermove",
          (e) => {
            tx = e.clientX;
            ty = e.clientY;
            if (!seen) {
              seen = true;
              x = tx;
              y = ty;
            }
            op = 1;
            const target = e.target as Element | null;
            ts =
              target?.closest &&
              target.closest("a,button,input,label,.canvas-wrap")
                ? 1
                : 0.22;
          },
          { passive: true },
        );
        document.addEventListener("pointerleave", () => {
          op = 0;
        });
        (function loop() {
          x += (tx - x) * 0.22;
          y += (ty - y) * 0.22;
          sc += (ts - sc) * 0.16;
          c.style.transform = `translate3d(${x}px,${y}px,0) scale(${sc})`;
          c.style.opacity = String(op * (sc > 0.5 ? 0.8 : 1));
          requestAnimationFrame(loop);
        })();
      }
    }

    /* ---------- Antes y después, y la pregunta que se enfoca ---------- */
    (function initBeforeAfterAndAsk() {
      const tabs = $$<HTMLButtonElement>(".ba-tabs [role=tab]");
      function pick(t: HTMLButtonElement, f?: boolean) {
        tabs.forEach((x) => {
          const on = x === t;
          x.setAttribute("aria-selected", on ? "true" : "false");
          x.tabIndex = on ? 0 : -1;
          const ctrl = x.getAttribute("aria-controls");
          const p = ctrl ? document.getElementById(ctrl) : null;
          if (p) {
            p.hidden = !on;
            if (on) {
              p.classList.remove("go");
              void p.offsetWidth;
              p.classList.add("go");
            }
          }
        });
        if (f) t.focus();
      }
      tabs.forEach((t, i) => {
        t.addEventListener("click", () => pick(t));
        t.addEventListener("keydown", (e) => {
          if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
            e.preventDefault();
            pick(
              tabs[
                (i + (e.key === "ArrowRight" ? 1 : tabs.length - 1)) %
                  tabs.length
              ],
              true,
            );
          }
        });
      });

      const sq = $<HTMLElement>("#sq");
      const st = $<HTMLElement>(".stage");
      const inp = $<HTMLInputElement>("#f-preg");
      const chips = $$<HTMLButtonElement>(".ask .chip");
      let tm: ReturnType<typeof setTimeout>;
      if (!sq || !st || !inp) return;

      function show(q: string, fromInput?: boolean) {
        const text = q || "Elige una pregunta o escribe la tuya.";
        sq!.textContent = text;
        sq!.classList.remove("foc");
        st!.classList.remove("foc");
        void sq!.offsetWidth;
        clearTimeout(tm);
        tm = setTimeout(
          () => {
            sq!.classList.add("foc");
            st!.classList.add("foc");
          },
          fromInput ? 260 : 60,
        );
      }
      chips.forEach((c) => {
        c.addEventListener("click", () => {
          chips.forEach((x) =>
            x.setAttribute("aria-pressed", x === c ? "true" : "false"),
          );
          inp.value = c.textContent || "";
          show(c.textContent || "");
          AE.blip?.("foco");
        });
      });
      inp.addEventListener("input", () => {
        chips.forEach((x) => x.setAttribute("aria-pressed", "false"));
        show(inp.value.trim(), true);
      });
      st.classList.add("foc");
    })();

    /* ---------- Producto y Método: función ---------- */
    (function initProductoAndMetodo() {
      const pv = $<HTMLElement>("#v-producto");
      if (!pv) return;

      const rv = $$<HTMLElement>("[data-rv]");
      if ("IntersectionObserver" in window && !reduce) {
        const io = new IntersectionObserver(
          (es) => {
            es.forEach((e) => {
              if (e.isIntersecting) {
                e.target.classList.add("in");
                io.unobserve(e.target);
              }
            });
          },
          { rootMargin: "0px 0px -10% 0px", threshold: 0.08 },
        );
        rv.forEach((e) => io.observe(e));
      } else {
        rv.forEach((e) => e.classList.add("in"));
      }

      // audiencia
      $$<HTMLButtonElement>(".ausel button").forEach((b) => {
        b.addEventListener("click", () => {
          pv.dataset.au = b.dataset.set;
          $$<HTMLButtonElement>(".ausel button").forEach((x) =>
            x.setAttribute("aria-pressed", x === b ? "true" : "false"),
          );
        });
      });

      // riel de pasos
      const rb = $$<HTMLButtonElement>(".rail button");
      const sp = $$<HTMLElement>(".sp");
      rb.forEach((b) => {
        b.addEventListener("click", () => {
          const to = b.dataset.to;
          if (to) {
            document.getElementById(to)?.scrollIntoView({
              behavior: reduce ? "auto" : "smooth",
              block: "start",
            });
          }
        });
      });
      if ("IntersectionObserver" in window) {
        const so = new IntersectionObserver(
          (es) => {
            es.forEach((e) => {
              if (e.isIntersecting) {
                rb.forEach((b) => {
                  if (b.dataset.to === e.target.id) {
                    b.setAttribute("aria-current", "step");
                  } else {
                    b.removeAttribute("aria-current");
                  }
                });
              }
            });
          },
          { rootMargin: "-45% 0px -50% 0px" },
        );
        sp.forEach((e) => so.observe(e));
      }

      // áreas de interés
      const AO = [
        ["52 %", "94 %", "0,6 s", "1,8 s"],
        ["24 %", "81 %", "1,1 s", "1,2 s"],
        ["12 %", "46 %", "2,4 s", "0,5 s"],
        ["5 %", "22 %", "3,1 s", "0,3 s"],
      ];
      const dd = $$<HTMLElement>("#aoi-out dd");
      const ab = $$<HTMLButtonElement>(".aoi");
      function aoi(b: HTMLButtonElement) {
        ab.forEach((x) =>
          x.setAttribute("aria-pressed", x === b ? "true" : "false"),
        );
        const idx = Number(b.dataset.k || 0);
        AO[idx]?.forEach((v, i) => {
          if (dd[i]) dd[i].textContent = v;
        });
      }
      ab.forEach((b) => {
        b.addEventListener("click", () => aoi(b));
        b.addEventListener("pointerenter", (e) => {
          if (e.pointerType === "mouse") aoi(b);
        });
        b.addEventListener("focus", () => aoi(b));
      });

      // grupos de la asociación
      const G: [number, number, number, number, string][] = [
        [0.58, 0.41, 0.75, 52, "Todos"],
        [0.81, 0.58, 1.04, 21, "Quienes ya compran Brisa"],
        [0.42, 0.2, 0.64, 31, "Quienes no la compran"],
      ];
      const df = $<HTMLElement>("#d-fill");
      const db = $<HTMLElement>("#d-band");
      const dt = $<HTMLElement>("#d-dot");
      const dout = $<HTMLElement>("#d-out");
      const gb = $$<HTMLButtonElement>(".grp button");
      const nx = (v: number) => 30 + (v / 1.2) * 70;
      const nf = (v: number) => v.toFixed(2).replace(".", ",");
      function grp(k: number) {
        const g = G[k];
        if (!df || !db || !dt || !dout || !g) return;
        df.style.width = `${nx(g[0]) - 30}%`;
        db.style.left = `${nx(g[1]) - 4}%`;
        db.style.width = `${nx(g[2]) - nx(g[1]) + 8}%`;
        dt.style.left = `${nx(g[0])}%`;
        dout.innerHTML = `<b>+${nf(g[0])}</b>${g[4]}: Brisa se asocia con «natural». Intervalo de ${nf(g[1])} a ${nf(g[2])}, con ${g[3]} personas.`;
        gb.forEach((x, i) =>
          x.setAttribute("aria-pressed", i === k ? "true" : "false"),
        );
      }
      gb.forEach((b, i) => b.addEventListener("click", () => grp(i)));
      grp(0);

      // precio
      const pin = $<HTMLInputElement>("#pr-in");
      const pval = $<HTMLElement>("#pr-val");
      const pmk = $<HTMLElement>("#pr-mk");
      const pout = $<HTMLElement>("#pr-out");
      const lg = (p: number, c: number, k: number) =>
        1 / (1 + Math.exp(-(p - c) / k));
      const pc = (x: number) => `${Math.round(x * 100)} %`;
      function price() {
        if (!pin || !pval || !pmk || !pout) return;
        const p = Number(pin.value);
        pval.textContent = `$${p.toFixed(2).replace(".", ",")}`;
        pmk.style.left = `${((p - 10) / 26) * 100}%`;
        const caro = lg(p, 23, 2.5);
        const barato = 1 - lg(p, 19, 2.5);
        const t =
          p < 17.4
            ? "Por debajo del rango: empieza a generar duda por barato."
            : p > 24
              ? "Por encima del rango: empieza a perder a quien lo ve caro."
              : "Dentro del rango aceptable.";
        pout.innerHTML = `<b>${t}</b>Lo considera caro: ${pc(caro)}. Lo considera barato: ${pc(barato)}.`;
      }
      pin?.addEventListener("input", price);
      price();

      // arma tu estudio
      const Q: Record<string, [string, string][]> = {
        mira: [
          ["Seguimiento ocular", "con personas"],
          ["Análisis visual con IA", "para descartar versiones antes"],
        ],
        emo: [["Video con lectura del rostro", "con personas"]],
        asoc: [["Asociación implícita", "con personas"]],
        ab: [
          ["Variantes implícitas", "con personas"],
          ["Seguimiento ocular", "con personas"],
        ],
        precio: [["Encuestas y precio", "con personas"]],
        sitio: [
          ["Recorrido web", "simulación"],
          ["Auditoría SEO", "sin participantes"],
        ],
      };
      const out = $<HTMLElement>("#arma-out");
      const qb = $$<HTMLButtonElement>(".aq .chip");
      function arma() {
        if (!out) return;
        const sel = qb.filter((b) => b.getAttribute("aria-pressed") === "true");
        const seen: Record<string, number> = {};
        const L: [string, string][] = [];
        sel.forEach((b) => {
          const qKey = b.dataset.q || "";
          (Q[qKey] || []).forEach((t) => {
            if (!seen[t[0]]) {
              seen[t[0]] = 1;
              L.push(t);
            }
          });
        });
        if (!L.length) {
          out.innerHTML = '<p class="aempty">Tu estudio aparece aquí.</p>';
          return;
        }
        const people = L.some((t) => t[1] === "con personas");
        if (L.length > 1) {
          L.push(["Baterías e informe", "todo en una liga y una sola lectura"]);
        }
        out.innerHTML = `<h3>Tu estudio: ${
          L.length > 1
            ? `${L.length - 1} herramientas y un informe`
            : "1 herramienta"
        }</h3><ul>${L.map(
          (t, i) =>
            `<li style="animation-delay:${i * 0.12}s">${t[0]}<span>${t[1]}</span></li>`,
        ).join("")}</ul><p class="an2">${
          people
            ? "Cuánta gente hace falta lo calcula la plataforma según el margen de error que aceptes. "
            : ""
        }Cada resultado sale con su sello y su margen de error.</p><a class="btn" href="/#demo" data-go="demo" id="arma-go">Pedir una demostración con este estudio</a>`;
        $("#arma-go")?.addEventListener("click", () => {
          const f = $<HTMLInputElement>("#f-preg");
          const tx = `Quiero saber: ${sel
            .map((b) => (b.textContent || "").toLowerCase())
            .join(", ")}.`;
          if (f) {
            f.value = tx;
            f.dispatchEvent(new Event("input", { bubbles: true }));
          }
        });
      }
      qb.forEach((b) => {
        b.addEventListener("click", () => {
          b.setAttribute(
            "aria-pressed",
            b.getAttribute("aria-pressed") === "true" ? "false" : "true",
          );
          arma();
          AE.blip?.("foco");
        });
      });

      // acordeón: una abierta a la vez
      const ac = $$<HTMLDetailsElement>(".acc");
      ac.forEach((d) => {
        d.addEventListener("toggle", () => {
          if (d.open) {
            ac.forEach((x) => {
              if (x !== d) x.open = false;
            });
          }
        });
      });

      // Método: tocar para leer lo difuso, y la línea del recorrido
      $$<HTMLElement>(".sn").forEach((c) => {
        c.addEventListener("click", () => c.classList.toggle("open"));
      });
      const tl = $<HTMLElement>("#tl");
      const tf = $<HTMLElement>("#tl-fill");
      function tline() {
        if (!tl || !tl.offsetParent || !tf) return;
        const r = tl.getBoundingClientRect();
        tf.style.transform = `scaleY(${clamp(
          (window.innerHeight * 0.62 - r.top) / r.height,
        )})`;
      }
      window.addEventListener("scroll", tline, { passive: true });
      window.addEventListener("resize", tline);
      AE.tline = tline;
    })();

    /* ---------- Menú: el punto difuso abre lo demás; páginas nuevas ---------- */
    (function initMenuAndPages() {
      const mb = $<HTMLButtonElement>("#more");
      const sh = $<HTMLElement>("#sheet");
      if (mb && sh) {
        function set(o: boolean) {
          sh!.hidden = !o;
          mb!.setAttribute("aria-expanded", o ? "true" : "false");
          if (o) {
            sh!.classList.remove("on");
            void sh!.offsetWidth;
            sh!.classList.add("on");
            AE.blip?.("foco");
          }
        }
        mb.addEventListener("click", (e) => {
          e.stopPropagation();
          set(sh.hidden);
        });
        document.addEventListener("click", (e) => {
          const target = e.target as Element | null;
          if (!sh.hidden && !target?.closest("#sheet")) set(false);
          else if (target?.closest("#sheet a")) set(false);
        });
        document.addEventListener("keydown", (e) => {
          if (e.key === "Escape" && !sh.hidden) {
            set(false);
            mb.focus();
          }
        });
      }

      // informe con tu marca (agencias)
      const rep = $<HTMLElement>("#rep");
      $$<HTMLButtonElement>(".sw button").forEach((b) => {
        b.addEventListener("click", () => {
          $$<HTMLButtonElement>(".sw button").forEach((x) =>
            x.setAttribute("aria-pressed", x === b ? "true" : "false"),
          );
          if (rep) {
            rep.classList.remove("sw1", "sw0");
            void rep.offsetWidth;
            rep.classList.add(b.dataset.b === "1" ? "sw1" : "sw0");
          }
        });
      });

      // blog: filtro por línea
      const fb = $$<HTMLButtonElement>(".bfil button");
      const ps = $$<HTMLElement>(".post");
      fb.forEach((b) => {
        b.addEventListener("click", () => {
          fb.forEach((x) =>
            x.setAttribute("aria-pressed", x === b ? "true" : "false"),
          );
          ps.forEach((p) => {
            p.hidden = Boolean(b.dataset.f) && p.dataset.l !== b.dataset.f;
          });
        });
      });

      // ayuda: puertas y búsqueda
      const dr = $$<HTMLButtonElement>(".doors [role=tab]");
      const hl = $$<HTMLElement>(".hlist");
      const hq = $<HTMLInputElement>("#h-q");
      const hn = $<HTMLElement>("#h-none");
      function door(t: HTMLButtonElement) {
        if (!t) return;
        dr.forEach((x) =>
          x.setAttribute("aria-selected", x === t ? "true" : "false"),
        );
        hl.forEach((p) => {
          p.hidden = p.id !== t.getAttribute("aria-controls");
        });
        $$<HTMLElement>(".hi").forEach((a) => {
          a.hidden = false;
        });
        if (hn) hn.hidden = true;
      }
      dr.forEach((t) => {
        t.addEventListener("click", () => {
          if (hq) hq.value = "";
          door(t);
        });
      });
      const norm = (x: string) =>
        x
          .toLowerCase()
          .normalize("NFD")
          .replace(/[\u0300-\u036f]/g, "");
      hq?.addEventListener("input", () => {
        const q = norm(hq.value.trim());
        if (!q) {
          door(
            dr.find((x) => x.getAttribute("aria-selected") === "true") || dr[0],
          );
          return;
        }
        let n = 0;
        hl.forEach((p) => {
          let any = false;
          $$<HTMLElement>(".hi", p).forEach((a) => {
            const ok = norm(a.textContent || "").indexOf(q) >= 0;
            a.hidden = !ok;
            if (ok) {
              any = true;
              n++;
            }
          });
          p.hidden = !any;
        });
        if (hn) hn.hidden = n > 0;
      });

      // entrar
      $("#f-ent")?.addEventListener("submit", (e) => {
        e.preventDefault();
        const msg = $("#e-msg");
        const email = $<HTMLInputElement>("#e-mail")?.value.trim();
        if (!msg) return;
        if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
          msg.textContent =
            "Ingresa tu correo institucional o de trabajo válido.";
          return;
        }
        msg.textContent =
          "El acceso a app.aesteros.com se activa por invitación de tu organización.";
      });
      $("#f-cod")?.addEventListener("submit", (e) => {
        e.preventDefault();
        const msg = $("#e-msg");
        if (msg) {
          msg.textContent =
            "Los códigos de grupo se activan con la plataforma de tu universidad.";
        }
      });
    })();

    /* ---------- Menú: la pastilla ámbar viaja entre secciones (420 ms, curva trasladar) ---------- */
    (function initPill() {
      const navs = $$<HTMLElement>(".dock nav");
      const last: Record<number, [number, number] | null> = {};
      function place(anim: boolean) {
        navs.forEach((n, k) => {
          const p = $<HTMLElement>(".pil", n);
          const a = $<HTMLElement>('a[aria-current="page"]', n);
          if (!p) return;
          if (!n.offsetParent) {
            last[k] = null;
            return;
          }
          if (!a) {
            p.style.opacity = "0";
            last[k] = null;
            return;
          }
          const x = a.offsetLeft;
          const w = a.offsetWidth;
          const o = last[k];
          p.style.opacity = "1";
          p.style.left = `${x}px`;
          p.style.width = `${w}px`;
          if (
            anim &&
            o &&
            !reduce &&
            p.animate &&
            (o[0] !== x || o[1] !== w)
          ) {
            const l = Math.min(o[0], x);
            const r = Math.max(o[0] + o[1], x + w);
            p.animate(
              [
                { left: `${o[0]}px`, width: `${o[1]}px`, filter: "blur(0px)" },
                {
                  left: `${l + (r - l) * 0.14}px`,
                  width: `${(r - l) * 0.72}px`,
                  filter: "blur(3.5px)",
                  offset: 0.5,
                },
                { left: `${x}px`, width: `${w}px`, filter: "blur(0px)" },
              ],
              { duration: 420, easing: "cubic-bezier(.65,0,.35,1)" },
            );
            AE.blip?.("menu");
          }
          last[k] = [x, w];
          if (n.scrollWidth > n.clientWidth) {
            n.scrollTo({
              left: x - n.clientWidth / 2 + w / 2,
              behavior: anim ? "smooth" : "auto",
            });
          }
        });
      }
      AE.pill = place;
      window.addEventListener("resize", () => place(false));
      if (document.fonts && document.fonts.ready) {
        document.fonts.ready.then(() => place(false));
      }
      requestAnimationFrame(() => place(false));
    })();

    /* ---------- Confianza: tres demostraciones ---------- */
    (function initTrustDemos() {
      const ni = $<HTMLInputElement>("#n-in");
      if (!ni) return;
      const nb = $<HTMLElement>("#n-band");
      const nd = $<HTMLElement>("#n-dot");
      const nv = $<HTMLElement>("#n-val");
      const no = $<HTMLElement>("#n-out");
      const E = 0.24;
      const SD = 0.625;
      const nx = (v: number) => 22 + (v / 1) * 72;
      const f = (v: number) =>
        `${v < 0 ? "−" : "+"}${Math.abs(v).toFixed(2).replace(".", ",")}`;
      function upd() {
        if (!ni || !nb || !nd || !nv || !no) return;
        const n = Number(ni.value);
        const h = (1.96 * SD) / Math.sqrt(n);
        const lo = E - h;
        const hi = E + h;
        const weak = lo <= 0;
        nv.textContent = String(n);
        nd.style.left = `${nx(E)}%`;
        nb.style.left = `${Math.max(0, nx(lo) - 3)}%`;
        nb.style.width = `${
          Math.min(100, nx(hi) + 3) - Math.max(0, nx(lo) - 3)
        }%`;
        nb.classList.toggle("weak", weak);
        no.className = `nout${weak ? " weak" : ""}`;
        no.innerHTML = weak
          ? `<b>Aún no se puede afirmar.</b> Diferencia de ${f(E)}, de ${f(lo)} a ${f(hi)}. El margen cruza el cero.`
          : `<b>Se sostiene.</b> Diferencia de ${f(E)}, de ${f(lo)} a ${f(hi)}.`;
      }
      ni.addEventListener("input", upd);
      upd();

      const R = [
        [
          "Greenwald, Nosek y Banaji (2003)",
          "Algoritmo de puntuación mejorado.",
        ],
        ["Brooke (1996)", "Escala de usabilidad de 10 frases."],
        ["Van Westendorp (1976)", "Medidor de sensibilidad al precio."],
      ];
      const rc = $<HTMLElement>("#r-card");
      const ra = $<HTMLElement>("#r-a");
      const rb = $<HTMLElement>("#r-b");
      const bs = $$<HTMLButtonElement>(".rchips button");
      bs.forEach((b) => {
        b.addEventListener("click", () => {
          bs.forEach((x) =>
            x.setAttribute("aria-pressed", x === b ? "true" : "false"),
          );
          const r = R[Number(b.dataset.r || 0)];
          if (r && ra && rb && rc) {
            ra.textContent = r[0];
            rb.textContent = r[1];
            rc.classList.remove("go");
            void rc.offsetWidth;
            rc.classList.add("go");
          }
        });
      });
    })();

    if (reduce) {
      AE.view = () => {};
      return;
    }

    root.classList.add("anim");
    gsap.registerPlugin(ScrollTrigger);

    /* ---------- Capítulos fijos (GSAP + ScrollTrigger) ---------- */
    function chapter(
      el: HTMLElement,
      build: (tl: gsap.core.Timeline, el: HTMLElement) => void,
    ) {
      const tl = gsap.timeline({
        defaults: { ease: "power2.out" },
        scrollTrigger: {
          trigger: el,
          start: "top top",
          end: "bottom bottom",
          scrub: 1.1,
          invalidateOnRefresh: true,
        },
      });
      build(tl, el);
      tl.set({}, {}, 1);
      return tl;
    }

    function inOut(tl: gsap.core.Timeline, els: (Element | null)[]) {
      tl.fromTo(
        els,
        { autoAlpha: 0, y: 28, filter: "blur(12px)" },
        {
          autoAlpha: 1,
          y: 0,
          filter: "blur(0px)",
          duration: 0.12,
          stagger: 0.02,
          ease: "power1.out",
        },
        0,
      ).to(
        els,
        {
          autoAlpha: 0,
          y: -18,
          filter: "blur(8px)",
          duration: 0.07,
          ease: "power1.inOut",
        },
        0.93,
      );
    }

    function steps(tl: gsap.core.Timeline, el: HTMLElement, at: number[]) {
      $$(".st", el).forEach((s, k) => {
        tl.fromTo(
          s,
          { autoAlpha: 0, y: 16, filter: "blur(8px)" },
          {
            autoAlpha: 1,
            y: 0,
            filter: "blur(0px)",
            duration: 0.07,
            ease: "power1.out",
          },
          at[k],
        );
        if (k < at.length - 1) {
          tl.to(
            s,
            {
              autoAlpha: 0,
              y: -14,
              filter: "blur(6px)",
              duration: 0.055,
              ease: "power1.inOut",
            },
            at[k + 1] - 0.06,
          );
        }
      });
    }

    if (CH[0]) {
      chapter(CH[0], (tl, el) => {
        tl.to($(".hintw", el), { autoAlpha: 0, duration: 0.06 }, 0.02);
        tl.to(
          $(".hero-in", el),
          {
            autoAlpha: 0,
            y: -90,
            filter: "blur(16px)",
            duration: 0.3,
            ease: "power1.in",
          },
          0.12,
        )
          .fromTo(
            $(".mark", el),
            { autoAlpha: 0, scale: 0.92, filter: "blur(22px)" },
            { autoAlpha: 1, scale: 1, filter: "blur(0px)", duration: 0.24 },
            0.56,
          )
          .to(
            $(".mark", el),
            {
              autoAlpha: 0,
              filter: "blur(14px)",
              duration: 0.1,
              ease: "power1.in",
            },
            0.9,
          );
      });
    }

    if (CH[1]) {
      chapter(CH[1], (tl, el) => {
        inOut(tl, [$(".cx", el), $(".vis", el)]);
        steps(tl, el, [0.05, 0.36, 0.64]);
        tl.fromTo(
          $(".heatcss", el),
          { opacity: 0 },
          { opacity: 1, duration: 0.16 },
          0.3,
        ).fromTo(
          $("polyline", el),
          { strokeDashoffset: 1 },
          { strokeDashoffset: 0, duration: 0.16, ease: "none" },
          0.64,
        );
        $$(".nodes g", el).forEach((g, k) => {
          tl.fromTo(
            g,
            { scale: 0, transformOrigin: "50% 50%" },
            { scale: 1, duration: 0.03, ease: "back.out(2)" },
            0.64 + k * 0.07,
          );
        });
        $$(".tag", el).forEach((t, k) => {
          tl.fromTo(
            t,
            { autoAlpha: 0, filter: "blur(8px)" },
            { autoAlpha: 1, filter: "blur(0px)", duration: 0.04 },
            0.66 + k * 0.07,
          );
        });
      });
    }

    if (CH[2]) {
      chapter(CH[2], (tl, el) => {
        inOut(tl, [$(".cx", el), $(".vis", el)]);
        steps(tl, el, [0.05, 0.38, 0.68]);
        const box = $<HTMLElement>(".iat", el);
        $$<HTMLElement>(".words span", el).forEach((w, k) => {
          const t = 0.12 + k * 0.088;
          const d = Number(w.dataset.d || 0);
          tl.fromTo(
            w,
            { autoAlpha: 0, scale: 0.82, x: 0, filter: "blur(12px)" },
            {
              autoAlpha: 1,
              scale: 1,
              filter: "blur(0px)",
              duration: 0.04,
              ease: "power1.out",
            },
            t,
          )
            .to(
              w,
              {
                x: () => d * (box?.clientWidth || 300) * 0.3,
                autoAlpha: 0,
                scale: 0.72,
                filter: "blur(6px)",
                duration: 0.045,
                ease: "power1.inOut",
              },
              t + 0.045,
            )
            .fromTo(
              $(d < 0 ? ".side.l" : ".side.r", el),
              { scale: 1 },
              {
                scale: 1.04,
                duration: 0.02,
                yoyo: true,
                repeat: 1,
                transformOrigin: d < 0 ? "0 50%" : "100% 50%",
                ease: "sine.inOut",
              },
              t + 0.075,
            );
        });
        tl.fromTo(
          $$(".hl", el),
          { autoAlpha: 0 },
          { autoAlpha: 1, duration: 0.05, stagger: 0.03 },
          0.36,
        );
        const o = { v: 0 };
        const dn = $("#dnum");
        tl.fromTo(
          $(".res", el),
          { autoAlpha: 0, y: 20, filter: "blur(10px)" },
          { autoAlpha: 1, y: 0, filter: "blur(0px)", duration: 0.06 },
          0.68,
        ).fromTo(
          o,
          { v: 0 },
          {
            v: 0.58,
            duration: 0.1,
            ease: "power1.out",
            onUpdate: () => {
              if (dn) dn.textContent = `+${o.v.toFixed(2).replace(".", ",")}`;
            },
          },
          0.68,
        );
      });
    }

    if (CH[3]) {
      chapter(CH[3], (tl, el) => {
        inOut(tl, [$(".cx", el), $(".vis", el)]);
        steps(tl, el, [0.05, 0.36, 0.66]);
        const axisSpans = $$(".axis span", el);
        tl.fromTo(
          $(".plot svg", el),
          { clipPath: "inset(-10% 100% -10% 0%)" },
          { clipPath: "inset(-10% 0% -10% 0%)", duration: 0.2, ease: "none" },
          0.34,
        )
          .fromTo(
            $(".leg", el),
            { autoAlpha: 0 },
            { autoAlpha: 1, duration: 0.06 },
            0.34,
          )
          .fromTo(
            $(".rng", el),
            { scaleX: 0, opacity: 0 },
            { scaleX: 1, opacity: 1, duration: 0.1 },
            0.66,
          )
          .fromTo(
            [$(".rg", el), axisSpans[1], axisSpans[2]],
            { autoAlpha: 0 },
            { autoAlpha: 1, duration: 0.05 },
            0.7,
          )
          .fromTo(
            $(".opt", el),
            { autoAlpha: 0, filter: "blur(8px)" },
            { autoAlpha: 1, filter: "blur(0px)", duration: 0.06 },
            0.78,
          );
      });
    }

    if (CH[4]) {
      chapter(CH[4], (tl, el) => {
        tl.fromTo(
          $(".top", el),
          { autoAlpha: 0, y: 46, filter: "blur(18px)" },
          { autoAlpha: 1, y: 0, filter: "blur(0px)", duration: 0.12 },
          0,
        );
        $$(".sl", el).forEach((s, k) => {
          tl.fromTo(
            s,
            { autoAlpha: 0, y: 30, filter: "blur(12px)" },
            { autoAlpha: 1, y: 0, filter: "blur(0px)", duration: 0.1 },
            0.14 + k * 0.1,
          );
        });
      });
    }

    /* ---------- Tramo claro: revelados ---------- */
    $$(
      ".lite .hd,.lite .demo,.lite .aud-c,.lite .tri>div,.lite .ba-tabs,.lite .ask,.snp",
    ).forEach((el) => {
      gsap.from(el, {
        y: 44,
        autoAlpha: 0,
        filter: "blur(12px)",
        duration: 0.9,
        ease: "power3.out",
        clearProps: "filter,transform",
        scrollTrigger: { trigger: el, start: "top 90%", once: true },
      });
    });
    $$(".tc").forEach((el, k) => {
      ScrollTrigger.create({
        trigger: el,
        start: "top 86%",
        once: true,
        onEnter: () => {
          setTimeout(() => el.classList.add("in"), (k % 3) * 140);
        },
      });
    });
    $$(".ba-p").forEach((p) => {
      ScrollTrigger.create({
        trigger: "#antes",
        start: "top 70%",
        once: true,
        onEnter: () => p.classList.add("go"),
      });
    });
    $$(".tgr h3,.proof").forEach((el) => {
      gsap.from(el, {
        y: 30,
        autoAlpha: 0,
        filter: "blur(10px)",
        duration: 0.9,
        ease: "power3.out",
        clearProps: "filter,transform",
        scrollTrigger: { trigger: el, start: "top 90%", once: true },
      });
    });

    /* ---------- Puntos en WebGL ---------- */
    const GL = (function initWebGL() {
      const cv = document.getElementById("gl") as HTMLCanvasElement | null;
      if (!cv) return null;
      let gl: WebGLRenderingContext | null = null;
      try {
        gl = cv.getContext("webgl", {
          alpha: true,
          premultipliedAlpha: true,
          antialias: false,
          powerPreference: "high-performance",
        });
      } catch {}
      if (!gl) return null;

      const N = small()
        ? 5000
        : (navigator.hardwareConcurrency || 4) > 4
          ? 15000
          : 9000;
      const VS =
        "precision mediump float;attribute vec3 aP;attribute vec3 aA;uniform vec2 uR;uniform float uF,uD,uG;varying float vG,vK;void main(){vec2 p=aP.xy/(uR*.5);p.y=-p.y;gl_Position=vec4(p,0.,1.);float d=1.+aP.z*.4;gl_PointSize=uD*aA.x*mix(11.,2.5,uF)*d;vG=aA.y*uG;vK=aA.z;}";
      const FS =
        "precision mediump float;uniform float uF,uA,uL;varying float vG,vK;void main(){float r=length(gl_PointCoord-.5)*2.;float a=smoothstep(1.,mix(0.,.72,uF),r)*mix(.075,.74,uF*uF)*uA*(.55+.45*vK);vec3 c=mix(vec3(1.,.69,0.),vec3(.85,.576,.353),vG);c=mix(c,vec3(.93,.52,0.),uL);gl_FragColor=vec4(c*a,a);}";

      function sh(t: number, s: string) {
        const o = gl!.createShader(t)!;
        gl!.shaderSource(o, s);
        gl!.compileShader(o);
        return o;
      }

      const pr = gl.createProgram()!;
      gl.attachShader(pr, sh(gl.VERTEX_SHADER, VS));
      gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, FS));
      gl.linkProgram(pr);
      if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) return null;
      gl.useProgram(pr);

      const U: Record<string, WebGLUniformLocation | null> = {};
      ["uR", "uF", "uD", "uG", "uA", "uL"].forEach((n) => {
        U[n] = gl!.getUniformLocation(pr, n);
      });

      const pos = new Float32Array(N * 3);
      const att = new Float32Array(N * 3);
      const rnd = new Float32Array(N);
      const ph = new Float32Array(N);
      const sp = new Float32Array(N);
      const loc = new Float32Array(N * 3);
      const SH: Float32Array[] = [];

      function gs() {
        let u = 0;
        while (!u) u = Math.random();
        const v = Math.random();
        return Math.sqrt(-2 * Math.log(u)) * Math.cos(6.2832 * v);
      }

      for (let i = 0; i < N; i++) {
        att[i * 3] = 0.6 + Math.random() * 0.9;
        att[i * 3 + 1] = i % 5 < 3 ? 0 : 1;
        att[i * 3 + 2] = Math.random();
        rnd[i] = Math.random();
        ph[i] = Math.random() * 6.2832;
        sp[i] = 0.4 + Math.random() * 1.1;
        loc[i * 3] = gs();
        loc[i * 3 + 1] = gs();
        loc[i * 3 + 2] = gs();
      }

      const bp = gl.createBuffer();
      const ba = gl.createBuffer();
      const lp = gl.getAttribLocation(pr, "aP");
      const la = gl.getAttribLocation(pr, "aA");
      gl.bindBuffer(gl.ARRAY_BUFFER, ba);
      gl.bufferData(gl.ARRAY_BUFFER, att, gl.STATIC_DRAW);
      gl.enableVertexAttribArray(la);
      gl.vertexAttribPointer(la, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, bp);
      gl.bufferData(gl.ARRAY_BUFFER, pos, gl.DYNAMIC_DRAW);
      gl.enableVertexAttribArray(lp);
      gl.vertexAttribPointer(lp, 3, gl.FLOAT, false, 0, 0);
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
      gl.clearColor(0, 0, 0, 0);

      let W = 0,
        H = 0,
        dpr = 1,
        FAR = 1200,
        c0 = [0, 0],
        R0 = 100,
        mx = 0,
        my = 0,
        tmx = 0,
        tmy = 0;

      function box(el: HTMLElement | null) {
        if (!el) return { x: 0, y: 0, w: 100, h: 100 };
        let x = 0,
          y = 0;
        const w = el.offsetWidth,
          h = el.offsetHeight,
          pin = el.closest(".pin");
        let cur: HTMLElement | null = el;
        while (cur && cur !== pin) {
          x += cur.offsetLeft;
          y += cur.offsetTop;
          cur = cur.offsetParent as HTMLElement | null;
        }
        return { x: x - W / 2, y: y - H / 2, w, h };
      }

      const CK = ["tb", "bc", "ca", "dc"];

      function build() {
        W = window.innerWidth;
        H = window.innerHeight;
        dpr = Math.min(window.devicePixelRatio || 1, small() ? 1.5 : 2);
        cv!.width = W * dpr;
        cv!.height = H * dpr;
        gl!.viewport(0, 0, cv!.width, cv!.height);
        FAR = Math.max(W, H) * 0.8;
        const sm = small();
        const m = Math.min(W, H);
        c0 = sm ? [0, -H * 0.24] : [W * 0.24, -H * 0.02];
        R0 = m * (sm ? 0.17 : 0.2);

        for (let k = 0; k < 6; k++) {
          if (!SH[k]) SH[k] = new Float32Array(N * 3);
        }

        const lg = box($<HTMLElement>(".mark .word"));
        const ad = box($<HTMLElement>("#ad"));
        const hi = box($<HTMLElement>("#hist"));
        const pl = box($<HTMLElement>("#plot"));
        const ho = $$<HTMLElement>(".hole").map(box);
        const cl = [
          [0.235, 0.39, 0.1, 0.085, 0.5],
          [0.82, 0.5, 0.035, 0.17, 0.25],
          [0.175, 0.715, 0.06, 0.03, 0.12],
          [0.1, 0.1, 0.04, 0.025, 0.07],
          [0.585, 0.735, 0.03, 0.035, 0.06],
        ];

        for (let i = 0; i < N; i++) {
          const a = i * 3;
          // 1: el punto nítido
          let r = Math.min(1, Math.abs(gs()) * 0.42) * lg.w * 0.0592;
          let t = Math.random() * 6.2832;
          SH[1][a] = lg.x + lg.w * 0.1833 + Math.cos(t) * r;
          SH[1][a + 1] = lg.y + lg.h * 0.488 + Math.sin(t) * r;
          SH[1][a + 2] = (Math.random() - 0.5) * 0.3;

          // 2: instantes de mirada sobre el anuncio
          let u = Math.random();
          let qSum = 0;
          let k = 0;
          for (k = 0; k < cl.length; k++) {
            qSum += cl[k][4];
            if (u < qSum) break;
          }
          k = Math.min(k, cl.length - 1);
          SH[2][a] =
            ad.x +
            ad.w * Math.min(0.985, Math.max(0.015, cl[k][0] + gs() * cl[k][2]));
          SH[2][a + 1] =
            ad.y +
            ad.h * Math.min(0.98, Math.max(0.02, cl[k][1] + gs() * cl[k][3]));
          SH[2][a + 2] = Math.random() - 0.5;

          // 3: dos distribuciones de tiempos de respuesta
          const g = att[a + 1];
          const mu = g ? 0.6125 : 0.39;
          const sd = g ? 0.1 : 0.085;
          const hh = g ? 0.68 : 0.9;
          t = Math.max(-2.6, Math.min(2.6, gs()));
          const bVal = Math.exp((-t * t) / 2);
          SH[3][a] = hi.x + hi.w * Math.min(1, Math.max(0, mu + t * sd));
          SH[3][a + 1] = hi.y + hi.h - Math.random() * bVal * hh * hi.h;
          SH[3][a + 2] = (Math.random() - 0.5) * 0.6;

          // 4: cuatro curvas de precio
          const q = CURV[CK[i % 4]];
          t = Math.random() * (q.length - 1);
          k = t | 0;
          u = t - k;
          SH[4][a] =
            pl.x +
            (pl.w * (q[k][0] + (q[k + 1][0] - q[k][0]) * u)) / 1000 +
            gs() * 2.2;
          SH[4][a + 1] =
            pl.y +
            (pl.h * (q[k][1] + (q[k + 1][1] - q[k][1]) * u)) / 400 +
            gs() * 2.2;
          SH[4][a + 2] = (Math.random() - 0.5) * 0.5;

          // 5: los tres sellos: disco, punto difuso, aro
          k = i % 3;
          const bBox = ho[k] || { x: 0, y: 0, w: 60, h: 60 };
          r = bBox.w / 2;
          t = Math.random() * 6.2832;
          if (k === 0) r *= Math.sqrt(Math.random());
          else if (k === 1) r *= Math.min(1.5, Math.abs(gs()) * 0.55);
          else r *= 0.86 + Math.random() * 0.12;
          SH[5][a] = bBox.x + bBox.w / 2 + Math.cos(t) * r;
          SH[5][a + 1] = bBox.y + bBox.h / 2 + Math.sin(t) * r;
          SH[5][a + 2] = (Math.random() - 0.5) * 0.3;
        }
        gl!.uniform2f(U.uR, W, H);
        gl!.uniform1f(U.uD, dpr);
      }

      window.addEventListener(
        "pointermove",
        (e) => {
          tmx = e.clientX / window.innerWidth - 0.5;
          tmy = e.clientY / window.innerHeight - 0.5;
        },
        { passive: true },
      );

      let shown = true;
      function draw(
        time: number,
        s: number,
        f: number,
        alpha: number,
        light: number,
        it: number,
      ) {
        if (alpha <= 0.002) {
          if (shown) {
            gl!.clear(gl!.COLOR_BUFFER_BIT);
            shown = false;
          }
          return;
        }
        shown = true;
        mx += (tmx - mx) * 0.06;
        my += (tmy - my) * 0.06;
        const si = Math.min(4, Math.floor(s));
        const fr = Math.min(1, s - si);
        const A = SH[si];
        const B = SH[si + 1];
        if (!A || !B) return;
        const T = time * 0.001;
        const cs = Math.cos(T * 0.22);
        const sn = Math.sin(T * 0.22);
        const amp = 3 + 10 * (1 - f);
        const par = 24;

        for (let i = 0; i < N; i++) {
          const a = i * 3;
          let ax: number, ay: number, az: number;
          if (si === 0) {
            const lx = loc[a];
            const lz = loc[a + 2];
            ax = c0[0] + (lx * cs - lz * sn) * R0;
            ay = c0[1] + loc[a + 1] * R0;
            az = (lx * sn + lz * cs) * 0.5;
            if (it < 1) {
              let q = it * 1.75 - 0.75 * rnd[i];
              q = q < 0 ? 0 : q > 1 ? 1 : q;
              q = 1 - (1 - q) * (1 - q) * (1 - q);
              const fr0 = FAR * (0.75 + 0.6 * sp[i]);
              const sw2 = (1 - q) * 1.4;
              ax = ax * q + (c0[0] + Math.cos(ph[i] + sw2) * fr0) * (1 - q);
              ay = ay * q + (c0[1] + Math.sin(ph[i] + sw2) * fr0) * (1 - q);
            }
          } else {
            ax = A[a];
            ay = A[a + 1];
            az = A[a + 2];
          }
          let t = fr * 1.7 - 0.7 * rnd[i];
          t = t < 0 ? 0 : t > 1 ? 1 : t;
          t = t * t * (3 - 2 * t);
          const arc =
            Math.sin(t * 3.1416) * (24 + 50 * rnd[i]) * (si < 2 ? 1.6 : 1);
          const w = T * sp[i] + ph[i];
          const x =
            ax + (B[a] - ax) * t + Math.cos(ph[i]) * arc + Math.sin(w) * amp;
          const y =
            ay +
            (B[a + 1] - ay) * t +
            Math.sin(ph[i]) * arc +
            Math.cos(w * 0.9) * amp;
          const z = az + (B[a + 2] - az) * t;
          pos[a] = x + mx * z * par;
          pos[a + 1] = y + my * z * par;
          pos[a + 2] = z;
        }
        gl!.bindBuffer(gl!.ARRAY_BUFFER, bp);
        gl!.bufferSubData(gl!.ARRAY_BUFFER, 0, pos);
        gl!.uniform1f(U.uF, f);
        gl!.uniform1f(U.uA, alpha);
        gl!.uniform1f(U.uL, light);
        gl!.uniform1f(U.uG, Math.max(0, 1 - Math.abs(s - 3)));
        gl!.clear(gl!.COLOR_BUFFER_BIT);
        gl!.drawArrays(gl!.POINTS, 0, N);
      }

      return { build, draw };
    })();

    if (GL) root.classList.add("gl");

    /* ---------- Ciclo principal: apertura pausada, cielo, puntos, filtro de sonido ---------- */
    let IT0 = 0;
    const ITD = 3400;
    let intro =
      (root.dataset.view || "inicio") === "inicio" && window.scrollY < 40;
    if (intro) root.classList.add("wait");

    function endIntro(fast: boolean) {
      if (!intro) return;
      intro = false;
      root.classList.remove("wait");
      root.classList.add("opened");
      if (fast) IT0 = -1e9;
    }

    if (intro) {
      ["pointerdown", "keydown", "wheel", "touchstart"].forEach((n) => {
        window.addEventListener(n, () => endIntro(true), {
          passive: true,
          once: true,
        });
      });
      window.addEventListener(
        "scroll",
        () => {
          if (window.scrollY > 30) endIntro(true);
        },
        { passive: true },
      );
    }

    const sky = $<HTMLElement>("#sky");
    const sel = CH[4];
    const holes = $$<HTMLElement>(".hole");
    let lastChap = -1;
    let lastL = -1;
    let built = false;
    let prevTime = 0;
    const mix = (a: number, b: number, t: number) =>
      Math.round(a + (b - a) * t);

    function frame(time: number) {
      requestAnimationFrame(frame);
      if (view !== "inicio" || document.hidden) return;
      if (GL && !built) {
        GL.build();
        built = true;
      }
      if (!IT0) IT0 = time;
      const it = clamp((time - IT0) / ITD);
      if (intro && it > 0.86) endIntro(false);
      if (!GL && intro && it > 0.3) endIntro(false);

      const dt = Math.min(0.05, (time - (prevTime || time)) / 1000);
      prevTime = time;
      const kk = 1 - Math.exp(-dt * 5.5);
      for (let i = 0; i < 5; i++) {
        const raw = prog(CH[i]);
        PR[i] = raw;
        P[i] += (raw - P[i]) * (Math.abs(raw - P[i]) > 0.6 ? 1 : kk);
      }
      AE.dbg = { raw: PR.slice(), p: P.slice() };
      const s =
        ease(P[0] / 0.8) +
        ease(P[1] / 0.2) +
        ease(P[2] / 0.26) +
        ease(P[3] / 0.26) +
        ease(P[4] / 0.34);
      const fr = s - Math.floor(s);
      let f =
        s < 1
          ? ease(s) * ease(s)
          : 1 - (s < 2 ? 0.82 : 0.6) * Math.sin(Math.PI * Math.min(1, fr));
      if (s >= 5) f = 1;

      const L = ease((P[4] - 0.36) / 0.24);
      const out = ease((P[4] - 0.82) / 0.14);

      if (L !== lastL && sky && sel) {
        lastL = L;
        sky.style.backgroundColor = `rgb(${mix(11, 255, L)},${mix(9, 247, L)},${mix(7, 230, L)})`;
        const k = `${mix(255, 20, L)},${mix(247, 17, L)},${mix(230, 12, L)}`;
        sel.style.setProperty("--ink", `rgb(${k})`);
        sel.style.setProperty("--mut", `rgba(${k},.72)`);
      }

      if (GL) {
        for (let i = 0; i < 3; i++) {
          if (holes[i]) holes[i].style.opacity = String(out);
        }
        const alpha =
          (1 - out) *
          (small() ? 0.5 + 0.5 * clamp(s) : 1) *
          (1 -
            0.62 *
              ease((P[1] - 0.6) / 0.06) *
              (1 - ease((P[1] - 0.97) / 0.03))) *
          (1 -
            0.66 *
              ease((P[3] - 0.5) / 0.08) *
              (1 - ease((P[3] - 0.97) / 0.03)));
        GL.draw(time, s, f, alpha, L, it);
      }

      const chap = Math.min(5, Math.round(s));
      if (chap !== lastChap) {
        if (lastChap >= 0 && AE.blip) {
          AE.blip(chap === 5 ? "sello" : "foco");
        }
        lastChap = chap;
      }
      AE.tone?.(f);
    }

    let rz: ReturnType<typeof setTimeout>;
    window.addEventListener("resize", () => {
      clearTimeout(rz);
      rz = setTimeout(() => {
        built = false;
      }, 180);
    });
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(() => {
        built = false;
        ScrollTrigger.refresh();
      });
    }
    window.addEventListener("load", () => {
      built = false;
      ScrollTrigger.refresh();
    });

    AE.view = (n: string) => {
      if (n === view && lastChap >= -1 && AE.on) return;
      AE.on = 1;
      view = n;
      if (AE.tline) setTimeout(AE.tline, 60);
      if (n === "inicio") {
        built = false;
        lastL = -1;
        requestAnimationFrame(() => {
          ScrollTrigger.refresh();
        });
      }
    };

    AE.view(root.dataset.view || "inicio");
    requestAnimationFrame(frame);

    return () => {
      document.removeEventListener("click", handleDocClick);
    };
  }, [router]);

  return (
    <>
      <a className="skip" href="#contenido">
        Ir al contenido
      </a>
      <header className="dock">
        <Link className="brand" href="/" aria-label="Aesteros, inicio">
          <Logo uid="n" height={18} />
        </Link>
        <nav className="n1" aria-label="Principal">
          <i className="pil" aria-hidden="true" />
          <Link
            href="/"
            data-v="inicio"
            aria-current={
              VIEWS_META[currentView]?.nav === "inicio" ? "page" : undefined
            }
          >
            Inicio
          </Link>
          <Link
            href="/producto"
            data-v="producto"
            aria-current={
              VIEWS_META[currentView]?.nav === "producto" ? "page" : undefined
            }
          >
            Producto
          </Link>
          <Link
            href="/metodo"
            data-v="metodo"
            aria-current={
              VIEWS_META[currentView]?.nav === "metodo" ? "page" : undefined
            }
          >
            Método
          </Link>
        </nav>
        <nav className="n2" aria-label="Explorar">
          <i className="pil" aria-hidden="true" />
          <Link className="bk" href="/">
            <span aria-hidden="true">‹</span> Inicio
          </Link>
          <Link
            href="/universidades"
            data-v="universidades"
            aria-current={
              VIEWS_META[currentView]?.nav === "universidades"
                ? "page"
                : undefined
            }
          >
            Universidades
          </Link>
          <Link
            href="/agencias"
            data-v="agencias"
            aria-current={
              VIEWS_META[currentView]?.nav === "agencias" ? "page" : undefined
            }
          >
            Agencias
          </Link>
          <Link
            href="/empresas"
            data-v="empresas"
            aria-current={
              VIEWS_META[currentView]?.nav === "empresas" ? "page" : undefined
            }
          >
            Empresas
          </Link>
          <Link
            href="/planes"
            data-v="planes"
            aria-current={
              VIEWS_META[currentView]?.nav === "planes" ? "page" : undefined
            }
          >
            Planes
          </Link>
          <Link
            href="/blog"
            data-v="blog"
            aria-current={
              VIEWS_META[currentView]?.nav === "blog" ? "page" : undefined
            }
          >
            Blog
          </Link>
          <Link
            href="/ayuda"
            data-v="ayuda"
            aria-current={
              VIEWS_META[currentView]?.nav === "ayuda" ? "page" : undefined
            }
          >
            Ayuda
          </Link>
        </nav>
        <button
          type="button"
          className={`more${VIEWS_META[currentView]?.mode === "mas" ? " here" : ""}`}
          id="more"
          aria-expanded="false"
          aria-controls="sheet"
          aria-label="Explorar más páginas"
        >
          <i aria-hidden="true" />
          <span aria-hidden="true">Explorar</span>
        </button>
        <button
          type="button"
          className="snd"
          id="snd"
          aria-pressed="false"
          aria-label="Sonido"
        >
          <i aria-hidden="true" />
          <span>Sonido</span>
        </button>
        <Link className="btn sm" href="/#demo" data-go="demo">
          <span className="w">Demostración</span>
          <span className="n">Demo</span>
        </Link>
      </header>

      <div className="sheet" id="sheet" hidden>
        <div className="shg mob">
          <em>El sitio</em>
          <Link className="m1" href="/">
            Inicio
          </Link>
          <Link className="m1" href="/producto">
            Producto
          </Link>
          <Link href="/metodo">Método</Link>
        </div>
        <div className="shg">
          <em>Para ti</em>
          <Link href="/universidades">Universidades</Link>
          <Link href="/agencias">Agencias</Link>
          <Link href="/empresas">Empresas</Link>
        </div>
        <div className="shg">
          <em>Comprar</em>
          <Link href="/planes">Planes</Link>
          <Link href="/novedades">Novedades</Link>
        </div>
        <div className="shg">
          <em>Aprender</em>
          <Link href="/blog">Blog</Link>
          <Link href="/ayuda">Centro de ayuda</Link>
        </div>
        <div className="shg end">
          <Link className="entb" href="/entrar" aria-label="Entrar a Aesteros">
            <span>Entrar a</span>
            <Logo uid="sh" height={20} />
          </Link>
        </div>
      </div>

      <span className="cur" id="cur" aria-hidden="true" />

      <main id="contenido">
        {(Object.keys(VIEWS_META) as ViewId[]).map((vid) => {
          const vMeta = VIEWS_META[vid];
          const vData = VIEWS_HTML[vid];
          return (
            <section
              key={vid}
              className={vData.className}
              id={`v-${vid}`}
              data-nav={vMeta.nav !== vid ? vMeta.nav : undefined}
              data-au={vid === "producto" ? "u" : undefined}
              hidden={vid !== currentView}
              suppressHydrationWarning
              dangerouslySetInnerHTML={{ __html: vData.html }}
            />
          );
        })}
      </main>

      <footer className="foot">
        <span className="brand">
          <Logo uid="f" height={20} />
        </span>
        <span>Percepción, comparada.</span>
        <span className="flk">
          <Link href="/privacidad">Privacidad</Link>
          <Link href="/terminos">Términos</Link>
          <Link href="/camara">Uso de cámara</Link>
        </span>
        <span className="fine">
          Aesteros · Neuromarketing en línea, con personas reales.
        </span>
      </footer>
    </>
  );
}
