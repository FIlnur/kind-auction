import { cn } from '~/shared/lib/utils';

// Типизация пропсов — это контракт компонента
interface LotCardProps {
  title: string;
  price: number;
  imageUrl: string;
  className?: string; // Позволяет добавить кастомные стили снаружи
}

export const LotCard = ({ title, price, imageUrl, className }: LotCardProps) => {
  return (
    <div className={cn(
      "border p-4 rounded-lg w-64 transition-shadow hover:shadow-md",
      className
    )}>
      <img 
        src={imageUrl} 
        alt={title} 
        className="w-full h-40 object-cover rounded-md mb-3" 
      />
      <h3 className="font-bold text-lg mb-1">{title}</h3>
      <p className="text-gray-600 text-sm">{price.toLocaleString()} ₽</p>
    </div>
  );
};