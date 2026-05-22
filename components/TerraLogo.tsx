"use client"

export default function TerraLogo({ className = "" }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 260 320"
      fill="none"
      className={className}
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Outer left leaf */}
      <path
        d="M90 305 C55 265 8 182 28 92 C44 28 88 8 98 46 C112 92 108 218 90 305Z"
        stroke="currentColor"
        strokeWidth="7"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Left leaf main vein */}
      <path
        d="M90 305 C82 238 74 162 88 90"
        stroke="currentColor"
        strokeWidth="5"
        strokeLinecap="round"
      />
      {/* Left leaf side vein upper */}
      <path
        d="M81 188 C67 183 54 174 46 162"
        stroke="currentColor"
        strokeWidth="3.5"
        strokeLinecap="round"
      />
      {/* Left leaf side vein lower */}
      <path
        d="M85 258 C71 252 58 244 50 233"
        stroke="currentColor"
        strokeWidth="3.5"
        strokeLinecap="round"
      />
      {/* Inner right leaf */}
      <path
        d="M112 305 C102 262 132 182 157 96 C170 48 198 33 198 64 C198 100 166 212 112 305Z"
        stroke="currentColor"
        strokeWidth="7"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Right leaf vein */}
      <path
        d="M112 305 C120 246 150 172 160 100"
        stroke="currentColor"
        strokeWidth="5"
        strokeLinecap="round"
      />
      {/* Circuit trace 1 — top */}
      <path
        d="M186 76 C200 63 212 54 224 46"
        stroke="currentColor"
        strokeWidth="5"
        strokeLinecap="round"
      />
      <circle cx="224" cy="46" r="13" stroke="currentColor" strokeWidth="5" />
      <circle cx="224" cy="46" r="5.5" fill="currentColor" />
      {/* Circuit trace 2 — middle */}
      <path
        d="M197 148 C211 143 222 141 235 141"
        stroke="currentColor"
        strokeWidth="5"
        strokeLinecap="round"
      />
      <circle cx="235" cy="141" r="13" stroke="currentColor" strokeWidth="5" />
      <circle cx="235" cy="141" r="5.5" fill="currentColor" />
      {/* Circuit trace 3 — lower */}
      <path
        d="M188 212 C202 218 213 225 224 234"
        stroke="currentColor"
        strokeWidth="5"
        strokeLinecap="round"
      />
      <circle cx="224" cy="234" r="13" stroke="currentColor" strokeWidth="5" />
      <circle cx="224" cy="234" r="5.5" fill="currentColor" />
    </svg>
  )
}
