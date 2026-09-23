import type { ButtonHTMLAttributes } from 'react';
import { cn } from '~/shared/lib/utils';

// Расширяем стандартные пропсы HTML-кнопки
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
}

export const Button = ({ className, variant = 'primary', children, ...props }: ButtonProps) => {
  return (
    <button
      className={cn(
        "px-4 py-2 rounded-md font-medium transition-colors", // Базовые стили
        variant === 'primary' && "bg-blue-600 text-white hover:bg-blue-700",
        variant === 'secondary' && "bg-gray-200 text-gray-800 hover:bg-gray-300",
        className // Позволяет добавить или переопределить стили снаружи
      )}
      {...props}
    >
      {children}
    </button>
  );
};