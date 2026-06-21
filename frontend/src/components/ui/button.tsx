import type { ButtonHTMLAttributes } from 'react'

import { cn } from '../../lib/cn'

type ButtonVariant = 'primary' | 'danger' | 'ghost'

const variantClasses: Record<ButtonVariant, string> = {
  primary: 'border-anthropic bg-anthropic text-bg',
  danger: 'border-danger bg-danger text-ink',
  ghost: 'border-ink/20 bg-transparent text-ink hover:border-anthropic',
}

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButtonVariant
}

export function Button({ className, variant = 'ghost', ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex h-10 items-center justify-center gap-2 border px-3 text-sm font-semibold transition-colors disabled:cursor-not-allowed disabled:opacity-60',
        variantClasses[variant],
        className,
      )}
      {...props}
    />
  )
}
