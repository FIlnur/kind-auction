import { LotCard } from "@/entities/lot/ui/LotCard";


export default function CatalogPage() {
  return (
    <div className="p-10">
      <h1 className="text-2xl mb-5">Каталог лотов</h1>
      
      {/* Пример использования */}
      <LotCard 
        title="Ретро фотоаппарат" 
        price={5000} 
        imageUrl="https://via.placeholder.com/150" 
      />
    </div>
  );
}