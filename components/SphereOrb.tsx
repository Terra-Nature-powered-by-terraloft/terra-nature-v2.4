"use client"

import { motion } from "framer-motion"
import { cn } from "@/lib/utils"

type Variant = "indigo" | "amber" | "whisper-indigo"
type Position = "top-right" | "top-left" | "bottom-right" | "bottom-left"
type Intensity = "hero" | "medium" | "subtle"

interface SphereOrbProps {
  variant?: Variant
  position?: Position
  size?: number
  intensity?: Intensity
  bridge?: boolean
}

const variantStyles: Record<Variant, { primary: string; secondary: string }> = {
  indigo: {
    primary: "rgba(99, 102, 241, VAR)",
    secondary: "rgba(165, 180, 252, VAR)",
  },
  amber: {
    primary: "rgba(245, 158, 11, VAR)",
    secondary: "rgba(252, 211, 77, VAR)",
  },
  "whisper-indigo": {
    primary: "rgba(99, 102, 241, VAR)",
    secondary: "rgba(165, 180, 252, VAR)",
  },
}

const intensityOpacity: Record<Intensity, number> = {
  hero: 0.18,
  medium: 0.10,
  subtle: 0.05,
}

const positionClasses: Record<Position, string> = {
  "top-right": "-top-1/3 -right-1/4",
  "top-left": "-top-1/3 -left-1/4",
  "bottom-right": "-bottom-1/3 -right-1/4",
  "bottom-left": "-bottom-1/3 -left-1/4",
}

export default function SphereOrb({
  variant = "indigo",
  position = "top-right",
  size = 1200,
  intensity = "medium",
  bridge = false,
}: SphereOrbProps) {
  const opacity = intensityOpacity[intensity]
  const { primary, secondary } = variantStyles[variant]

  const color1 = primary.replace("VAR", String(opacity))
  const color2 = secondary.replace("VAR", String(opacity * 0.5))

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 2, ease: "easeOut" }}
      className={cn("pointer-events-none absolute z-0", positionClasses[position])}
      style={{ width: size, height: size }}
    >
      <div
        className="absolute inset-0 rounded-full"
        style={{
          background: `radial-gradient(circle at center, ${color1} 0%, ${color2} 40%, transparent 70%)`,
          filter: "blur(80px)",
        }}
      />
      {bridge && (
        <div
          className="absolute inset-0 rounded-full"
          style={{
            background: `radial-gradient(circle at center, ${color1} 0%, transparent 60%)`,
            filter: "blur(120px)",
            opacity: 0.5,
          }}
        />
      )}
    </motion.div>
  )
}
