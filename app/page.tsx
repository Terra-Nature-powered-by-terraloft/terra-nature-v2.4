"use client"

import { useState, useRef, useEffect } from "react"
import { motion, useScroll, useTransform, useInView } from "framer-motion"
import {
  Mail,
  ExternalLink,
  ArrowRight,
  Menu,
  X,
  ChevronDown,
  MapPin,
} from "lucide-react"
import SphereOrb from "@/components/SphereOrb"
import TerraLogo from "@/components/TerraLogo"

const ease = [0.22, 1, 0.36, 1] as const

/* ── Clip-from-below text reveal (hut8 style) ── */
function Reveal({
  children,
  delay = 0,
  className = "",
}: {
  children: React.ReactNode
  delay?: number
  className?: string
}) {
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: true, margin: "-5%" })
  return (
    <div ref={ref} className={`overflow-hidden ${className}`}>
      <motion.div
        initial={{ y: "110%", opacity: 0 }}
        animate={inView ? { y: 0, opacity: 1 } : {}}
        transition={{ duration: 1.05, delay, ease }}
      >
        {children}
      </motion.div>
    </div>
  )
}

/* ── Simple fade + rise ── */
function FadeUp({
  children,
  delay = 0,
  className = "",
}: {
  children: React.ReactNode
  delay?: number
  className?: string
}) {
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: true, margin: "-5%" })
  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 28 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.85, delay, ease }}
      className={className}
    >
      {children}
    </motion.div>
  )
}

/* ── Horizontal rule that draws itself ── */
function DrawLine({ delay = 0, className = "" }: { delay?: number; className?: string }) {
  const ref = useRef<HTMLDivElement>(null)
  const inView = useInView(ref, { once: true })
  return (
    <div ref={ref} className={`h-px bg-cold-white/8 overflow-hidden ${className}`}>
      <motion.div
        className="h-full bg-cold-white/25"
        style={{ transformOrigin: "left" }}
        initial={{ scaleX: 0 }}
        animate={inView ? { scaleX: 1 } : {}}
        transition={{ duration: 1.4, delay, ease }}
      />
    </div>
  )
}

/* ── Section slide-number bar ── */
function SlideBar({ n }: { n: string }) {
  return (
    <div className="relative z-10 px-6 md:px-10 py-4 border-t border-cold-white/5 flex justify-between text-[9px] font-bold tracking-[0.22em] text-cold-white/15 uppercase select-none">
      <span>{n}</span>
      <span>Terranature.io</span>
    </div>
  )
}

