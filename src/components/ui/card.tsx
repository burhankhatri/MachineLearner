import React from 'react'
import clsx from 'clsx'

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
}

export function Card({ className, children, ...props }: CardProps) {
  return (
    <div 
      className={clsx(
        'rounded-lg border border-zinc-800 bg-zinc-900/50',
        className
      )} 
      {...props}
    >
      {children}
    </div>
  )
} 