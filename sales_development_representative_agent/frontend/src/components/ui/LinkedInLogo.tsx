'use client'

import React from 'react'
import Image from 'next/image'

interface LinkedInLogoProps {
  size?: number
  className?: string
}

export function LinkedInLogo({ size = 20, className = '' }: LinkedInLogoProps) {
  return (
    <Image
      src="/images/linkedin.PNG"
      alt="LinkedIn"
      width={size}
      height={size}
      className={className}
      style={{ width: size, height: size }}
    />
  )
}