/* ═══════════════════════════════════════════════════════════ */
export default function Home() {
  const [menuOpen, setMenuOpen] = useState(false)
  const { scrollYProgress } = useScroll()
  const heroOpacity = useTransform(scrollYProgress, [0, 0.12], [1, 0])
  const heroScale  = useTransform(scrollYProgress, [0, 0.12], [1, 0.97])

  const goto = (id: string) => {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" })
    setMenuOpen(false)
  }

  const navLinks = [
    { id: "thesis",       label: "Thesis" },
    { id: "system",       label: "System" },
    { id: "verification", label: "Verifikation" },
    { id: "founder",      label: "Founder" },
    { id: "roadmap",      label: "Roadmap" },
  ]

  return (
    <div className="bg-[#07070d] text-cold-white overflow-x-hidden">

      {/* ── Fixed nav ── */}
      <motion.nav
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.6, duration: 0.8 }}
        className="fixed inset-x-0 top-0 z-50 flex items-center justify-between px-6 md:px-10 py-4"
      >
        <button onClick={() => goto("hero")} className="flex items-center gap-2.5 group">
          <TerraLogo className="w-6 h-7 text-cold-white/70 group-hover:text-cold-white transition-colors" />
          <span className="hidden sm:block text-[10px] font-black tracking-[0.18em] text-cold-white/50 group-hover:text-cold-white transition-colors uppercase">
            Terra Nature
          </span>
        </button>

        <div className="hidden md:flex gap-7">
          {navLinks.map(({ id, label }) => (
            <button
              key={id}
              onClick={() => goto(id)}
              className="text-[9px] font-bold tracking-[0.16em] text-cold-white/35 hover:text-cold-white transition-colors uppercase"
            >
              {label}
            </button>
          ))}
        </div>

        <button
          onClick={() => setMenuOpen(v => !v)}
          className="md:hidden p-2 text-cold-white/50 hover:text-cold-white transition-colors"
        >
          {menuOpen ? <X size={18} /> : <Menu size={18} />}
        </button>
      </motion.nav>

      {/* Mobile fullscreen menu */}
      {menuOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="fixed inset-0 z-40 bg-[#07070d]/97 backdrop-blur-xl flex flex-col items-center justify-center gap-10"
        >
          {navLinks.map(({ id, label }) => (
            <button
              key={id}
              onClick={() => goto(id)}
              className="text-4xl font-black tracking-tight text-cold-white/50 hover:text-cold-white transition-colors uppercase"
            >
              {label}
            </button>
          ))}
        </motion.div>
      )}

      {/* ── Sections ── */}
      <HeroSection goto={goto} heroOpacity={heroOpacity} heroScale={heroScale} />
      <ThesisSection />
      <SystemSection />
      <VerificationSection />
      <FounderSection />
      <RoadmapSection />

      {/* ── Footer ── */}
      <footer className="border-t border-cold-white/5 px-6 md:px-10 py-8 flex flex-col md:flex-row gap-4 items-center justify-between">
        <div className="flex items-center gap-2.5">
          <TerraLogo className="w-4 h-5 text-cold-white/20" />
          <span className="text-[9px] font-bold tracking-[0.18em] text-cold-white/18 uppercase">
            © 2026 Terra Nature · powered by Terraloft
          </span>
        </div>
        <div className="flex gap-6">
          {navLinks.map(({ id, label }) => (
            <button
              key={id}
              onClick={() => goto(id)}
              className="text-[9px] font-bold tracking-[0.14em] text-cold-white/18 hover:text-cold-white/50 transition-colors uppercase"
            >
              {label}
            </button>
          ))}
        </div>
        <span className="text-[9px] font-bold tracking-[0.18em] text-cold-white/18 uppercase">
          terranature.io
        </span>
      </footer>
    </div>
  )
}

/* ═══════════════════════════════════════════════════════════ */
/* HERO                                                        */
/* ═══════════════════════════════════════════════════════════ */
function HeroSection({
  goto,
  heroOpacity,
  heroScale,
}: {
  goto: (id: string) => void
  heroOpacity: any
  heroScale: any
}) {
  return (
    <section id="hero" className="relative min-h-[100dvh] flex flex-col overflow-hidden">
      <SphereOrb variant="indigo" position="top-right" size={1600} intensity="hero" />

      {/* Top meta bar */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4, duration: 1 }}
        className="relative z-10 flex justify-between px-6 md:px-10 pt-20 text-[9px] font-bold tracking-[0.22em] text-cold-white/20 uppercase"
      >
        <span>Powered by Terraloft</span>
        <span>Company Profile · 2026</span>
      </motion.div>

      {/* Glowing logo centrepiece */}
      <motion.div
        initial={{ opacity: 0, scale: 0.75 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 2.8, ease: [0.16, 1, 0.3, 1] }}
        className="relative z-10 flex-1 flex items-center justify-center py-12"
      >
        <div className="relative">
          <div className="absolute inset-0 -m-24 rounded-full bg-electric-indigo/15 blur-[100px]" />
          <div className="absolute inset-0 -m-10 rounded-full bg-soft-lavender/8 blur-[60px]" />
          <TerraLogo className="w-28 h-36 md:w-44 md:h-56 text-cold-white relative z-10 drop-shadow-[0_0_40px_rgba(99,102,241,0.5)]" />
        </div>
      </motion.div>

      {/* Headline */}
      <motion.div
        style={{ opacity: heroOpacity, scale: heroScale }}
        className="relative z-10 px-6 md:px-10"
      >
        <Reveal delay={0.2}>
          <h1 className="text-[18vw] sm:text-[14vw] md:text-[11vw] font-black leading-[0.84] tracking-[-0.045em] text-cold-white">
            Terra
          </h1>
        </Reveal>
        <Reveal delay={0.38}>
          <h1 className="text-[18vw] sm:text-[14vw] md:text-[11vw] font-black leading-[0.84] tracking-[-0.045em] text-cold-white">
            Nature.
          </h1>
        </Reveal>
      </motion.div>

      <DrawLine delay={0.9} className="relative z-10 mx-6 md:mx-10 mt-7" />

      <div className="relative z-10 flex justify-between items-end px-6 md:px-10 py-5">
        <FadeUp delay={1.0}>
          <p className="text-[10px] text-cold-white/45 tracking-[0.14em] uppercase font-semibold">
            Abwärme · Energiewandlung · Nachweis
          </p>
        </FadeUp>
        <FadeUp delay={1.1}>
          <p className="hidden sm:block text-[9px] text-cold-white/22 tracking-[0.18em] uppercase font-bold">
            Deep-Tech · Rosenheim, Bavaria
          </p>
        </FadeUp>
      </div>

      {/* Scroll indicator + bottom bar */}
      <div className="relative z-10 flex justify-between items-center px-6 md:px-10 py-4 border-t border-cold-white/5 text-[9px] font-bold tracking-[0.22em] text-cold-white/15 uppercase">
        <span>01</span>
        <motion.button
          onClick={() => goto("thesis")}
          animate={{ y: [0, 7, 0] }}
          transition={{ duration: 2.5, repeat: Infinity, ease: "easeInOut" }}
          className="text-cold-white/22 hover:text-cold-white/60 transition-colors"
        >
          <ChevronDown size={16} />
        </motion.button>
        <span>Terranature.io</span>
      </div>
    </section>
  )
}

/* ═══════════════════════════════════════════════════════════ */
/* THESIS                                                      */
/* ═══════════════════════════════════════════════════════════ */
function ThesisSection() {
  const ref = useRef<HTMLElement>(null)
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "end start"] })
  const orbY = useTransform(scrollYProgress, [0, 1], [-100, 100])

  return (
    <section id="thesis" ref={ref} className="relative min-h-[100dvh] flex flex-col overflow-hidden grain">
      <motion.div style={{ y: orbY }} className="absolute inset-0 pointer-events-none">
        <SphereOrb variant="indigo" position="top-right" size={1300} intensity="medium" />
      </motion.div>

      <div className="relative z-10 px-6 md:px-10 pt-28 md:pt-32 flex-1">
        <FadeUp>
          <p className="text-[9px] font-bold tracking-[0.22em] text-electric-indigo/50 uppercase mb-16">
            01 — Thesis
          </p>
        </FadeUp>

        <div className="mb-16 text-center">
          <Reveal delay={0.1}>
            <h2 className="text-[10vw] md:text-[7vw] font-black leading-[0.88] tracking-[-0.032em] text-cold-white">
              Industrielle
            </h2>
          </Reveal>
          <Reveal delay={0.22}>
            <h2 className="text-[10vw] md:text-[7vw] font-black leading-[0.88] tracking-[-0.032em] text-cold-white">
              Emissionen
            </h2>
          </Reveal>
          <Reveal delay={0.34}>
            <h2 className="text-[10vw] md:text-[7vw] font-black leading-[0.88] tracking-[-0.032em] text-cold-white">
              als{" "}
              <span className="text-thermal-amber">Nachweis.</span>
            </h2>
          </Reveal>
        </div>

        <DrawLine delay={0.6} className="mb-12 max-w-3xl mx-auto" />

        <div className="max-w-2xl mx-auto space-y-6 text-center">
          <FadeUp delay={0.7}>
            <p className="text-base md:text-lg text-cold-white/48 font-light leading-relaxed">
              Terra Nature ist eine Deep-Tech-Plattform für industrielle Abwärmenutzung.
              Das System erfasst hochtemperierte thermische Ströme und führt sie in
              Energie, nutzbare Wärme und kryptografisch verifizierten Nachweis.
            </p>
          </FadeUp>
          <FadeUp delay={0.85}>
            <p className="text-base md:text-lg text-cold-white/48 font-light leading-relaxed">
              Jede erzeugte Einheit wird physikalisch erfasst, strukturiert verdichtet
              und revisionsfähig referenzierbar gemacht — nicht als Schätzung,
              sondern als nachvollziehbare Infrastruktur.
            </p>
          </FadeUp>
        </div>
      </div>

      <SlideBar n="02" />
    </section>
  )
}

/* ═══════════════════════════════════════════════════════════ */
/* SYSTEM                                                      */
/* ═══════════════════════════════════════════════════════════ */
function SystemSection() {
  const ref = useRef<HTMLElement>(null)
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "end start"] })
  const orbY = useTransform(scrollYProgress, [0, 1], [100, -100])
  const isInView = useInView(ref, { once: true, margin: "-20%" })
  const [count, setCount] = useState(0)

  useEffect(() => {
    if (!isInView) return
    let frame: number
    const startTime = performance.now()
    const duration = 2200
    const target = 11
    const tick = (now: number) => {
      const t = Math.min((now - startTime) / duration, 1)
      const eased = 1 - Math.pow(1 - t, 3)
      setCount(Math.round(eased * target))
      if (t < 1) frame = requestAnimationFrame(tick)
    }
    frame = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(frame)
  }, [isInView])

  const cards = [
    { title: "Industrial Waste Heat", desc: "High-temperature capture from real process environments." },
    { title: "Power Conversion",      desc: "ORC turbine and TEG module integration at scale." },
    { title: "Heat Recovery",         desc: "Cascaded thermal return at industrial grade." },
    { title: "MRV Architecture",      desc: "Cryptographic measurement, reporting, verification." },
    { title: "Pilot Readiness",       desc: "Site-validated with municipal energy partner." },
    { title: "Climate Alignment",     desc: "EnEfG, CSRD and EU-ETS regulatory frameworks." },
  ]

  return (
    <section id="system" ref={ref} className="relative min-h-[100dvh] flex flex-col overflow-hidden grain">
      <motion.div style={{ y: orbY }} className="absolute inset-0 pointer-events-none">
        <SphereOrb variant="amber" position="bottom-right" size={1400} intensity="medium" />
      </motion.div>

      <div className="relative z-10 px-6 md:px-10 pt-28 md:pt-32 flex-1">
        <FadeUp>
          <p className="text-[9px] font-bold tracking-[0.22em] text-thermal-amber/50 uppercase mb-16">
            02 — System
          </p>
        </FadeUp>

        <div className="mb-10">
          <Reveal delay={0.1}>
            <h2 className="text-[10vw] md:text-[7vw] font-black leading-[0.88] tracking-[-0.032em] text-cold-white">
              Abwärme.
            </h2>
          </Reveal>
          <Reveal delay={0.22}>
            <h2 className="text-[10vw] md:text-[7vw] font-black leading-[0.88] tracking-[-0.032em] text-cold-white">
              Energie.
            </h2>
          </Reveal>
          <Reveal delay={0.34}>
            <h2 className="text-[10vw] md:text-[7vw] font-black leading-[0.88] tracking-[-0.032em] text-thermal-amber">
              Nachweis.
            </h2>
          </Reveal>
        </div>

        {/* Animated counter */}
        <FadeUp delay={0.45} className="mb-14">
          <div className="flex items-end gap-5">
            <span className="text-[20vw] md:text-[13vw] font-black leading-none tracking-[-0.05em] text-thermal-amber tabular-nums">
              {count}%
            </span>
            <div className="pb-4 space-y-1">
              <p className="text-xs font-bold text-cold-white/50 leading-snug">
                Referenzwert ORC-Pfad
              </p>
              <p className="text-[10px] text-cold-white/28 font-light leading-relaxed max-w-[160px]">
                Energieumwandlung aus industrieller Abwärme
              </p>
            </div>
          </div>
        </FadeUp>

        <DrawLine delay={0.55} className="mb-10" />

        {/* Competence cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 mb-8">
          {cards.map((c, i) => (
            <FadeUp key={i} delay={0.6 + i * 0.07}>
              <div className="p-6 rounded-2xl border border-cold-white/6 bg-cold-white/[0.018] hover:border-thermal-amber/15 hover:bg-cold-white/[0.03] transition-all duration-300 group">
                <h3 className="text-sm font-bold text-cold-white mb-2 tracking-tight group-hover:text-thermal-amber transition-colors duration-300">
                  {c.title}
                </h3>
                <p className="text-xs text-cold-white/32 font-light leading-relaxed">{c.desc}</p>
              </div>
            </FadeUp>
          ))}
        </div>
      </div>

      <SlideBar n="03" />
    </section>
  )
}

/* ═══════════════════════════════════════════════════════════ */
/* VERIFICATION                                                */
/* ═══════════════════════════════════════════════════════════ */
function VerificationSection() {
  const ref = useRef<HTMLElement>(null)
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "end start"] })
  const orbY = useTransform(scrollYProgress, [0, 1], [-80, 80])

  const steps = [
    { num: "01", title: "Physikalische Messung",   desc: "Erfassung relevanter Energie- und Betriebsdaten" },
    { num: "02", title: "SHA-256 Hash",            desc: "Kryptografischer Fingerabdruck der Messdaten" },
    { num: "03", title: "Merkle-Aggregation",       desc: "Strukturelle Integrität und Verkettung" },
    { num: "04", title: "IPFS-Anker",              desc: "Manipulationsarme externe Referenzierung" },
    { num: "05", title: "NRG-NFT Nachweisobjekt",  desc: "Verifizierbares digitales Zertifikatsartefakt" },
  ]

  return (
    <section id="verification" ref={ref} className="relative min-h-[100dvh] flex flex-col overflow-hidden grain">
      <motion.div style={{ y: orbY }} className="absolute inset-0 pointer-events-none">
        <SphereOrb variant="indigo" position="top-left" size={1200} intensity="medium" />
      </motion.div>

      <div className="relative z-10 px-6 md:px-10 pt-28 md:pt-32 flex-1">
        <FadeUp>
          <p className="text-[9px] font-bold tracking-[0.22em] text-electric-indigo/50 uppercase mb-16">
            03 — TerraNode Verification Layer
          </p>
        </FadeUp>

        <div className="mb-16">
          <Reveal delay={0.1}>
            <h2 className="text-[9vw] md:text-[6.5vw] font-black leading-[0.88] tracking-[-0.032em] text-cold-white">
              Physikalisch.
            </h2>
          </Reveal>
          <Reveal delay={0.22}>
            <h2 className="text-[9vw] md:text-[6.5vw] font-black leading-[0.88] tracking-[-0.032em] text-cold-white">
              Mathematisch.
            </h2>
          </Reveal>
          <Reveal delay={0.34}>
            <h2 className="text-[9vw] md:text-[6.5vw] font-black leading-[0.88] tracking-[-0.032em] text-electric-indigo">
              Digital nachvollziehbar.
            </h2>
          </Reveal>
        </div>

        <div className="max-w-3xl rounded-2xl overflow-hidden border border-cold-white/5">
          {steps.map((s, i) => (
            <FadeUp key={i} delay={0.45 + i * 0.09}>
              <div className="flex items-start gap-6 px-8 py-6 border-b border-cold-white/5 last:border-none bg-cold-white/[0.015] hover:bg-cold-white/[0.035] transition-colors group">
                <span className="text-[9px] font-bold text-electric-indigo/35 tracking-widest shrink-0 pt-0.5 w-6">
                  {s.num}
                </span>
                <div>
                  <p className="text-sm font-bold text-cold-white mb-0.5 tracking-tight group-hover:text-electric-indigo transition-colors duration-300">
                    {s.title}
                  </p>
                  <p className="text-xs text-cold-white/32 font-light">{s.desc}</p>
                </div>
              </div>
            </FadeUp>
          ))}
        </div>
      </div>

      <SlideBar n="04" />
    </section>
  )
}

/* ═══════════════════════════════════════════════════════════ */
/* FOUNDER                                                     */
/* ═══════════════════════════════════════════════════════════ */
function FounderSection() {
  const ref = useRef<HTMLElement>(null)
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "end start"] })
  const orbY = useTransform(scrollYProgress, [0, 1], [80, -80])

  return (
    <section id="founder" ref={ref} className="relative min-h-[100dvh] flex flex-col overflow-hidden grain">
      <motion.div style={{ y: orbY }} className="absolute inset-0 pointer-events-none">
        <SphereOrb variant="indigo" position="top-right" size={1400} intensity="medium" />
      </motion.div>

      <div className="relative z-10 px-6 md:px-10 pt-28 md:pt-32 flex-1">
        <FadeUp>
          <p className="text-[9px] font-bold tracking-[0.22em] text-cold-white/22 uppercase mb-12">
            Founder Profile · Terra Nature
          </p>
        </FadeUp>

        <div className="mb-6">
          <Reveal delay={0.1}>
            <h2 className="text-[15vw] md:text-[10vw] font-black leading-[0.85] tracking-[-0.04em] text-cold-white">
              Eren
            </h2>
          </Reveal>
          <Reveal delay={0.22}>
            <h2 className="text-[15vw] md:text-[10vw] font-black leading-[0.85] tracking-[-0.04em] text-cold-white">
              Yergezen
            </h2>
          </Reveal>
        </div>

        <FadeUp delay={0.35} className="mb-8">
          <p className="text-base md:text-lg text-cold-white/38 font-light tracking-[0.06em] uppercase text-sm">
            Gründer
          </p>
        </FadeUp>

        <DrawLine delay={0.42} className="mb-8 max-w-sm" />

        {/* Contact pills */}
        <FadeUp delay={0.5} className="flex flex-col sm:flex-row gap-3 mb-14">
          <div className="flex items-center justify-center gap-2.5 px-5 py-3.5 rounded-full border border-cold-white/8 text-cold-white/35 text-sm font-semibold tracking-wide">
            <MapPin size={14} />
            Rosenheim, Germany
          </div>
          <a
            href="mailto:info@terranature.io"
            className="flex items-center justify-center gap-2.5 px-5 py-3.5 rounded-full border border-cold-white/8 text-cold-white/45 hover:text-cold-white hover:border-cold-white/22 transition-all text-sm font-semibold tracking-wide"
          >
            <Mail size={14} />
            info@terranature.io
          </a>
          <a
            href="https://linkedin.com/in/erenyergezen"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-center gap-2.5 px-5 py-3.5 rounded-full border border-cold-white/8 text-cold-white/45 hover:text-cold-white hover:border-cold-white/22 transition-all text-sm font-semibold tracking-wide"
          >
            <ExternalLink size={14} />
            LinkedIn
          </a>
        </FadeUp>

        {/* 13+ big stat */}
        <FadeUp delay={0.62} className="mb-14">
          <div className="flex items-end gap-5">
            <span className="text-[20vw] md:text-[13vw] font-black leading-none tracking-[-0.05em] text-cold-white/88 tabular-nums">
              13+
            </span>
            <div className="pb-4 space-y-1.5">
              <p className="text-sm font-bold text-cold-white/55 leading-snug">
                Dreizehn Jahre technische Praxis.
              </p>
              <p className="text-[10px] text-cold-white/28 font-light leading-relaxed max-w-[200px]">
                Jahre in industriellen Energiesystemen, ORC- und thermischer Ingenieurpraxis.
              </p>
            </div>
          </div>
        </FadeUp>

        <div className="grid md:grid-cols-2 gap-4 max-w-2xl">
          <FadeUp delay={0.75}>
            <div className="p-6 rounded-2xl border border-cold-white/6 bg-cold-white/[0.018]">
              <p className="text-sm text-cold-white/48 font-light leading-relaxed">
                Über{" "}
                <span className="text-cold-white font-semibold">13 Jahre Erfahrung</span> in
                thermodynamischen Systemen, industrieller Energieumwandlung und
                kryptografischer Infrastruktur.
              </p>
            </div>
          </FadeUp>
          <FadeUp delay={0.88}>
            <div className="p-6 rounded-2xl border border-cold-white/6 bg-cold-white/[0.018]">
              <p className="text-sm text-cold-white/48 font-light leading-relaxed">
                Verbindet physikalische Energiesysteme mit Blockchain-Architektur zu einer
                revisionsfähigen Nachweisinfrastruktur für industrielle Abwärme.
              </p>
            </div>
          </FadeUp>
        </div>
      </div>

      <SlideBar n="05" />
    </section>
  )
}

/* ═══════════════════════════════════════════════════════════ */
/* ROADMAP                                                     */
/* ═══════════════════════════════════════════════════════════ */
function RoadmapSection() {
  const ref = useRef<HTMLElement>(null)
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "end start"] })
  const orbY = useTransform(scrollYProgress, [0, 1], [-60, 60])

  const phases = [
    { phase: "Phase 1",    title: "Demonstrator", desc: "Einzelstandort mit vollständiger Nachweiskette" },
    { phase: "Phase 2",    title: "Serie",         desc: "Mehrstandortfähige Standardisierung der Infrastruktur" },
    { phase: "Phase 3",    title: "Cluster",       desc: "Regionale Bündelung und industrielle Betriebsführung" },
    { phase: "Langfristig",title: "Skalierung",    desc: "Überregionale Ausweitung und regulatorische Einbindung" },
  ]

  return (
    <section id="roadmap" ref={ref} className="relative min-h-[100dvh] flex flex-col overflow-hidden grain">
      <motion.div style={{ y: orbY }} className="absolute inset-0 pointer-events-none">
        <SphereOrb variant="whisper-indigo" position="bottom-left" size={1100} intensity="subtle" />
      </motion.div>

      <div className="relative z-10 px-6 md:px-10 pt-28 md:pt-32 flex-1">
        <FadeUp>
          <p className="text-[9px] font-bold tracking-[0.22em] text-electric-indigo/50 uppercase mb-16">
            04 — Roadmap & Kontakt
          </p>
        </FadeUp>

        <div className="mb-16">
          <Reveal delay={0.1}>
            <h2 className="text-[10vw] md:text-[7vw] font-black leading-[0.88] tracking-[-0.032em] text-cold-white">
              Energie wird
            </h2>
          </Reveal>
          <Reveal delay={0.22}>
            <h2 className="text-[10vw] md:text-[7vw] font-black leading-[0.88] tracking-[-0.032em] text-thermal-amber">
              zum Beweis.
            </h2>
          </Reveal>
        </div>

        <div className="max-w-3xl rounded-2xl overflow-hidden border border-cold-white/5 mb-16">
          {phases.map((p, i) => (
            <FadeUp key={i} delay={0.3 + i * 0.1}>
              <div className="flex items-start gap-8 px-8 py-7 border-b border-cold-white/5 last:border-none bg-cold-white/[0.015] hover:bg-cold-white/[0.03] transition-colors">
                <span className="text-[9px] font-bold text-electric-indigo/38 tracking-widest shrink-0 pt-0.5 min-w-[70px]">
                  {p.phase}
                </span>
                <div>
                  <h3 className="text-base font-black text-cold-white mb-1 tracking-tight">{p.title}</h3>
                  <p className="text-xs text-cold-white/32 font-light">{p.desc}</p>
                </div>
              </div>
            </FadeUp>
          ))}
        </div>

        <FadeUp delay={0.85}>
          <p className="text-[9px] font-bold tracking-[0.18em] text-cold-white/25 uppercase mb-5">
            CO₂ · Abwärme · MRV · Bitcoin
          </p>
          <div className="flex flex-col sm:flex-row gap-3">
            <a
              href="mailto:info@terranature.io"
              className="inline-flex items-center gap-3 px-7 py-4 bg-electric-indigo hover:bg-electric-indigo/90 text-cold-white font-bold text-sm rounded-xl transition-all shadow-lg shadow-electric-indigo/20 hover:shadow-electric-indigo/35"
            >
              <Mail size={15} />
              info@terranature.io
            </a>
            <a
              href="https://terranature.io"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-3 px-7 py-4 rounded-xl border border-cold-white/10 text-cold-white/55 hover:text-cold-white hover:border-cold-white/22 font-bold text-sm transition-all"
            >
              <ArrowRight size={15} />
              terranature.io
            </a>
          </div>
        </FadeUp>
      </div>

      <SlideBar n="06" />
    </section>
  )
}
